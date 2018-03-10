

class BaseServer(object):
    def __init__(self):
        print('Hello init')

    async def run(self):
        print('async world')

if __name__ == '__main__':
    print('hello')
    srv = BaseServer()
    srv.run()
