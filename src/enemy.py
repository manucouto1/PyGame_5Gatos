import pygame as pg
import os
import assets
from spritesheet import Spritesheet
from projectile import Projectile

GRAVITY = pg.Vector2((0, 4.8))


class Enemy(pg.sprite.Sprite):

    def __init__(self, width, height, offset, frames, level):
        super().__init__()
        self.idle_L = Spritesheet(assets.path_to("player", "idle", "Hero_idle_L_32x32_200.png"))
        self.idle_R = Spritesheet(assets.path_to("player", "idle", "Hero_idle_R_32x32_200.png"))
        self.walk_L = Spritesheet(assets.path_to("player", "walk", "Hero_walk_L_32x32_200.png"))
        self.walk_R = Spritesheet(assets.path_to("player", "walk", "Hero_walk_R_32x32_200.png"))
        self.level = level
        self.frames = frames
        self.width = width
        self.height = height
        self.idle_id = 0
        self.walk_id = 0
        self.move_x = 0
        self.move_y = 0
        self.idle_images = []
        self.walk_images = []
        self.direction = None
        self.onGround = False
        self.vel = pg.Vector2((0, 0))
        self.speed = 8
        self.jump_strength = 30
        self.num_jumps = 0
        self.offset = offset
        self.image = self.idle_R.image_at((self.offset, 0, width, height))

        self.rect = self.image.get_rect()
        self.path = [0, 100]
        self.walk_count = 0

    def idle_loop(self):
        self.idle_id = (self.idle_id + 1) % self.frames
        if self.direction == pg.K_LEFT:
            self.image = self.idle_L.image_at(
                (self.idle_id * (self.width + self.offset * 2) + self.offset, 0, self.width, self.height))
        elif self.direction == pg.K_RIGHT:
            self.image = self.idle_R.image_at(
                (self.idle_id * (self.width + self.offset * 2) + self.offset, 0, self.width, self.height))

    def walk_loop(self):
        self.walk_id = (self.walk_id + 1) % self.frames
        if self.direction == pg.K_LEFT:
            self.image = (self.walk_L.image_at(
                (self.walk_id * (self.width + self.offset * 2) + self.offset, 0, self.width, self.height)))
        elif self.direction == pg.K_RIGHT:
            self.image = (self.walk_R.image_at(
                (self.walk_id * (self.width + self.offset * 2) + self.offset, 0, self.width, self.height)))

    def gravity(self):
        if not self.onGround:
            self.vel += GRAVITY
            if self.vel.y > 100:
                self.vel.y = 100

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

    def move(self):
        if self.vel.x > 0:
            if self.rect[0] < self.path[1] + self.vel.x:
                self.move_right()
            else:
                self.move_left()
                self.walkCount = 0
        else:
            if self.rect[0] > self.path[0] - self.vel.x:
                self.move_left()
            else:  # Change direction
                self.move_right()
                self.walkCount = 0

    def update(self):
        self.move()
        self.walk_loop()

        self.gravity()
        self.rect.x += self.vel.x
        self.collide(self.vel.x, 0)
        self.rect.y += self.vel.y
        self.onGround = False
        self.collide(0, self.vel.y)

    def collide(self, xvel, yvel):
        for p in self.level:
            if pg.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.num_jumps = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.vel.y = 0

