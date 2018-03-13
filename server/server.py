
import asyncio

class BaseServer(object):
    def __init__(self):
        print('Hello init')

    async def run(self, reader, writer):
        print('async world')
        while True:
            print('Test')


async def client_handler():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    while True:
        data = await reader.read(100)
        print('Client Received: %r' % data.decode())


async def server_handler(reader, writer):
    print('Got connection from: {}'.format(writer.get_extra_info('peername')))
    while True:
        writer.write(b'Hello')
        await writer.drain()
        await asyncio.sleep(2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(server_handler, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(coro)
    loop.run_until_complete(client_handler())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
