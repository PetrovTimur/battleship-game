import asyncio
import threading
import pickle

# SERVER_IP = '40.91.223.121'
SERVER_IP = '127.0.0.1'


class AsyncioThread(threading.Thread):
    def __init__(self, game, screen):
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
        self.screen = screen

    def run(self):
        self.asyncio_loop.run_until_complete(self.play())

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(SERVER_IP, 8888)

    async def put_in_queue(self, data):
        await self.aqueue.put(data)

    async def put_in_erqueue(self, data):
        await self.erqueue.put(data)

    async def handle_tech_data(self):
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
        await self.connect()

        await self.handle_tech_data()

        self.screen.start_game()
        connected = True

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
                        self.screen.handle_connection_error()
                elif q is send_to_server:
                    send_to_server = asyncio.create_task(self.aqueue.get())
                    data = q.result()
                    self.writer.write(pickle.dumps(data))
                    print(f'Sent {data} to server')
                    await self.writer.drain()
                elif q is handle_error:
                    handle_error = asyncio.create_task(self.erqueue.get())
                    data = q.result()
                    if data == 'quit':
                        connected = False
                        self.writer.write_eof()
                        await self.writer.drain()

        receive_from_server.cancel()
        send_to_server.cancel()
        handle_error.cancel()

        self.writer.close()
        await self.writer.wait_closed()

# TODO send eof from server (?)
# TODO disconnect properly after Esc (?)
