import pygame as pg
from  spritesheet import Spritesheet
import os

class Platform(pg.sprite.Sprite):

    def __init__(self, level_name, tile_size, x, y, id, *groups):
        super().__init__(*groups)

        self.sheet = Spritesheet("assets"+os.sep+level_name+os.sep+level_name+".png")

        column = id % 8
        row = id // 8

        self.rect = pg.Rect(column*tile_size, row*tile_size, tile_size, tile_size)
        self.image = self.sheet.image_at(self.rect)
        self.rect.x = x*tile_size
        self.rect.y = y*tile_size