
import asyncio

ADDRESS = '127.0.0.1'
PORT = 8888

class Server:
    connections = []

    def __init__(self, world):
        self.world = world

    async def run(self):
        await self.world.run()

    async def connect(self, r, writer):
        print('Server: Got connection from: {}'.format(writer.get_extra_info('peername')))
        while True:
            writer.write(bytes(str(self.world.counter), 'utf8'))
            await writer.drain()
            await asyncio.sleep(2)


class ClassGameWorld(object):
    counter = 0

    async def run(self):
        while True:
            self.counter += 1
            await asyncio.sleep(1)
            print('WORLD: counter={}'.format(self.counter))


async def client_handler():
    reader, writer = await asyncio.open_connection(ADDRESS, PORT)
    while True:
        data = await reader.read(100)
        print('Client Received: %r' % data.decode())


async def server_handler(reader, writer):
    print('Server: Got connection from: {}'.format(writer.get_extra_info('peername')))
    while True:
        writer.write(b'Hello')
        await writer.drain()
        await asyncio.sleep(2)


if __name__ == '__main__':
    world = ClassGameWorld()
    my_server = Server(world)
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(my_server.connect, ADDRESS, PORT)
    server = loop.run_until_complete(coro)
    asyncio.async(my_server.run())
    asyncio.async(client_handler())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
