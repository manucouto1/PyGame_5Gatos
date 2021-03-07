import pygame as pg
from src.sprites.active.active_entity import ActiveEntity

GRAVITY = pg.Vector2((0, 4.8))


class Enemy(ActiveEntity):

    def __init__(self, width, height, offset, frames, *groups):
        super().__init__(width, height, offset, frames, *groups)
        self.path = [0, 100]
        self.walk_count = 0
        self.jump()

    def move(self):
        if self.vel.x > 0:
            if self.rect[0] < self.path[1] + self.vel.x:
                self.move_right()
            else:
                self.move_left()
        else:
            if self.rect[0] > self.path[0] - self.vel.x:
                self.move_left()
            else:
                self.move_right()

    def kill(self):
        self.path[1] = 4000

    def update(self, platforms):
        self.move()
        self.walk_loop()
        self.apply(platforms)
