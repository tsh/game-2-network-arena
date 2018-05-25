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
from objects import Character


class ServerConnection:
    _sock = None

    def __init__(self):
        if ServerConnection._sock is None:
            ServerConnection._sock = socket.socket()
            ServerConnection._sock.connect(('127.0.0.1', 8888))


class Receiver(ServerConnection):
    def __init__(self, queue: queue.Queue):
        super().__init__()
        self.queue = queue
        self.active = True

    def run(self):
        received = b''
        while self.active:
            received += self._sock.recv(4096)
            pos = received.find(b'\n')
            if pos >= 0:
                msg = received[:pos]
                received = received[pos+1:]
                self.queue.put(json.loads(msg))
            time.sleep(1)


class Sender(ServerConnection):
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.active = True

    def send(self, msg: dict):
        self.queue.put_nowait(msg)

    def run(self):
        while self.active:
            to_send = self.queue.get()  # will block on exit
            msg = json.dumps(to_send)
            self._sock.send(msg.encode())


class Game(object):
    def __init__(self):
        self.queue = queue.Queue()
        self.receiver = Receiver(self.queue)
        self.receiver_thread = threading.Thread(target=self.receiver.run, name='receiver_thread')
        self.receiver_thread.start()
        self.sender = Sender()
        self.sender_thread = threading.Thread(target=self.sender.run, name='sender_thread')
        self.sender_thread.start()
        pygame.init()
        # Set up the window
        self.window_surface = pygame.display.set_mode((800, 800), 0, 32)
        pygame.display.set_caption('Hello World')

        self.map = Map()
        self.character = Character()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            try:
                msg = self.queue.get_nowait()
                print('received', msg)
                if msg.get('map'):
                    self.map.initialize(msg['map'])
                elif msg.get('character'):
                    self.character.move(msg)
            except queue.Empty:
                pass
            else:
                pass

            self.map.render(self.window_surface)
            self.character.render(self.window_surface)
            pygame.display.flip()

            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_w]:
                self.sender.send({'move': 10})

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.receiver.active = False
                    self.sender.active = False
                    self.receiver_thread.join()
                    self.sender_thread.join()
                    sys.exit()
        sys.exit()


class BaseClient(object):
    pass


if __name__ == '__main__':
    Game().run()
