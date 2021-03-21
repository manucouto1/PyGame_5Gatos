from random import randint, choice

import pygame as pg

from utils import assets


class Arrows(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.pos_left = 300
        self.number = 20
        self.speed = 3
        self.arrow_images = []

        arrow_right = assets.load_image('cursor', 'arrow.png')
        arrow_right.set_colorkey((255, 255, 255), pg.RLEACCEL)
        arrow_right = pg.transform.scale(arrow_right, (30, 30))

        arrow_down = pg.transform.rotate(arrow_right, 90)
        arrow_down.set_colorkey((255, 255, 255), pg.RLEACCEL)

        arrow_left = pg.transform.rotate(arrow_down, 90)
        arrow_left.set_colorkey((255, 255, 255), pg.RLEACCEL)

        arrow_up = pg.transform.rotate(arrow_left, 90)
        arrow_up.set_colorkey((255, 255, 255), pg.RLEACCEL)

        self.arrow_images.append(arrow_right)
        self.arrow_images.append(arrow_down)
        self.arrow_images.append(arrow_left)
        self.arrow_images.append(arrow_up)

        arrow_sprites = []
        for i in range(self.number):
            arrow_sprites.append(self.init_sprite(i))

        self.add(*arrow_sprites)

    def init_sprite(self, i):
        sprite = pg.sprite.Sprite()
        arrow = choice(self.arrow_images)
        sprite.image = arrow
        sprite.rect = pg.Rect(0, 0, 30, 30)
        sprite.rect.bottomleft = self.pos_left, 0 - i * 40

        return sprite

    def update(self):
        for s in self.sprites():
            s.rect.bottom = s.rect.bottom + 1

    def draw(self, surface):
        super().draw(surface)
        # Dibujar marco
