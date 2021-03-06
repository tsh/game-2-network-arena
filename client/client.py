import sys
import os
import queue
import time
import threading
import socket
import selectors
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
            received += self._sock.recv(2048)
            pos = received.find(b'\n')
            if pos >= 0:
                msg = received[:pos]
                received = received[pos+1:]
                self.queue.put(json.loads(msg))
            print('RCVD ', time.ctime())
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
    RUN = True

    def __init__(self):
        self.sender = Sender()
        self.sender_thread = threading.Thread(target=self.sender.run, name='sender_thread', daemon=True)
        self.sender_thread.start()
        pygame.init()
        # Set up the window
        self.window_surface = pygame.display.set_mode((800, 800), 0, 32)
        pygame.display.set_caption('Hello World')

        self.map = Map()
        self.character = Character()

        server_address = ('127.0.0.1', 8888)
        print('connecting to {} port {}'.format(*server_address))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(server_address)
        self.sock.setblocking(False)
        self.mysel = selectors.DefaultSelector()
        self.mysel.register(
            self.sock,
            selectors.EVENT_READ | selectors.EVENT_WRITE,
        )
        self.received_msg = []
        self.outgoing_msg = []

    def incoming_messages(self):
        for key, mask in self.mysel.select(timeout=0):
            connection = key.fileobj
            if mask & selectors.EVENT_READ:
                data = connection.recv(1024)
                while data:
                    pos = data.find(b'\n')
                    if pos >= 0:
                        msg = data[:pos]
                        data = data[pos+1:]
                        self.received_msg.append(json.loads(msg))

    def run(self):
        clock = pygame.time.Clock()
        while self.RUN:
            clock.tick(60)
            self.incoming_messages()

            try:
                msg = self.received_msg.pop(0)
            except IndexError:
                pass
            else:
                if msg.get('map'):
                    self.map.initialize(msg['map'])
                elif msg.get('character'):
                    self.character.move(msg)


            try:
                msg = self.outgoing_msg.pop(0)
            except IndexError:
                pass
            else:
                self.sock.sendall(json.dumps(msg).encode())

            self.map.render(self.window_surface)
            self.character.render(self.window_surface)
            pygame.display.flip()

            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_w]:
                print('SEND: ', time.time())
                # self.sender.send({'move': 10})
                self.outgoing_msg.append({'move': 10})

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.RUN = False
                    pygame.quit()



class BaseClient(object):
    pass


if __name__ == '__main__':
    Game().run()
