import sys
import queue
import time
import threading
import pygame
from pygame.locals import *


class ThreadReader:
    def __init__(self, queue: queue.Queue):
        self.queue = queue
        self.active = True

    def run(self):
        while self.active:
            self.queue.put('test')
            time.sleep(1)


class Game(object):
    def __init__(self):
        self.queue = queue.Queue()
        self.tr = ThreadReader(self.queue)
        self.thread = threading.Thread(target=self.tr.run)
        self.thread.start()
        pygame.init()
        #Set up the window
        self.windowSurface = pygame.display.set_mode((800, 800), 0, 32)
        pygame.display.set_caption('Hello World')

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            try:
                msg = self.queue.get_nowait()
            except queue.Empty:
                pass
            else:
                print(msg)
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_w]:
                print('K_w')

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.tr.active = False
                    self.thread.join()
                    sys.exit()
        pygame.display.update()
        sys.exit()


class BaseClient(object):
    pass


if __name__ == '__main__':
    Game().run()
