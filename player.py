import pygame as pg
import os
from spritesheet import Spritesheet

class Player(pg.sprite.Sprite):

    def __init__(self, width, height, frames, level):
        super().__init__()
        self.idle_sheet = Spritesheet("assets"+os.sep+"Hero_idle-export.png")
        self.walk_sheet = Spritesheet("assets"+os.sep+"Hero_walk-Sheet.png")
        self.rect = pg.Rect(0, 0, width, height)
        self.level = level
        self.frames = frames
        self.idle_id = 0
        self.walk_id = 0
        self.idle_images = []
        self.walk_images = []
        self.movement = False
        self.move_x = 0
        self.move_y = 0
        self.is_jumping = True
        self.is_falling = True
        
        for i in range(frames):
            self.idle_images.append(self.idle_sheet.image_at((i*width, 0, width, height)))
            self.walk_images.append(self.walk_sheet.image_at((i*width, 0, width, height)))

        self.image = self.idle_sheet.image_at((0,0, width, height))
        self.rect = self.image.get_rect()
    
    def state(self, state):
        if not state:
            self.walk_id = 0
        self.movement = state

    def idle_loop(self):
        self.idle_id = ( (self.idle_id + 1) % self.frames)
        self.image = self.idle_images[self.idle_id]
    
    def walk_loop(self):
        self.walk_id = ( (self.walk_id + 1) % self.frames)
        #Hay una funcion transform.flip que no se aun que hace y que algunos la usan para caminar
        self.image = self.walk_images[self.walk_id]

    def gravity(self):
        if self.is_jumping:
            self.move_y += 3.2
    
    def jump(self):
        if self.is_jumping is False:
            self.is_falling = False
            self.is_jumping = True

    def control(self, x, y):
        self.move_x = x

    def update(self):
        if self.movement:
            self.walk_loop()
        else:
            self.idle_loop()

        ground_hit_list = pg.sprite.spritecollide(self, self.level, False)

        #Esto hay que depurarlo
        for g in ground_hit_list:
            self.move_y = 0
            self.rect.bottom = g.rect.top
            self.is_jumping = False  # stop jumping

        if self.is_jumping and self.is_falling is False:
            self.is_falling = True
            self.move_y -= 9.8  # how high to jump

        self.rect.x += self.move_x
        self.rect.y += self.move_y 

        super().update()

    
        
