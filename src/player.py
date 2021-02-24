import pygame as pg
import os
from spritesheet import Spritesheet

GRAVITY = pg.Vector2((0, 0.3))


class Player(pg.sprite.Sprite):

    def __init__(self, width, height, frames, level):
        super().__init__()
        self.idle_L = Spritesheet(".."+os.sep+"assets"+os.sep+"player"+os.sep+"idle"+os.sep+"Hero_idle_L_32x32_200.png")
        self.idle_R = Spritesheet(".."+os.sep+"assets"+os.sep+"player"+os.sep+"idle"+os.sep+"Hero_idle_R_32x32_200.png")
        self.walk_L = Spritesheet(".."+os.sep+"assets"+os.sep+"player"+os.sep+"walk"+os.sep+"Hero_walk_L_32x32_200.png")
        self.walk_R = Spritesheet(".."+os.sep+"assets"+os.sep+"player"+os.sep+"walk"+os.sep+"Hero_walk_R_32x32_200.png")
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
        self.jump_strength = 10
        self.offset = 16
        self.image = self.idle_R.image_at((self.offset, 0, width, height))
        
        self.rect = self.image.get_rect()

    def idle_loop(self):
        self.idle_id = (self.idle_id + 1) % self.frames
        if self.direction == pg.K_LEFT:
            self.image = self.idle_L.image_at((self.idle_id*(self.width+self.offset*2) + self.offset, 0, self.width, self.height))
        elif self.direction == pg.K_RIGHT:
            self.image = self.idle_R.image_at((self.idle_id*(self.width+self.offset*2) + self.offset, 0, self.width, self.height))

    def walk_loop(self):
        self.walk_id = (self.walk_id + 1) % self.frames
        if self.direction == pg.K_LEFT:
            self.image = (self.walk_L.image_at((self.walk_id*(self.width+self.offset*2) + self.offset, 0, self.width, self.height)))
        elif self.direction == pg.K_RIGHT:
            self.image = (self.walk_R.image_at((self.walk_id*(self.width+self.offset*2) + self.offset, 0, self.width, self.height)))

    def gravity(self):
        if not self.onGround:
            self.vel += GRAVITY
            if self.vel.y > 100:
                self.vel.y = 100
    
    def jump(self):
        if self.onGround:
            self.vel.y = -self.jump_strength

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

    def update(self):
        if self.movement:
            self.walk_loop()
        else:
            self.idle_loop()

        self.gravity()
        self.rect.x += self.vel.x
        self.collide(self.vel.x, 0, self.level)
        self.rect.y += self.vel.y
        self.onGround = False
        self.collide(0, self.vel.y, self.level)
        self.reset_movement()

    def collide(self, xvel, yvel, platforms):
        for p in self.level:
            if pg.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

