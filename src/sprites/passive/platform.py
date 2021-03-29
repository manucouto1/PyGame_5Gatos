import time

import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, sheet, tile_size, plat_dto, *groups):
        super().__init__(*groups)

        column = plat_dto.id % 8
        row = plat_dto.id // 8

        self.rect = pg.Rect(column * tile_size, row * tile_size, tile_size, tile_size)
        self.image = sheet.image_at(self.rect)
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = plat_dto.x * tile_size
        self.rect.y = plat_dto.y * tile_size
        self.tile_size = tile_size

    def update(self, *args):
        pass


class FallingPlatform(Platform):
    def __init__(self, sheet, tile_size, plat_dto, *groups):
        super().__init__(sheet, tile_size, plat_dto, *groups)
        self.row = self.rect.y // 32
        self.col = self.rect.x // 32

        self.time_to_fall = None
        self.falling = None
        self.last_level = None
        self.forth = True
        self.shake_period = 10
        self.last_shake = 0
        self.vel = pg.Vector2((0, 0))

    def update(self, dt, collided=False):
        if self.time_to_fall is None:
            if collided:
                self.time_to_fall = time.time()
        else:
            now = time.time()
            if self.time_to_fall + 3 > now:
                self.shake(dt)
            else:
                self.falling = time.time()
                self.rect.y += 5

        if self.falling is not None and time.time() - self.falling > 10:
            self.kill()

    def set_world_size(self, world_size):
        w, h = world_size
        w = w // self.tile_size
        h = h // self.tile_size
        self.time_to_fall = ((h - self.row) * w * 100) + (self.col * 100)

    def shake(self, dt):
        self.last_shake += dt
        if self.last_shake > self.shake_period:
            self.last_shake = 0
            mov = 5 if self.forth else -5
            self.forth = not self.forth
            self.rect.x += mov
