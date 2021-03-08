import pygame as pg
from src.sprites.pasive.hero import Player

class Heart(pg.sprite.Sprite):
    # state represents init frame of the heart:
    #   - 0: full heart
    #   - 1: half-Heart
    #   - 2: empty heart
    def __init__(self, sheet, state):
        self.size = 32
        self.sheet = sheet
        self.image = sheet.image_at(0, 0, self.size, self.size)
        self.rect = self.image.get_rect()
        self.heart_id = 10 * state
        self.animation = 10
        self.down_healing = False

    def update(self, player):
        if(self.down_healing):
            self.heart_id = self.heart_id + 1
            if(self.heart_id % self.animation == 0):
                self.down_healing = False
        self.image = self.sheet.image_at(self.heart_id * self.size, 0, self.size, self.size)

    def decrease(self):
        self.down_healing = True