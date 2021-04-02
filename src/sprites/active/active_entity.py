import time
import random

import numpy as np
import pygame as pg
from pygame.sprite import collide_rect

from src.sprites.spritesheet import SpriteStripAnim
from src.utils import assets

GRAVITY = pg.Vector2((0, 3.8))


class ActiveEntity(pg.sprite.Sprite):
    """
    Class to implement moving sprites

    :param container: Application container
    :param entity: Enemy map DTO
    :param character: Character DTO
    """
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
        self.y_movement = False
        self.gravity_value = pg.Vector2((0, 3.8))
        self.vel = pg.Vector2((0, 0))
        self.speed = 8
        self.jump_strength = 28
        self.num_jumps = 0
        self.damage_time = 0
        self.falling_velocity = 0
        self.mixer = container.get_object('mixer')

    def shutdown_gravity(self, falling_velocity=1):
        """
        Enables free fall mode

        :param falling_velocity: Gravity speed
        """
        self.jump_strength = 0
        self.falling_velocity = falling_velocity
        self.falling_mode = True

    def on_gravity(self):
        """
        Disables free fall mode
        """
        self.jump_strength = 28
        self.falling_mode = False

    def calc_distance(self, hero):
        a = (self.rect.x - hero.rect.x) ** 2
        b = (self.rect.y - hero.rect.y) ** 2

        return np.sqrt(a + b)

    def idle_loop(self, dt):
        """
        Rolls the idle sprite sheet strip

        :param dt: Elapsed clock time
        """
        self.image = self.sheet[0].next(dt)
        self.mask = self.sheet.get_mask()

    def walk_loop(self, dt):
        """
        Rolls the walk sprite sheet strip for the current direction

        :param dt: Elapsed clock time
        """
        if self.direction == pg.K_LEFT:
            self.image = self.sheet[2].next(dt)
            self.mask = self.sheet.get_mask()
        elif self.direction == pg.K_RIGHT:
            self.image = self.sheet[1].next(dt)
            self.mask = self.sheet.get_mask()

    def gravity(self, dt):
        """
        Updates gravity effects for the sprite

        :param dt: Elapsed clock time
        """
        if self.falling_mode and not self.y_movement:
            self.vel.y = (self.falling_velocity / 50) * dt
        elif not self.onGround:
            self.vel += (self.gravity_value / 50) * dt
            if self.vel.y > 63:
                self.vel.y = 63
            if self.vel.x > 63:
                self.vel.x = 63

    def jump(self):
        """
        Makes the sprite to jump
        """
        if self.onGround:
            self.vel.y = -self.jump_strength
            self.num_jumps += 1
            self.mixer.play_jump()
        elif self.num_jumps < 2:
            self.vel.y = -self.jump_strength
            self.num_jumps += 1
            self.mixer.play_jump()

    def move_left(self):
        """
        Sets the sprite movement direction to the left
        """
        if self.falling_mode:
            self.vel.x = -self.speed - self.falling_velocity
        else:
            self.vel.x = -self.speed

        self.vel.x = -self.speed
        self.direction = pg.K_LEFT
        self.movement = True

    def move_right(self):
        """
        Sets the sprite movement direction to the right
        """
        self.vel.x = self.speed
        if self.falling_mode:
            self.vel.x = self.speed + self.falling_velocity
        else:
            self.vel.x = self.speed
        self.direction = pg.K_RIGHT
        self.movement = True

    def move_up(self):
        """
        Sets the sprite movement direction to up in free fall
        """
        self.vel.y = -self.speed
        if self.falling_mode:
            self.vel.y = -self.speed - self.falling_mode
        else:
            self.vel.y = -self.speed
        self.y_movement = True

    def move_down(self):
        """
        Sets the sprite movement direction to down in free fall
        """
        self.vel.y = self.speed
        if self.falling_mode:
            self.vel.y = +self.speed + self.falling_mode
        else:
            self.vel.y = +self.speed
        self.y_movement = True

    def reset_movement(self):
        """
        Finished sprite movement
        """
        self.movement = False
        self.y_movement = False
        self.vel.x = 0

    def damage_effect(self, hit):
        """
        Makes the sprite to move after a hit

        :param hit: Rect of the object that hit the sprite
        """
        left, right = self.after_hit_direction(hit)
        self.choose_mov(left, right)
        self.getting_damage = True
        self.damage_time = time.time()
        self.jump()
        self.num_jumps = 0

    def after_hit_direction(self, hit):
        """
        Decides the direction of the sprite movement after a hit

        :param hit: Rect of the object that hit the sprite
        """
        right = hit.rect.left < self.rect.right
        left = hit.rect.right > self.rect.left

        return left, right

    def choose_mov(self, left, right):
        """
        Move the sprite to the selected direction or choose one random if both equal

        :param left: Boolean
        :param right: Boolean
        """
        if left:
            self.move_left()
        elif right:
            self.move_right()
        else:
            random.choice([self.move_right, self.move_left])()

    def collide_ground(self, xvel, yvel, platforms, dt, fun=collide_rect):
        """
        Checks the collision with platforms

        :param xvel: x speed
        :param yvel: y speed
        :param platforms: Platform list
        :param dt: Elapsed clock time
        :param fun: Collision function
        """
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
        """
        Checks the collision with platforms while free fall

        :param xvel: x speed
        :param yvel: y speed
        :param platforms: Platform list
        :param fun: Collision function
        """
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
        """
        Updates gravity and checks collisions

        :param platforms: Platform list
        :param dt: Elapsed clock time
        """
        self.gravity(dt)
        vel_x = (self.vel.x / 50 * dt)
        self.rect.x += vel_x if (vel_x <= 63) else 63
        self.collide_ground(self.vel.x, 0, platforms, dt)
        vel_y = (self.vel.y / 50 * dt)
        self.rect.y += vel_y if (vel_y <= 63) else 63
        self.onGround = False
        self.collide_ground(0, self.vel.y, platforms, dt)
