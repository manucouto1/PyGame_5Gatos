from pygame.sprite import collide_rect

from src.sprites.active.enemy import Enemy
import pygame as pg

RIGHT = 0
LEFT = 1


class EnemyDummy(Enemy):
    def __init__(self, container, entity, *groups):
        Enemy.__init__(self, container, entity, *groups)
        self.moving = LEFT
        self.life = 1
        #self.hero = container.get_object('hero')

    def move(self, dt):
        if self.moving == RIGHT:
            self.move_right()
        elif self.moving == LEFT:
            self.move_left()

    def collide_ground(self, xvel, yvel, platforms, _):
        collide_l = pg.sprite.spritecollide(self, platforms, False)
        bot_left_collided = 0
        bot_right_collided = 0
        bot_mid_collided = 0

        for p in collide_l:
            if pg.sprite.collide_rect(self, p):
                bot_left_collided = p.rect.collidepoint(self.rect.bottomleft)
                bot_mid_collided = p.rect.collidepoint(self.rect.midbottom)
                bot_right_collided = p.rect.collidepoint(self.rect.bottomright)
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

        if len(collide_l) == 1 and not bot_right_collided and not bot_mid_collided and bot_left_collided:
            self.reset_movement()
            self.moving = LEFT
        if len(collide_l) == 1 and not bot_left_collided and not bot_mid_collided and bot_right_collided:
            self.reset_movement()
            self.moving = RIGHT