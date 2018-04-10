import sys
import os
import queue
import time
import threading
import socket
import json

import pygame
from pygame.locals import *


class ThreadReader:
    def __init__(self, queue: queue.Queue):
        self.queue = queue
        self.active = True
        self.sock = socket.socket()
        self.sock.connect(('127.0.0.1', 8888))

    def run(self):
        while self.active:
            self.queue.put(json.loads(self.sock.recv(4096)))
            time.sleep(1)


class Game(object):
    def __init__(self):
        self.queue = queue.Queue()
        self.tr = ThreadReader(self.queue)
        self.thread = threading.Thread(target=self.tr.run)
        self.thread.start()
        pygame.init()
        #Set up the window
        self.window_surface = pygame.display.set_mode((800, 800), 0, 32)
        pygame.display.set_caption('Hello World')

        self.map = []
        self.map_tile_size = 64
        self.tile_sprite = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'tiles', 'grass.png'))
        self.tile_sprite.convert()

    def render(self, window_srf):
        map_srf = pygame.Surface((self.map_tile_size*4, self.map_tile_size*3))
        map_srf.fill((255, 255, 255))
        for i, row in enumerate(self.map):
            for j, tile in enumerate(row):
                if tile == 1:
                    obj = self.tile_sprite
                    map_srf.blit(obj, (j*self.map_tile_size, i*self.map_tile_size))
                else:
                    r = pygame.Rect(i*self.map_tile_size, j*self.map_tile_size, self.map_tile_size, self.map_tile_size)
                    map_srf.fill(Color('blue'), r)
        window_srf.blit(map_srf, (0, 0))
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            try:
                msg = self.queue.get_nowait()
                if msg.get('map'):
                    self.map = msg['map']
            except queue.Empty:
                pass
            else:
                print(msg)

            self.render(self.window_surface)

            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_w]:
                print('K_w')

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.tr.active = False
                    self.thread.join()
                    sys.exit()
        # pygame.display.update()
        sys.exit()


class BaseClient(object):
    pass


if __name__ == '__main__':
    Game().run()
