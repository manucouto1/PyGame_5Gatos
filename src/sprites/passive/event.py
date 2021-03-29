from pygame.sprite import Sprite
import pygame as pg

from src.utils import assets


class Event(Sprite):

    def __init__(self, observer, *groups):

        self.event = ''
        self.observer = observer
        super().__init__(*groups)

    def update(self, dt):
        return NotImplemented

    def kill(self):
        self.observer.notify(self.event)


class Item(Event):

    def __init__(self, sheet, event_dto, observer, *groups):
        super().__init__(observer, *groups)
        self.event = "Got pow up"
        self.image = sheet.image_at((0, 0, 32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = event_dto.pos

    def kill(self):
        Event.kill(self)
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
        Event.kill(self)
        self.observer.next_level()
        Sprite.kill(self)


class ExtraLife(Event):
    def __init__(self, hero, pos, *groups):
        super().__init__(hero, *groups)
        self.event = "Extra life"
        self.image = hero.life.sheet.image_at((0, 0, 160, 160))
        self.image = pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos

    def kill(self):
        self.observer.add_life()
        Sprite.kill(self)


class KittyPoint(Event):
    def __init__(self, hero, sheet, pos, *groups):
        super().__init__(hero, *groups)
        self.event = "X1 Point"
        self.sheet = sheet
        self.image = self.sheet.images[self.sheet.row][self.sheet.idx]
        self.image = pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos

    def update(self, dt):
        self.image = self.sheet[3].next(dt)

    def kill(self):
        self.observer.add_point()
        Sprite.kill(self)

