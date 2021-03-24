import pygame as pg

from src.sprites.active.shutter_entity import ShutterEntity
from src.sprites.pasive.life import Life
import time


class HeroBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        self.entity_dto = level_dto.hero

    def build(self, player):
        return Hero(player, self)


class Hero(ShutterEntity):
    def __init__(self, player, builder: HeroBuilder):
        super().__init__(builder.container, builder.entity_dto)
        self.last_hit = time.time()
        self.life = Life(builder.container, 3, player)

    def walk_loop(self, dt):
        if self.direction == pg.K_LEFT:
            self.image = self.sheet[1].next(dt)
        elif self.direction == pg.K_RIGHT:
            self.image = self.sheet[2].next(dt)

    def is_hit(self, dangerous):
        collide_l = pg.sprite.spritecollideany(self, dangerous)
        if collide_l:
            new_hit = time.time()
            if self.last_hit + 2 < new_hit:
                self.last_hit = new_hit
                self.life.decrease()

    def update(self, platforms, _, dt):
        if self.movement:
            self.walk_loop(dt)
        else:
            self.idle_loop(dt)
        self.life.update()
        self.apply(platforms, dt)
        self.reset_movement()
