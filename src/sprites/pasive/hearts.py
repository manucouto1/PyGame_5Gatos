import pygame as pg


class Heart(pg.sprite.Sprite):
    # state represents init frame of the heart:
    #   - 0: full heart
    #   - 1: half-Heart
    #   - 2: empty heart
    def __init__(self, sheet, state):
        super().__init__()
        self.size = 160
        self.sheet = sheet
        self.image = sheet.image_at((0, 0, self.size, self.size))
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.heart_id = 10 * state
        self.animation = 10
        self.decreasing = False

    def update(self):
        if self.decreasing:
            self.heart_id = self.heart_id + 1
            if self.heart_id % self.animation == 0:
                self.decreasing = False
        self.image = self.sheet.image_at((self.heart_id * self.size, 0, self.size, self.size))
        self.image = pg.transform.scale(self.image, (50, 50))

    def decrease(self):
        print("Hit decrease")
        self.decreasing = True

    def draw(self, win, x, y):
        win.blit(self.image, (x, y))
