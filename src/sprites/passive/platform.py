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

    def update(self, *args):
        pass


class FallingPlatform(Platform):
    def __init__(self, sheet, tile_size, plat_dto, *groups):
        super().__init__(sheet, tile_size, plat_dto, *groups)
        self.time_to_shake = self.rect.x
        self.limit_speed = 1
        self.last_level = None
        self.forth = True
        self.shake_period = 50
        self.last_shake = 0
        self.vel = pg.Vector2((0, 0))

    def update(self, limit_level):
        limit_dt = 0 if self.last_level is None else self.last_level - limit_level
        if self.rect.y > limit_level:
            if self.time_to_shake > 0:
                self.time_to_shake -= limit_dt
                self.shake(limit_dt)
            else:
                self.rect.y += 5
                pass

        self.last_level = limit_level

    def shake(self, dt):
        self.last_shake += dt
        if self.last_shake > self.shake_period:
            self.last_shake = 0
            mov = 5 if self.forth else -5
            self.forth = not self.forth
            self.rect.x += mov
