import asyncio
import json

from world import GameWorld

ADDRESS = '127.0.0.1'
PORT = 8888

class Server:
    connections = []

    def __init__(self):
        self.world = GameWorld()
        self.notify = True
        self.notify_delay = 2  # sec

    async def tick(self):
        await self.world.run()

    async def notify_clients(self):
        while self.notify:
            for con in self.connections:
                try:
                    await con.send({'tick': self.world.counter})
                except ConnectionResetError:
                    self.connections.remove(con)
            await asyncio.sleep(self.notify_delay)

    async def client_connected(self, reader, writer):
        print('Server: Got connection from: {}'.format(writer.get_extra_info('peername')))
        con = Connection(reader, writer)
        await con.send({'map': self.world.map.serialize()})
        self.connections.append(con)


class Connection:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def send(self, msg: dict):
        self.writer.write(json.dumps(msg).encode())
        await self.writer.drain()


if __name__ == '__main__':
    my_server = Server()
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(my_server.client_connected, ADDRESS, PORT)
    server = loop.run_until_complete(coro)
    asyncio.async(my_server.tick())
    asyncio.async(my_server.notify_clients())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
