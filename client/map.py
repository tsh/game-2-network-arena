import os

import pygame
from pygame.locals import Color

class Map:
    def __init__(self):
        self.map = []
        self.TILE_SIZE = 64
        self.MAX_TILES_HORIZ = 0
        self.MAX_TILES_VERT = 0

        self.tile_sprite = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'tiles', 'grass.png'))
        self.tile_sprite.convert()

    def initialize(self, map_array):
        self.map = map_array
        self.MAX_TILES_HORIZ = len(self.map[0]) +2
        self.MAX_TILES_VERT = len(self.map) +2

    def render(self, window_srf):
        map_srf = pygame.Surface((self.TILE_SIZE * self.MAX_TILES_HORIZ, self.TILE_SIZE * self.MAX_TILES_VERT))
        map_srf.fill((255, 255, 255))
        for i, row in enumerate(self.map):
            for j, tile in enumerate(row):
                if tile == 1:
                    obj = self.tile_sprite
                    map_srf.blit(obj, (j * self.TILE_SIZE, i * self.TILE_SIZE))
                else:
                    r = pygame.Rect(i * self.TILE_SIZE, j * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    map_srf.fill(Color('blue'), r)
                window_srf.blit(map_srf, (0, 0))
                pygame.display.flip()