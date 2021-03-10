import pygame as pg
from src.sprites.active.active_entity import ActiveEntity
import src.utils.assets as assets
GRAVITY = pg.Vector2((0, 2.8))


class Enemy(ActiveEntity):

    def __init__(self, file, width, height, offset, frames, *groups):
        path = assets.path_to("characters", "enemy", file)
        super().__init__(path, width, height, offset, frames, *groups)
        self.path = [20*32, 20*32 + 100]
        self.walk_count = 0
        self.life = 2
        self.dead_id = 0
        self.rect.x = 20*32
        self.rect.y = 10*32

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

    def dead_loop(self):
        self.idle_id = (self.idle_id + 1) % self.frames
        offset_x = self.idle_id * (self.width + self.offset * 2) + self.offset
        self.image = self.sheet.image_at((offset_x, 96, self.width, self.height))

    def update(self, platforms):
        if self.life > 0:
            self.move()
            self.walk_loop()
            self.apply(platforms)
        else:
            self.vel.x = 0
            self.dead_loop()
            self.apply(platforms)

    def is_hit(self):
        # TODO ver como implementar daño en enemigo
        self.life -= 1
