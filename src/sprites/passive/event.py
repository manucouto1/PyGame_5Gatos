from pygame.sprite import Sprite
import pygame as pg

from sprites.passive.hud.hearts import Heart

from src.utils import assets


class Event(Sprite):
    def __init__(self, observer, *groups):
        self.observer = observer
        super().__init__(*groups)

    def update(self, dt):
        return NotImplemented


class Item(Event):
    def __init__(self, sheet, event_dto, observer, *groups):
        super().__init__(observer, *groups)
        self.event = "Got pow up"
        self.image = sheet.image_at((0, 0, 32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = event_dto.pos

    def kill(self):
        Sprite.kill(self)


class EndGame(Event):
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
