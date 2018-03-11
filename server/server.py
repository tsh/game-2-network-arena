
import asyncio

class BaseServer(object):
    def __init__(self):
        print('Hello init')

    async def run(self, reader, writer):
        print('async world')
        while True:
            print('Test')
if __name__ == '__main__':
    print('hello')
    srv = BaseServer()
    event_loop = asyncio.get_event_loop()
    factory = asyncio.start_server(srv.run, 'localhost', 8000)
    server = event_loop.run_until_complete(factory)
    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        event_loop.close()
