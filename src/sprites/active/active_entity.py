import time
import random

import numpy as np
import pygame as pg
from pygame.sprite import collide_rect

from src.sprites.spritesheet import SpriteStripAnim
from src.utils import assets

GRAVITY = pg.Vector2((0, 3.8))


class ActiveEntity(pg.sprite.Sprite):
    def __init__(self, container, entity, character, *groups):
        super().__init__(*groups)
        sheet_path = assets.path_to("characters", character.name, character.sheet)
        sheet = container.image_from_path(sheet_path)
        sheet = SpriteStripAnim(sheet, (0, 0, character.height, character.width), character.rows,
                                rows=4, scale=(character.rescale_x, character.rescale_y))

        self.scroll = pg.Vector2(0, 0)
        self.sheet = sheet
        self.image = self.sheet.images[0][0]
        self.mask = self.sheet.masks[0][0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = entity.pos
        self.movement = None
        self.direction = None
        self.onGround = False
        self.getting_damage = False
        self.falling_mode = False
        self.gravity_value = pg.Vector2((0, 3.8))
        self.vel = pg.Vector2((0, 0))
        self.speed = 8
        self.jump_strength = 28
        self.num_jumps = 0
        self.damage_time = 0
        self.falling_velocity = 0
        self.mixer = container.get_object('mixer')

    def shutdown_gravity(self, falling_velocity=1):
        self.jump_strength = 0
        self.falling_velocity = falling_velocity
        self.falling_mode = True

    def on_gravity(self):
        self.jump_strength = 30
        self.falling_mode = False

    def calc_distance(self, hero):
        a = (self.rect.x - hero.rect.x) ** 2
        b = (self.rect.y - hero.rect.y) ** 2

        return np.sqrt(a + b)

    def idle_loop(self, dt):
        self.image = self.sheet[0].next(dt)
        self.mask = self.sheet.get_mask()

    def walk_loop(self, dt):
        if self.direction == pg.K_LEFT:
            self.image = self.sheet[2].next(dt)
            self.mask = self.sheet.get_mask()
        elif self.direction == pg.K_RIGHT:
            self.image = self.sheet[1].next(dt)
            self.mask = self.sheet.get_mask()

    def gravity(self, dt):
        if not self.onGround and not self.falling_mode:
            self.vel += (self.gravity_value / 50) * dt
            if self.vel.y > 63:
                self.vel.y = 63
            if self.vel.x > 63:
                self.vel.x = 63

    def jump(self):
        if self.onGround:
            self.vel.y = -self.jump_strength
            self.num_jumps += 1
            self.mixer.play_jump()
        elif self.num_jumps < 2:
            self.vel.y = -self.jump_strength
            self.num_jumps += 1
            self.mixer.play_jump()

    def move_left(self):
        self.vel.x = -self.speed
        self.direction = pg.K_LEFT
        self.movement = True

    def move_right(self):
        self.vel.x = self.speed
        self.direction = pg.K_RIGHT
        self.movement = True

    def move_up(self):
        self.vel.y = -self.speed
        self.movement = True

    def move_down(self):
        self.vel.y = self.speed
        self.movement = True

    def reset_movement(self):
        self.movement = False
        self.vel.x = 0
        if self.falling_mode:
            self.vel.y = self.falling_velocity

    def damage_effect(self, hit):
        left, right = self.after_hit_direction(hit)

        self.choose_mov(left, right)

        self.getting_damage = True
        self.damage_time = time.time()
        self.jump()
        self.num_jumps = 0

    def after_hit_direction(self, hit):
        right = hit.rect.left < self.rect.right
        left = hit.rect.right > self.rect.left

        return left, right

    def choose_mov(self, left, right):
        if left:
            self.move_left()
        elif right:
            self.move_right()
        else:
            random.choice([self.move_right, self.move_left])()

    def collide_ground(self, xvel, yvel, platforms, dt, fun=collide_rect):
        collide_l = pg.sprite.spritecollide(self, platforms, False, collided=fun)
        for p in collide_l:
            if fun(self, p):
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.num_jumps = 0
                    p.update(True)
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.vel.y = 0
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right

    def collide_ground_falling(self, xvel, yvel, platforms, fun=collide_rect):
        p = pg.sprite.spritecollideany(self, platforms, collided=fun)
        if p:
            if yvel > 0:
                self.rect.bottom = p.rect.top
                self.onGround = True
                self.num_jumps = 0
                p.update(True)
            if xvel > 0:
                self.rect.right = p.rect.left
            if xvel < 0:
                self.rect.left = p.rect.right

    def apply(self, platforms, dt):
        self.gravity(dt)
        vel_x = (self.vel.x / 50 * dt)
        self.rect.x += vel_x if (vel_x <= 63) else 63
        self.collide_ground(self.vel.x, 0, platforms, dt)
        vel_y = (self.vel.y / 50 * dt)


        self.rect.y += vel_y if (vel_y <= 63) else 63
        self.onGround = False
        self.collide_ground(0, self.vel.y, platforms, dt)
