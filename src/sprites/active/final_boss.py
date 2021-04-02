import time
import pygame as pg

from src.sprites.active.active_entity import ActiveEntity
from src.sprites.active.enemy_turret_shooter import EnemyTurretShooter
from src.sprites.passive.event import EndGame


class FinalBoss(EnemyTurretShooter):
    def __init__(self, container, entity, *groups):
        super().__init__(container, entity, *groups)
        self.life = 18
        self.maniac = True
        self.maniac_time = 1
        self.boss_mode = 1
        game = container.get_object('game')
        level_dto = container.get_object('level_dto')
        self.world_size = pg.Rect(0, 0, level_dto.map_width * level_dto.tile_size,
                                  level_dto.map_height * level_dto.tile_size)
        self.screen_size = pg.Rect((0, 0, game.screen_width, game.screen_height))

    def shutdown_gravity(self, _):
        self.boss_mode = 2
        self.life = 36
        ActiveEntity.shutdown_gravity(self, falling_velocity=3)

    def on_gravity(self):
        self.boss_mode = 3
        self.life = 36
        ActiveEntity.on_gravity(self)

    def follow(self, hero):
        y = hero.rect.center[1] - self.rect.center[1]
        self.rect.y += y * 0.01

    def move(self, hero, dt):
        distance = self.calc_distance(hero)
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

        if self.boss_mode == 1:
            if self.life > 0:
                if self.movement:
                    self.walk_loop(dt)
                else:
                    self.idle_loop(dt)
                self.move(hero, dt)
                self.apply(platforms, dt)
            else:
                self.walk_loop(dt)
                self.move_right()
                self.apply(platforms, dt)
        elif self.boss_mode == 2:
            if self.life > 0:
                if self.movement:
                    self.walk_loop(dt)
                else:
                    self.idle_loop(dt)
                self.move(hero, dt)
                self.follow(hero)
                self.apply(platforms, dt)
            else:
                self.falling_mode = False
                self.apply(platforms, dt)

        elif self.boss_mode == 3:
            if self.life > 0:
                if self.movement:
                    self.walk_loop(dt)
                else:
                    self.idle_loop(dt)
                self.move(hero, dt)
                self.apply(platforms, dt)
            else:
                self.vel.x = 0
                level = self.container.get_object('level')
                event = EndGame(level, self.rect.bottomleft)
                zone_events.add(event)
                self.kill()
