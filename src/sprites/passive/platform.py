import time
import pygame as pg

# Time fo the platform to
FALL = 3
VANISH = 10
# Fall speed
GRAVITY = 5


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


class FallingPlatform(Platform):
    def __init__(self, sheet, tile_size, plat_dto, *groups):
        super().__init__(sheet, tile_size, plat_dto, *groups)
        self.row = self.rect.y // 32
        self.col = self.rect.x // 32

        self.stepped_at = None
        self.falling_at = None
        self.last_level = None
        self.forth = True

    def update(self, collided=False):
        if self.stepped_at is None:
            if collided:
                self.stepped_at = time.time()
        else:
            now = time.time()
            if self.stepped_at + FALL > now:
                self.shake()
            else:
                self.falling_at = time.time()
                self.rect.y += GRAVITY

        if self.falling_at is not None and time.time() - self.falling_at > VANISH:
            self.kill()

    def shake(self):
        mov = 5 if self.forth else -5
        self.forth = not self.forth
        self.rect.x += mov
