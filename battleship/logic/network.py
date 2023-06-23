"""Multiplayer features."""

import asyncio
import threading
import pickle

SERVER_IP = '40.91.223.121'
# SERVER_IP = '127.0.0.1'


class AsyncioThread(threading.Thread):
    """Thread to handle networking during game."""

    def __init__(self, game, screen):
        """Initialize all params."""
        self.asyncio_loop = asyncio.get_event_loop()
        self.queue = game.queue
        self.screen = screen
        self.status = True
        self.reader = None
        self.writer = None
        self.game = game
        self.aqueue = asyncio.Queue()
        self.erqueue = asyncio.Queue()
        super().__init__(daemon=True)

    def update_screen(self, screen):
        """Get the new screen."""
        self.screen = screen

    def run(self):
        """Start the thread."""
        self.asyncio_loop.run_until_complete(self.play())

    async def connect(self):
        """Connect to server."""
        try:
            self.reader, self.writer = await asyncio.open_connection(SERVER_IP, 8888)
        except ConnectionError:
            self.status = False

    async def put_in_queue(self, data):
        """Put in regular queue."""
        await self.aqueue.put(data)

    async def put_in_erqueue(self, data):
        """Put in error queue."""
        await self.erqueue.put(data)

    async def handle_tech_data(self):
        """Receive and send technical data."""
        data = await self.reader.read(100)
        turn = data.decode()
        self.queue.put(turn)

        me = self.game.me
        self.writer.write(pickle.dumps(me))
        await self.writer.drain()

        data = await self.reader.read(1000)
        enemy = pickle.loads(data)
        self.queue.put(enemy)

    async def play(self):
        """Start the game."""
        await self.connect()

        if not self.status:
            self.screen.connection_error()
            return

        connected = False

        wait_for_opponent = asyncio.create_task(self.handle_tech_data())
        handle_error = asyncio.create_task(self.erqueue.get())

        done, pending = await asyncio.wait([wait_for_opponent, handle_error],
                                           return_when=asyncio.FIRST_COMPLETED)

        for q in done:
            if q is handle_error:
                data = q.result()
                if data == 'quit':
                    connected = False
                    self.writer.write(pickle.dumps(data))
                    await self.writer.drain()

                wait_for_opponent.cancel()
            else:
                connected = True
                handle_error.cancel()
                self.screen.start_game()

        receive_from_server = asyncio.create_task(self.reader.read(100))
        send_to_server = asyncio.create_task(self.aqueue.get())
        handle_error = asyncio.create_task(self.erqueue.get())
        while not self.reader.at_eof() and connected:
            done, pending = await asyncio.wait([send_to_server, receive_from_server, handle_error],
                                               return_when=asyncio.FIRST_COMPLETED)
            for q in done:
                if q is receive_from_server:
                    receive_from_server = asyncio.create_task(self.reader.read(100))
                    try:
                        data = pickle.loads(q.result())
                        self.screen.queue.put(data)
                        self.screen.frame.event_generate('<<EnemyTurn>>')
                    except EOFError:
                        connected = False
                        self.screen.connection_error()
                elif q is send_to_server:
                    send_to_server = asyncio.create_task(self.aqueue.get())
                    data = q.result()
                    self.writer.write(pickle.dumps(data))
                    await self.writer.drain()
                elif q is handle_error:
                    handle_error = asyncio.create_task(self.erqueue.get())
                    data = q.result()
                    if data == 'quit':
                        connected = False
                        self.writer.write(pickle.dumps(data))
                        await self.writer.drain()
                    elif data == 'end':
                        connected = False
                        self.writer.write(pickle.dumps(data))
                        await self.writer.drain()

        receive_from_server.cancel()
        send_to_server.cancel()
        handle_error.cancel()

        await asyncio.sleep(1)

        self.writer.close()
        await self.writer.wait_closed()
