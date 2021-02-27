import pygame as pg

import assets
from spritesheet import Spritesheet
import os


class Platform(pg.sprite.Sprite):
    def __init__(self, level_name, tile_size, x, y, pos_id, *groups):
        super().__init__(*groups)

        self.sheet = Spritesheet(assets.path_to(level_name, f"{level_name}.png"))

        column = pos_id % 8
        row = pos_id // 8

        self.rect = pg.Rect(column * tile_size, row * tile_size, tile_size, tile_size)
        self.image = self.sheet.image_at(self.rect)
        self.rect.x = x * tile_size
        self.rect.y = y * tile_size
