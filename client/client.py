import sys
import os
import queue
import time
import threading
import socket
import json

import pygame
from pygame.locals import *

from map import Map


class ThreadReader:
    def __init__(self, queue: queue.Queue):
        self.queue = queue
        self.active = True
        self.sock = socket.socket()
        self.sock.connect(('127.0.0.1', 8888))

    def run(self):
        received = b''
        while self.active:
            received += self.sock.recv(4096)
            pos = received.find(b'\n')
            if pos >= 0:
                msg = received[:pos]
                received = received[pos+1:]
                self.queue.put(json.loads(msg))
            time.sleep(1)


class Game(object):
    def __init__(self):
        self.queue = queue.Queue()
        self.tr = ThreadReader(self.queue)
        self.thread = threading.Thread(target=self.tr.run)
        self.thread.start()
        pygame.init()
        # Set up the window
        self.window_surface = pygame.display.set_mode((800, 800), 0, 32)
        pygame.display.set_caption('Hello World')

        self.map = Map()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            try:
                msg = self.queue.get_nowait()
                if msg.get('map'):
                    self.map.initialize(msg['map'])
            except queue.Empty:
                pass
            else:
                print(msg)

            self.map.render(self.window_surface)

            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_w]:
                print('K_w')

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.tr.active = False
                    self.thread.join()
                    sys.exit()
        sys.exit()


class BaseClient(object):
    pass


if __name__ == '__main__':
    Game().run()
