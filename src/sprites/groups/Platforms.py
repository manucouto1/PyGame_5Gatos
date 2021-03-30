import numpy as np
import pygame as pg


class Platforms:
    def __init__(self, game, platforms):
        self.center_x = game.screen_width/2
        self.center_y = game.screen_height/2
        self.max_distance = np.sqrt(self.center_x ** 2 + self.center_y ** 2)
        self.sprites = dict()
        self.sprites['actives'] = platforms
        self.sprites['freezes'] = []

    def get_actives(self):
        return self.sprites['actives']

    def get_freezes(self):
        return self.sprites['freezes']

    def calc_distance(self, sprite, target):
        a = (sprite.rect.x - abs(target[0] - self.center_x)) ** 2
        b = (sprite.rect.y - abs(target[1] - self.center_y)) ** 2

        return np.sqrt(a + b)

    def update(self, target):
        actives = self.sprites['actives']
        freezes = self.sprites['freezes']

        for sprite in actives:
            distance = self.calc_distance(sprite, target.camera_rect)
            if distance >= self.max_distance:
                self.sprites['actives'].remove(sprite)
                self.sprites['freezes'].append(sprite)

        for sprite in freezes:
            distance = self.calc_distance(sprite, target.camera_rect)
            if distance < self.max_distance:
                self.sprites['actives'].append(sprite)
                self.sprites['freezes'].remove(sprite)



