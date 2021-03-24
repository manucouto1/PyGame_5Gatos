import pygame as pg
from src.sprites.groups.scroll_adjusted import ScrollAdjustedGroup


class CameraBuilder:
    def __init__(self, level_dto, screen_size):
        self.world_size = pg.Rect(0, 0, level_dto.map_width * 32, level_dto.map_height * 32)
        self.screen_size = screen_size

    def build(self, hero):
        return Camera(hero, self)


class Camera(ScrollAdjustedGroup):
    def __init__(self, target, builder: CameraBuilder):
        self.scroll = pg.Vector2(0, 0)
        ScrollAdjustedGroup.__init__(self, self.scroll, target)

        self.target = target
        self.world_size = builder.world_size
        self.screen_size = builder.screen_size

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + self.screen_size.width / 2
            y = -self.target.rect.center[1] + self.screen_size.height / 2
            self.scroll += ((pg.Vector2((x, y)) - self.scroll) * 0.5)
            self.scroll.x = max(-(self.world_size.width - self.screen_size.width), min(0, round(self.scroll.x)))
            self.scroll.y = max(-(self.world_size.height - self.screen_size.height), min(0, round(self.scroll.y)))
