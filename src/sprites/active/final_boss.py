import time
import pygame as pg

from src.sprites.active.active_entity import ActiveEntity
from src.sprites.active.enemy_turret_shooter import EnemyTurretShooter
from src.sprites.passive.event import EndGame, ExtraLife


class FinalBoss(EnemyTurretShooter):
    def __init__(self, container, entity, *groups):
        super().__init__(container, entity, *groups)
        self.life = 18
        self.maniac = True
        self.maniac_time = 1
        self.boss_mode = 1
        self.last_bleed = 0
        self.last_shoot = 0
        game = container.get_object('game')
        level_dto = container.get_object('level_dto')
        self.level = container.get_object('level')
        self.map_min_x = 0
        self.map_max_x = level_dto.map_width * level_dto.tile_size
        self.map_max_y = level_dto.map_height * level_dto.tile_size
        self.map_tile_size = level_dto.tile_size
        self.world_size = pg.Rect(0, 0, self.map_max_x, self.map_max_y)
        self.screen_size = pg.Rect((0, 0, game.screen_width, game.screen_height))

    def shutdown_gravity(self, falling_velocity=1):
        self.boss_mode = 2
        self.life = 36
        ActiveEntity.shutdown_gravity(self, falling_velocity)

    def is_shoot(self, bullet):
        new_time = time.time()
        if new_time - self.last_shoot > 1:
            self.damage_effect(bullet)
        if new_time - self.last_shoot > 2:
            self.last_shoot = new_time
            self.life -= 1
            if self.life == 0:
                self.mixer.play_destroy_enemy()
            else:
                self.mixer.play_enemy_hit()

    def on_gravity(self):
        self.boss_mode = 3
        self.life = 18
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

            self.shoot_hero(hero, dt)
        else:
            if time.time() - self.maniac_init > 1:
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

        new_time = time.time()
        if new_time - self.last_bleed > 15 and self.getting_damage:
            self.last_bleed = new_time
            zone_events.add(ExtraLife(hero, self.rect.bottomleft))
            zone_events.add(ExtraLife(hero, self.rect.bottomright))
            zone_events.add(ExtraLife(hero, self.rect.midtop))

        if self.boss_mode == 1:
            if self.rect.x < self.map_min_x + self.map_tile_size:
                self.move_right()

            if self.rect.x > self.map_max_x - self.map_tile_size:
                self.move_left()

            if self.life > 0:
                if self.movement:
                    self.walk_loop(dt)
                else:
                    self.idle_loop(dt)
                self.move(hero, dt)
                self.apply(platforms, dt)
            else:
                self.level.time_to_fall = True
                self.getting_damage = False
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
                self.jump_strength = 28
                self.falling_mode = False
                self.apply(platforms, dt)

            self.level.enemy_limit(self)

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
                zone_events.add(EndGame(self.level, self.rect.bottomleft))
                self.kill()

            self.level.enemy_limit(self)