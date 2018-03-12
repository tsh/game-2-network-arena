
import asyncio

class BaseServer(object):
    def __init__(self):
        print('Hello init')

    async def run(self, reader, writer):
        print('async world')
        while True:
            print('Test')

async def test(reader, writer):
    print(writer)
    await asyncio.sleep(0.2)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    server_coro = loop.create_server(test, 'localhost', 8000)
    server = loop.run_until_complete(server_coro)
    print(server)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print('closing')
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
