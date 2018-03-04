

class BaseServer(object):
    def __init__(self):
        print('Hello')

    def __call__(self, *args, **kwargs):
        print('World')