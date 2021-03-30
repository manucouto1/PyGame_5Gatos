import time

import pygame as pg
from src.sprites.active.active_entity import ActiveEntity
from src.sprites.passive.event import KittyPoint


class Enemy(ActiveEntity):
    def __init__(self, container, entity, *groups):
        super().__init__(container, entity, *groups)
        self.walk_count = 0
        self.life = 2
        self.dead_id = 0
        self.last_hit = time.time()

        self.sheet[0].set_frames_skip(2)
        self.sheet[1].set_frames_skip(2)
        self.sheet[2].set_frames_skip(2)
        self.sheet[3].set_frames_skip(2)

    def move(self, dt):
        raise NotImplementedError

    def dead_loop(self, dt):
        self.image = self.sheet[3].next(dt)

    def update(self, hero, zone_events, platforms, dt):
        if self.life > 0:
            self.move(dt)
            self.walk_loop(dt)
            self.apply(platforms, dt)
        else:
            self.vel.x = 0
            zone_events.add(KittyPoint(hero, self.sheet, self.rect.bottomleft))
            self.kill()

    def is_hit(self, dangerous):
        new_hit = time.time()
        if self.last_hit + 0.5 < new_hit:
            self.damage_effect(dangerous[0])
            self.last_hit = new_hit

    def is_shoot(self, bullet):
        self.life -= 1
        if self.life == 0:
            self.damage_effect(bullet)
            self.mixer.play_destroy_enemy()
        else:
            self.damage_effect(bullet)
            self.mixer.play_enemy_hit()
