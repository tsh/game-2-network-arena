import asyncio

from map import Map

class GameWorld(object):
    counter = 0

    def __init__(self):
        self.map = Map()

    async def run(self):
        while True:
            self.counter += 1
            await asyncio.sleep(1)
            print('WORLD: counter={}'.format(self.counter))