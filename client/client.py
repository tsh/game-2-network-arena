import sys
import pygame
from pygame.locals import *


class Game(object):
    def __init__(self):
        pygame.init()
        #Set up the window
        self.windowSurface = pygame.display.set_mode((800, 800), 0, 32)
        pygame.display.set_caption('Hello World')

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_w]:
                print('K_w')

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
        pygame.display.update()
        sys.exit()


class BaseClient(object):
    pass


if __name__ == '__main__':
    Game().run()
