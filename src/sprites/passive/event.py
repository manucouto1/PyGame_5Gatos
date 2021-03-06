import numpy as np
from pygame.sprite import Sprite
from src.sprites.passive.hud.hearts import Heart
from src.utils import assets
import pygame as pg


class Event(Sprite):
    def __init__(self, observer, *groups):
        self.observer = observer
        super().__init__(*groups)

    def _calc_distance(self, sprite, target):
        a = (sprite.rect.x - abs(target[0])) ** 2
        b = (sprite.rect.y - abs(target[1])) ** 2
        return np.sqrt(a + b)

    def follow(self, hero):
        y = hero.rect.center[1] - self.rect.center[1]
        x = hero.rect.center[0] - self.rect.center[0]
        self.rect.y += y * 0.1
        self.rect.x += x * 0.1

    def update(self, dt):
        return NotImplemented


class EndLevel(Event):
    def __init__(self, sheet, event_dto, observer, *groups):
        super().__init__(observer, *groups)
        column = event_dto.id % 8
        row = event_dto.id // 8
        self.event = "Level end"
        self.rect = pg.Rect(column * event_dto.scale, row * event_dto.scale, event_dto.scale, event_dto.scale)
        self.image = sheet.image_at(self.rect)
        self.rect.bottomleft = event_dto.pos

    def kill(self):
        self.observer.next_level()


class ExtraLife(Event):

    def __init__(self, hero, pos, *groups):
        super().__init__(hero, *groups)
        self.event = "Extra life"
        self.image = hero.life.sheet.image_at((0, 0, Heart.SIZE, Heart.SIZE))
        self.image = pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos

    def kill(self):
        self.observer.add_life()
        Sprite.kill(self)

    def update(self, dt):
        distance = self._calc_distance(self, self.observer.rect)
        if distance < 128:
            self.follow(self.observer)


class KittyPoint(Event):
    def __init__(self, hero, sheet, pos, *groups):
        super().__init__(hero, *groups)
        self.event = "+1 Point"
        self.sheet = sheet
        self.image = self.sheet.next(0)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos

    def update(self, dt):
        self.image = self.sheet[3].next(dt)
        distance = self._calc_distance(self, self.observer.rect)
        if distance < 128:
            self.follow(self.observer)


    def kill(self):
        self.observer.add_point()
        Sprite.kill(self)


class ManiacMode(Event):
    def __init__(self, hero, pos, *groups):
        super().__init__(hero, *groups)
        self.event = "Maniac mode active"
        self.image = assets.load_image("treat.png")
        self.image = pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos

    def kill(self):
        self.observer.activate_maniac()
        Sprite.kill(self)


class EndGame(Event):
    def __init__(self, observer, pos, *groups):
        super().__init__(observer, *groups)
        self.event = "End Game"
        self.image = assets.load_image("foil_hat.png")
        self.image = pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos

    def kill(self):
        self.observer.next_level()
