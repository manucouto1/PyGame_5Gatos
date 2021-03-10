import pygame as pg
from src.sprites.active.active_entity import ActiveEntity
import src.utils.assets as assets
GRAVITY = pg.Vector2((0, 4.8))


class Enemy(ActiveEntity):

    def __init__(self, file, width, height, offset, frames, *groups):
        path = assets.path_to("characters", "enemy", file)
        super().__init__(path, width, height, offset, frames, *groups)
        self.path = [0, 100]
        self.walk_count = 0
        self.life = 2

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

    def update(self, platforms):
        if self.life > 0:
            self.move()
            self.walk_loop()
            self.apply(platforms)

    def is_hit(self):
        # TODO ver como implementar daño en enemigo
        self.life -= 1
