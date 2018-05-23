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

    @classmethod
    def get_sock(cls):
        if cls._sock is None:
            cls._sock = socket.socket()
            cls._sock.connect(('127.0.0.1', 8888))
        return cls._sock


class Receiver:
    def __init__(self, queue: queue.Queue):
        self.queue = queue
        self.active = True
        self.socket = ServerConnection.get_sock()

    def run(self):
        received = b''
        while self.active:
            received += self.socket.recv(4096)
            pos = received.find(b'\n')
            if pos >= 0:
                msg = received[:pos]
                received = received[pos+1:]
                self.queue.put(json.loads(msg))
            time.sleep(1)


class Sender:
    def __init__(self):
        self.queue = queue.Queue()
        self.active = True
        self.socket = ServerConnection.get_sock()

    def send(self, msg: dict):
        self.queue.put_nowait(msg)

    def run(self):
        while self.active:
            self.socket.send(b'test22')
            time.sleep(1)

class Game(object):
    def __init__(self):
        self.queue = queue.Queue()
        self.receiver = Receiver(self.queue)
        self.thread = threading.Thread(target=self.receiver.run)
        self.thread.start()
        self.sender = Sender()
        self.sender_thread = threading.Thread(target=self.sender.run)
        self.sender_thread.start()
        pygame.init()
        # Set up the window
        self.window_surface = pygame.display.set_mode((800, 800), 0, 32)
        pygame.display.set_caption('Hello World')

        self.map = Map()
        self.characters = []

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
                    self.characters.append(Character(msg))
            except queue.Empty:
                pass
            else:
                pass

            self.map.render(self.window_surface)
            for character in self.characters:
                character.render(self.window_surface)
            pygame.display.flip()

            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_w]:
                print('K_w')

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.receiver.active = False
                    self.thread.join()
                    self.sender_thread.active = False
                    self.sender_thread.join()
                    sys.exit()
        sys.exit()


class BaseClient(object):
    pass


if __name__ == '__main__':
    Game().run()
