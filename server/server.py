import asyncio

from world import GameWorld

ADDRESS = '127.0.0.1'
PORT = 8888

class Server:
    connections = []

    def __init__(self):
        self.world = GameWorld()
        self.notify = True
        self.notify_delay = 2  # sec

    async def run(self):
        await self.world.run()

    async def notify_clients(self):
        while self.notify:
            for con in self.connections:
                await con.send(bytes('Servv says: ' + str(self.world.counter), 'utf8'))
            await asyncio.sleep(self.notify_delay)

    async def client_connected(self, reader, writer):
        print('Server: Got connection from: {}'.format(writer.get_extra_info('peername')))
        con = Connection(reader, writer)
        self.connections.append(con)


class Connection:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def send(self, msg):
        self.writer.write(msg)
        await self.writer.drain()


async def client_handler():
    reader, writer = await asyncio.open_connection(ADDRESS, PORT)
    while True:
        data = await reader.read(100)
        print('Client Received: %r' % data.decode())


if __name__ == '__main__':
    my_server = Server()
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(my_server.client_connected, ADDRESS, PORT)
    server = loop.run_until_complete(coro)
    asyncio.async(my_server.run())
    asyncio.async(my_server.notify_clients())
    asyncio.async(client_handler())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
