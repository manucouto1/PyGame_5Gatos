import pygame as pg
from src.sprites.groups.scroll_adjusted import ScrollAdjustedGroup


class CameraBuilder:
    def __init__(self, container, level_dto, screen_size):
        self.container = container
        self.world_size = pg.Rect(0, 0, level_dto.map_width * 32, level_dto.map_height * 32)
        self.screen_size = screen_size
        self.gaps = level_dto.gaps

    def build(self, hero):
        return self.container.object_from_name(self.gaps.name, hero, self)


class Camera(ScrollAdjustedGroup):
    def __init__(self, target, builder: CameraBuilder):
        self.scroll = pg.Vector2(0, 0)
        ScrollAdjustedGroup.__init__(self, self.scroll, target)
        self.target = target
        self.world_size = builder.world_size
        self.screen_size = builder.screen_size
        x = -self.target.rect.center[0] + self.screen_size.width / 2
        y = -self.target.rect.center[1] + self.screen_size.height / 2
        self.do_scroll(x, y, 1, 1)

    def do_scroll(self, x, y, smooth_x, smooth_y):
        (aux_x, aux_y) = (pg.Vector2((x, y)) - self.scroll)
        self.scroll += pg.Vector2((aux_x*smooth_x, aux_y*smooth_y))
        self.scroll.x = max(-(self.world_size.width - self.screen_size.width), min(0, round(self.scroll.x)))
        self.scroll.y = max(-(self.world_size.height - self.screen_size.height), min(0, round(self.scroll.y)))

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + self.screen_size.width / 2
            y = -self.target.rect.center[1] + self.screen_size.height / 2
            self.do_scroll(x, y, 0.05, 0.01)


class CameraVerticalGap(Camera):
    def __init__(self, target, builder: CameraBuilder):
        super().__init__(target, builder)
        self.gaps_list = builder.gaps.list

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + self.screen_size.width / 2

            for gap in self.gaps_list:
                if gap["end"] > self.target.rect.center[1] > gap["init"]:
                    y = -(gap["init"]+gap['end']/2) + self.screen_size.height / 2
                    self.do_scroll(x, y, 0.05, 0.01)
                    return

            y = -self.target.rect.center[1] + self.screen_size.height / 2
            self.do_scroll(x, y, 0.05, 0.01)

