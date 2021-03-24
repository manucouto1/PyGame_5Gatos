from src.sprites.active.enemy import Enemy
import pygame as pg

RIGHT = 0
LEFT = 1


class EnemyDummy(Enemy):
    def __init__(self, container, entity, *groups):
        Enemy.__init__(self, container, entity, *groups)
        self.moving = LEFT

    def move(self):
        if self.moving == RIGHT:
            self.move_right()
        elif self.moving == LEFT:
            self.move_left()

    def collide_ground(self, xvel, yvel, platforms):
        collide_l = pg.sprite.spritecollide(self, platforms, False)
        for p in collide_l:
            if pg.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    if self.moving == RIGHT:
                        self.reset_movement()
                        self.moving = LEFT
                if xvel < 0:
                    self.rect.left = p.rect.right
                    if self.moving == LEFT:
                        self.reset_movement()
                        self.moving = RIGHT
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.num_jumps = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.vel.y = 0
