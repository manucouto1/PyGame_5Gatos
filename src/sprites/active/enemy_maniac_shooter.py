import random
import time

from src.sprites.active.enemy_turret_shooter import EnemyTurretShooter
from src.sprites.passive.event import ExtraLife, ManiacMode
import pygame as pg


class Maniac(EnemyTurretShooter):
    """
    Class implementing the shooting enemies

    :param container: Application container
    :param entity: Enemy map DTO
    """
    def __init__(self, container, entity, *groups):
        super().__init__(container, entity, *groups)
        self.maniac = True
        self.maniac_time = 0.25

    def after_hit_direction(self, hit):
        left = hit.rect.left < self.rect.right
        right = hit.rect.right > self.rect.left

        return left, right

    def shoot_hero(self, target, dt):
        distance = self.calc_distance(target)
        if distance < 300:
            if time.time() - self.maniac_init > 2:
                self.maniac_init = time.time()
                self.maniac = True

            self.shoot_maniac(self.e_bullets)

    def update(self, hero, zone_events, platforms, dt, gravity=pg.Vector2((0, 3.8))):
        if self.getting_damage:
            left = self.rect.left > hero.rect.right + 20
            right = self.rect.right < hero.rect.left - 20
            if left or right:
                self.choose_mov(left, right)

            self.jump()

        # The maniac will keep moving towards target because movement it's not being reset
        if self.life > 0:
            if self.movement:
                self.walk_loop(dt)
            else:
                self.idle_loop(dt)
            self.shoot_hero(hero, dt)
            self.apply(platforms, dt)
        else:
            self.vel.x = 0
            zone_events.add(ManiacMode(hero, self.rect.bottomleft))
            self.kill()
