import pygame as pg

from src.sprites.spritesheet import SpriteStripAnim
from src.utils import assets

POINT_Y = 50


class PointAnim(pg.sprite.Sprite):
    def __init__(self, container):
        super().__init__()
        path = assets.path_to("characters", "enemy", "enemy_full.png")
        self.sheet = SpriteStripAnim(container, path, (0, 0, 32, 32), 4, rows=4)
        self.sheet[3].set_frames_skip(2)
        self.image = self.sheet[3].images[self.sheet.row][self.sheet.idx]
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        game = container.get_object('game')
        self.rect.x = game.screen_width - 64 - 4
        self.rect.y = POINT_Y
        self.increasing = False
        self.increasing_count = 0

    def increase(self):
        self.increasing = True
        self.increasing_count = 0
        self.sheet.idx = 0

    def update(self, dt):
        if self.increasing:
            if self.increasing_count < 16:
                self.image = self.sheet.next(dt)
                self.image = pg.transform.scale(self.image, (64, 64))
                self.increasing_count += 1
            else:
                self.increasing_count = 0
                self.increasing = False


