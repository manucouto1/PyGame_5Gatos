import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, sheet, tile_size, plat_dto, *groups):
        super().__init__(*groups)

        column = plat_dto.id % 8
        row = plat_dto.id // 8

        self.rect = pg.Rect(column * tile_size, row * tile_size, tile_size, tile_size)
        self.image = sheet.image_at(self.rect)
        self.rect.x = plat_dto.x * tile_size
        self.rect.y = plat_dto.y * tile_size
