import time
import random
import pygame as pg
from pygame.sprite import collide_rect

from src.sprites.spritesheet import SpriteStripAnim
from src.utils import assets

GRAVITY = pg.Vector2((0, 3.8))


class ActiveEntity(pg.sprite.Sprite):
    def __init__(self, container, entity, character, *groups):
        super().__init__(*groups)
        sheet_path = assets.path_to("characters", character.name, character.sheet)
        sheet = SpriteStripAnim(container, sheet_path, (0, 0, character.height, character.width), character.rows,
                                rows=4)

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
        self.vel = pg.Vector2((0, 0))
        self.speed = 8
        self.jump_strength = 28
        self.num_jumps = 0
        self.damage_time = 0
        self.mixer = container.get_object('mixer')

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
        if not self.onGround:
            self.vel += (GRAVITY / 50) * dt
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

    def reset_movement(self):
        self.movement = False
        self.vel.x = 0

    def damage_effect(self, its_hit):
        bot_left_collided = its_hit.rect.collidepoint(self.rect.bottomleft)
        top_left_collided = its_hit.rect.collidepoint(self.rect.topleft)
        mid_left_collided = its_hit.rect.collidepoint(self.rect.midleft)

        bot_right_collided = its_hit.rect.collidepoint(self.rect.bottomright)
        top_right_collided = its_hit.rect.collidepoint(self.rect.topright)
        mid_right_collided = its_hit.rect.collidepoint(self.rect.midright)

        if bot_left_collided or top_left_collided or mid_left_collided:
            self.move_right()

        elif bot_right_collided or top_right_collided or mid_right_collided:
            self.move_left()
        else:
            random.choice([self.move_right, self.move_left])()

        self.getting_damage = True
        self.damage_time = time.time()

        self.jump()

    def collide_ground(self, xvel, yvel, platforms, dt, fun=collide_rect):
        collide_l = pg.sprite.spritecollide(self, platforms, False, collided=fun)
        for p in collide_l:
            if fun(self, p):
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.num_jumps = 0
                    p.update(dt, True)
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.vel.y = 0
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right

    def collide_ground_falling(self, xvel, yvel, platforms, dt, fun=collide_rect):
        collide_l = pg.sprite.spritecollide(self, platforms, False, collided=fun)
        for p in collide_l:
            if fun(self, p):
                if yvel > 0:
                    """
                    bottom_left = p.rect.collidepoint(self.rect.bottomleft)
                    bottom_right = p.rect.collidepoint(self.rect.bottomright)
                    mid_bottom = p.rect.collidepoint(self.rect.midbottom)
                    if bottom_left and mid_bottom or bottom_right and mid_bottom:
                    """
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.num_jumps = 0
                    p.update(dt, True)
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
