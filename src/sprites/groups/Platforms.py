import numpy as np
import pygame as pg


class Platforms:
    def __init__(self, platforms):
        self.sprites = dict()
        self.sprites['actives'] = platforms
        self.sprites['freezes'] = []

    def get_actives(self):
        return self.sprites['actives']

    def get_freezes(self):
        return self.sprites['freezes']

    @staticmethod
    def calc_distance(sprite, target):
        a = (sprite.rect.x - abs(target[0])) ** 2
        b = (sprite.rect.y - abs(target[1])) ** 2

        return np.sqrt(a + b)

    def update(self, target):
        actives = self.sprites['actives']
        freezes = self.sprites['freezes']

        for sprite in actives:
            distance = self.calc_distance(sprite, target.camera_rect)
            if distance > 1132:
                self.sprites['actives'].remove(sprite)
                self.sprites['freezes'].append(sprite)

        for sprite in freezes:
            distance = self.calc_distance(sprite, target.camera_rect)
            if distance < 1132:
                self.sprites['actives'].append(sprite)
                self.sprites['freezes'].remove(sprite)



