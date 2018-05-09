import pygame
from pygame.locals import Color


class Character:
    def __init__(self, msg):
        self.x = 50
        self.y = 50

    def render(self, surface):
        pygame.draw.circle(surface, Color('yellow'), (self.x, self.y), 25)