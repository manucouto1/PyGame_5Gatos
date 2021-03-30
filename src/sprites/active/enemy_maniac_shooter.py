import math
import random
import time

import numpy as np

from src.sprites.active.enemy_turret_shooter import EnemyTurretShooter
from src.sprites.passive.event import ExtraLife


class Maniac(EnemyTurretShooter):
    def damage_effect(self, its_hit):
        left = its_hit.rect.left > self.rect.left
        right = its_hit.rect.left < self.rect.left

        if left:
            self.move_right()
        elif right:
            self.move_left()
        else:
            random.choice([self.move_right, self.move_left])()

        self.getting_damage = True
        self.damage_time = time.time()
        self.jump()
        self.num_jumps = 0

    def move(self, hero, dt):
        distance = self.calc_distance(hero)
        self.dt_count += dt

        if distance < 300:
            if self.shots < 3 and len(self.e_bullets.sprites()) < 5:
                if self.dt_count >= self.wait_time:
                    self.wait_time = 450 / 5
                    self.dt_count = 0
                    for i in np.arange(0, 2 * math.pi, math.pi / 8):
                        x = math.cos(i) * 100
                        y = math.sin(i) * 100
                        print(i, x, y)
                        bullet = self.shoot((self.rect.x + x, self.rect.y + y))
                        self.e_bullets.add(bullet)
                        self.shots += 1
            else:
                self.wait_time = 14400 / 5
                self.shots = 0
        else:
            self.wait_time = 450 / 5

    def update(self, hero, zone_events, platforms, dt):
        if self.getting_damage:
            right = self.rect.left > hero.rect.left
            left = self.rect.left < hero.rect.right
            if left:
                self.move_right()
            elif right:
                self.move_left()
            self.jump()

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
