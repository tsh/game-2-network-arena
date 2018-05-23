import asyncio
import json

from world import GameWorld
from objects import Character

ADDRESS = '127.0.0.1'
PORT = 8888

class GameServer:
    connections = []

    MSG_NOTIFY_DELAY = 2  # sec

    def __init__(self):
        self.world = GameWorld()
        self.notify = True
        self.character = Character()

    async def tick(self):
        await self.world.run()

    async def notify_clients(self):
        while self.notify:
            for con in self.connections:
                con.send({'tick': self.world.counter})
            await asyncio.sleep(self.MSG_NOTIFY_DELAY)

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_connection(self, connection):
        self.connections.remove(connection)


class ClientConnection(asyncio.Protocol):
    game_server = GameServer()

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self.transport = transport
        self.game_server.add_connection(self)
        self.send({'map': self.game_server.world.map.serialize()})
        self.send({'character': self.game_server.character.serialize()})

    def data_received(self, data):
        message = data.decode()
        print('received: ', message)
        self.send({'echo': message})

    def connection_lost(self, exc):
        self.transport.close()
        self.game_server.remove_connection(self)

    def send(self, message: dict):
        self.transport.write(json.dumps(message).encode()+b'\n')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    game_server = GameServer()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(ClientConnection, '127.0.0.1', 8888)
    server = loop.run_until_complete(coro)
    asyncio.async(game_server.tick())
    asyncio.async(game_server.notify_clients())
    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
