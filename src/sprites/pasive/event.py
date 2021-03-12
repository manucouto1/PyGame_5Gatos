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

    def __init__(self, observer, *groups):
        super().__init__(observer, *groups)
        self.event = "Got pow up"
        self.image = pg.Surface((int(15), int(15)))

        self.color = 255, 0, 0
        self.rect = pg.Rect(200, 400, 10, 10)

    def kill(self):
        Event.kill(self)
        Sprite.kill(self)
