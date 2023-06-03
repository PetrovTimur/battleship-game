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
        super().__init__(daemon=True)

    def update_screen(self, screen):
        self.screen = screen

    def run(self):
        self.asyncio_loop.run_until_complete(self.play())

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(SERVER_IP, 8888)

    async def shoot(self):
        pos, status = self.queue.get()
        self.writer.write(pickle.dumps(pos))
        await self.writer.drain()

        if status == 'dead':
            self.status = False

        return status == 'hit' or status == 'sank'

    async def get_shot(self):
        data = await self.reader.read(100)

        pos = pickle.loads(data)
        self.queue.put(pos)
        status = self.screen.enemy_turn(pos)

        if status == 'dead':
            self.status = False

        return status == 'hit' or status == 'sank'

    async def play(self):
        await self.connect()
        data = await self.reader.read(100)
        turn = data.decode()
        self.queue.put(turn)

        me = self.game.me
        self.writer.write(pickle.dumps(me))
        await self.writer.drain()

        data = await self.reader.read(1000)
        enemy = pickle.loads(data)
        self.queue.put(enemy)

        self.screen.start_game()

        if turn == 'first':
            while self.status:
                while await self.shoot():
                    await asyncio.sleep(0.5)

                if not self.status:
                    break

                while await self.get_shot():
                    continue
        else:
            while self.status:
                while await self.get_shot():
                    continue

                if not self.status:
                    break

                while await self.shoot():
                    await asyncio.sleep(0.5)

        print('Close the connection')
        self.writer.close()
        await self.writer.wait_closed()
