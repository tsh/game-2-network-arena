import asyncio
from server import BaseServer
from client import BaseClient


async def tcp_echo_client(loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)
    message = 'Hello from client'
    print('Client Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print('Client Received: %r' % data.decode())

    print('Client Close the socket')
    writer.close()


async def handle_echo(reader, writer):
    print('run server')
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Server Received %r from %r" % (message, addr))

    print("Server Send: %r" % message)
    writer.write(data)
    await writer.drain()

    print("Close the client socket")
    writer.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
    server = loop.run_until_complete(coro)
    loop.run_until_complete(tcp_echo_client(loop))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()