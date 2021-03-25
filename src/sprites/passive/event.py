from pygame.sprite import Sprite
import pygame as pg


class Event(Sprite):

    def __init__(self, observer, *groups):

        self.event = ''
        self.observer = observer
        super().__init__(*groups)

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
        self.event = "Level end"
        self.image = sheet.image_at((0, 0, 32, 32))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = event_dto.pos

    def kill(self):
        Event.kill(self)
        self.observer.next_level()
        Sprite.kill(self)
