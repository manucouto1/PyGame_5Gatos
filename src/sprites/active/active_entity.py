import pygame as pg
import src.utils.assets as assets
from src.sprites.spritesheet import Spritesheet, SpriteStripAnim

GRAVITY = pg.Vector2((0, 3.8))


class ActiveEntity(pg.sprite.Sprite):

    def __init__(self, path, width, height, offset, frames, *groups):
        super().__init__(*groups)
        # assets.path_to("player", "idle", "Hero_idle_L_32x32_200.png")
        self.sheet = SpriteStripAnim(path, (0, 0, width, height), frames, rows=4)
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
        self.image = self.sheet.image_at((self.offset, 0, width, height))

        self.rect = self.image.get_rect()

    def idle_loop(self):
        self.image = self.sheet[0].next()

    def walk_loop(self):
        if self.direction == pg.K_LEFT:
            self.image = self.sheet[1].next()
        elif self.direction == pg.K_RIGHT:
            self.image = self.sheet[2].next()

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

    def collide_ground(self, xvel, yvel, platforms):
        collide_l = pg.sprite.spritecollide(self, platforms, False)
        for p in collide_l:
            if pg.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.num_jumps = 0
                    d = pg.sprite.spritecollide(self, platforms, False)
                    if len(d) > 0:
                        s = sorted(d, key=lambda e: e.rect.top, reverse=True)
                        self.rect.bottom = s[0].rect.top
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.vel.y = 0

    def apply(self, platforms):
        self.gravity()
        self.rect.x += self.vel.x
        self.collide_ground(self.vel.x, 0, platforms)
        self.rect.y += self.vel.y
        self.onGround = False
        self.collide_ground(0, self.vel.y, platforms)

