import asyncio


class GameWorld(object):
    counter = 0

    async def run(self):
        while True:
            self.counter += 1
            await asyncio.sleep(1)
            print('WORLD: counter={}'.format(self.counter))