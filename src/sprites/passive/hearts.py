import pygame as pg


class Heart(pg.sprite.Sprite):
    SIZE = 50

    def __init__(self, sheet, state):
        super().__init__()
        self.orig_size = 160
        self.sheet = sheet
        self.image = sheet.image_at((0, 0, self.orig_size, self.orig_size))
        self.image = pg.transform.scale(self.image, (Heart.SIZE, Heart.SIZE))
        self.rect = self.image.get_rect()
        self.heart_id = 10 * state
        self.animation = 10
        self.decreasing = False

    def update(self):
        if self.decreasing:
            self.heart_id = self.heart_id + 1
            if self.heart_id % self.animation == 0:
                self.decreasing = False
        self.image = self.sheet.image_at((self.heart_id * self.orig_size, 0, self.orig_size, self.orig_size))
        self.image = pg.transform.scale(self.image, (Heart.SIZE, Heart.SIZE))

    def decrease(self):
        self.decreasing = True
