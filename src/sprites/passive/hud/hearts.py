import pygame as pg

DECREASE = 0
INCREASE = 1


class Heart(pg.sprite.Sprite):
    SIZE = 50

    def __init__(self, sheet, state):
        super().__init__()
        self.sheet = sheet
        self.image = sheet.image_at((0, 0, Heart.SIZE, Heart.SIZE))
        self.rect = self.image.get_rect()
        self.heart_id = 10 * state
        self.animation = 10
        self.decreasing = False
        self.increasing = False
        self.queue = []

    def update(self):
        if self.decreasing:
            self.heart_id = self.heart_id + 1
            if self.heart_id % self.animation == 0:
                self.decreasing = False
        elif self.increasing:
            self.heart_id = self.heart_id - 1
            if self.heart_id % self.animation == 0:
                self.increasing = False
        else:
            if len(self.queue) > 0:
                action = self.queue.pop(0)
                if action == 0:
                    self.decreasing = True
                elif action == 1:
                    self.increasing = True

        self.image = self.sheet.image_at((self.heart_id * Heart.SIZE, 0, Heart.SIZE, Heart.SIZE))

    def decrease(self):
        #self.decreasing = True
        self.queue.append(DECREASE)

    def increase(self):
        #self.increasing = True
        self.queue.append(INCREASE)
