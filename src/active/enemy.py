import pygame as pg
from src.active.active_entity import ActiveEntity

GRAVITY = pg.Vector2((0, 4.8))


class Enemy(ActiveEntity):

    def __init__(self, width, height, offset, frames, level):
        super().__init__(width, height, offset, frames, level)
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
            else:  # Change direction
                self.move_right()

    def update(self):
        self.move()
        self.walk_loop()

        self.gravity()
        self.rect.x += self.vel.x
        self.collide_ground(self.vel.x, 0)
        self.rect.y += self.vel.y
        self.onGround = False
        self.collide_ground(0, self.vel.y)
