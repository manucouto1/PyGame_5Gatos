import time
import numpy as np
import pygame as pg
from src.sprites.active.shooter_entity import ShooterEntity
from src.sprites.passive.event import ExtraLife


class EnemyTurretShooter(ShooterEntity):
    def __init__(self, container, entity, *groups):
        ShooterEntity.__init__(self, container, entity, *groups)
        self.last_hit = time.time()
        self.container = container
        self.e_bullets = container.get_object('e_bullets')
        self.walk_count = 0
        self.life = 2
        self.dead_id = 0
        self.dt_count = 0
        self.wait_time = 900/5
        self.shots = 0

        self.sheet[0].set_frames_skip(2)
        self.sheet[1].set_frames_skip(2)
        self.sheet[2].set_frames_skip(2)
        self.sheet[3].set_frames_skip(2)

    def calc_distance(self, hero):
        a = (self.rect.x - hero.rect.x) ** 2
        b = (self.rect.y - hero.rect.y) ** 2

        return np.sqrt(a + b)

    def walk_loop(self, dt):
        if self.direction == pg.K_LEFT:
            self.image = self.sheet[1].next(dt)
        elif self.direction == pg.K_RIGHT:
            self.image = self.sheet[2].next(dt)

    def move(self, hero, dt):
        distance = self.calc_distance(hero)
        self.dt_count += dt

        if distance < 300:
            if self.shots < 3 and len(self.e_bullets.sprites()) < 5:
                if self.dt_count >= self.wait_time:
                    self.wait_time = 450 / 5
                    self.dt_count = 0
                    if self.onGround:
                        bullet = self.shoot((hero.rect.x, hero.rect.y))
                        self.e_bullets.add(bullet)
                        self.shots += 1
            else:
                self.wait_time = 14400 / 5
                self.shots = 0
        else:
            self.wait_time = 450 / 5

    def dead_loop(self, dt):
        self.image = self.sheet[3].next(dt)
        self.mask = self.sheet.get_mask()

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

    def update(self, hero, zone_events, platforms, dt, gravity=pg.Vector2((0, 3.8))):
        if not self.getting_damage:
            self.reset_movement()
        else:
            new_time = time.time()
            if self.damage_time + 1 < new_time:
                self.getting_damage = False
                self.reset_movement()

        if self.life > 0:
            if self.movement:
                self.walk_loop(dt)
            else:
                self.idle_loop(dt)
            self.move(hero, dt)
            self.apply(platforms, dt)
        else:
            self.vel.x = 0
            zone_events.add(ExtraLife(hero, (self.rect.x, self.rect.y)))
            self.kill()


