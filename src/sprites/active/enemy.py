import pygame as pg

from src.sprites.spritesheet import SpriteStripAnim
from src.sprites.active.active_entity import ActiveEntity
import src.utils.assets as assets

GRAVITY = pg.Vector2((0, 2.8))


class Enemy(ActiveEntity):
    def __init__(self, container, entity, *groups):
        super().__init__(container, entity, *groups)
        self.walk_count = 0
        self.life = 2
        self.dead_id = 0

        self.sheet[0].set_frames_skip(2)
        self.sheet[1].set_frames_skip(2)
        self.sheet[2].set_frames_skip(2)
        self.sheet[3].set_frames_skip(2)

    def move(self):
        raise NotImplementedError

    def dead_loop(self, dt):
        self.image = self.sheet[3].next(dt)

    def update(self, platforms, dt):
        if self.life > 0:
            self.move()
            self.walk_loop(dt)
            self.apply(platforms, dt)
        else:
            self.vel.x = 0
            self.dead_loop(dt)
            self.apply(platforms, dt)

    def is_hit(self):
        self.life -= 1
