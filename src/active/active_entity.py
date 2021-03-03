import pygame as pg
import assets
from src.spritesheet import Spritesheet

GRAVITY = pg.Vector2((0, 4.8))


class ActiveEntity(pg.sprite.Sprite):

    def __init__(self, width, height, offset, frames, level, *groups):
        super().__init__(*groups)
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
        self.movement = None
        self.direction = None
        self.onGround = False
        self.vel = pg.Vector2((0, 0))
        self.speed = 8
        self.jump_strength = 30
        self.num_jumps = 0
        self.offset = offset
        self.image = self.idle_R.image_at((self.offset, 0, width, height))

        self.rect = self.image.get_rect()

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
        top_x = self.walk_id * (self.width + self.offset * 2) + self.offset
        if self.direction == pg.K_LEFT:
            self.image = self.walk_L.image_at((top_x, 0, self.width, self.height))
        elif self.direction == pg.K_RIGHT:
            self.image = self.walk_R.image_at((top_x, 0, self.width, self.height))

    def gravity(self):
        if not self.onGround:
            self.vel += GRAVITY
            if self.vel.y > 100:
                self.vel.y = 100

    def jump(self):
        if self.onGround:
            self.vel.y = -self.jump_strength
            self.num_jumps += 1
            print("jump num:", self.num_jumps)
        elif self.num_jumps < 2:
            self.vel.y = -self.jump_strength
            self.num_jumps += 1
            print("double num:", self.num_jumps)

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

    def collide_ground(self, xvel, yvel):
        level_c = pg.sprite.spritecollideany(self, self.level)
        if level_c:
            if xvel > 0:
                self.rect.right = level_c.rect.left
            if xvel < 0:
                self.rect.left = level_c.rect.right
            if yvel > 0:
                self.rect.bottom = level_c.rect.top
                self.onGround = True
                self.num_jumps = 0
            if yvel < 0:
                self.rect.top = level_c.rect.bottom
                self.vel.y = 0

