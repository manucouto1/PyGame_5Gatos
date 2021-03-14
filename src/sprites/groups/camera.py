import pygame as pg
from src.sprites.groups.custom import CustomGroup


class Camera(CustomGroup):
    def __init__(self, target, world_size, screen_size):
        self.cam = pg.Vector2(0, 0)
        CustomGroup.__init__(self, self.cam, target)

        self.target = target
        self.world_size = world_size
        self.screen_size = screen_size

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + self.screen_size.width / 2
            y = -self.target.rect.center[1] + self.screen_size.height / 2
            self.cam += ((pg.Vector2((x, y)) - self.cam) * 0.5)
            self.cam.x = max(-(self.world_size.width - self.screen_size.width), min(0, round(self.cam.x)))
            self.cam.y = max(-(self.world_size.height - self.screen_size.height), min(0, round(self.cam.y)))
