from  spritesheet import Spritesheet
from platforms import Platform

import pygame as pg
import os

class Layer():

    def __init__(self, name, level_name, positions, tile_size):
        self.name = name
        self.plataforms_group = pg.sprite.Group()

        for position in positions:
            self.plataforms_group.add(Platform(level_name, tile_size, position["x"], position["y"], position["id"]))

    def update(self):
        self.plataforms_group.update()

    def draw(self, screen):
        self.plataforms_group.draw(screen)