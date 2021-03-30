import pygame as pg

from src.sprites.spritesheet import SpriteStripAnim
from src.utils import assets


class PointAnim(pg.sprite.Sprite):
    def __init__(self, container, point_y):
        super().__init__()
        path = assets.path_to("characters", "enemy", "enemy_full.png")
        sheet = container.image_from_path(path)
        self.sheet = SpriteStripAnim(sheet, (0, 0, 32, 32), 8, rows=4)
        self.sheet[3].set_frames_skip(2)
        self.image = self.sheet[3].next(0)
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        game = container.get_object('game')
        self.rect.x = game.screen_width - 64 - 4
        self.rect.y = point_y
        self.running = False
        self.begin = False

    def run_animation(self):
        self.sheet.reset()

    def update(self, dt):
        self.image = self.sheet[3].roll_once(dt)
        self.image = pg.transform.scale(self.image, (64, 64))
