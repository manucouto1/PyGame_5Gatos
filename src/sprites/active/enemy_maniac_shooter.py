import random
import time

from src.sprites.active.enemy_turret_shooter import EnemyTurretShooter
from src.sprites.passive.event import ExtraLife, ManiacMode


class Maniac(EnemyTurretShooter):

    def __init__(self, container, entity, *groups):
        super().__init__(container, entity, *groups)
        self.maniac = True
        self.maniac_time = 0.25

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
        if distance < 300:
            if time.time() - self.maniac_init > 2:
                self.maniac_init = time.time()
                self.maniac = True

            self.shoot_maniac(self.e_bullets)

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
            zone_events.add(ManiacMode(hero, self.rect.bottomleft))
            self.kill()
