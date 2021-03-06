import time

from pygame.sprite import collide_rect
from src.sprites.active.active_entity import ActiveEntity
import pygame as pg

from src.sprites.passive.event import KittyPoint

RIGHT = 0
LEFT = 1


class EnemyDummy(ActiveEntity):
    """
    Class implementing the rolling enemies

    :param container: Application container
    :param entity: Enemy map DTO
    """
    def __init__(self, container, entity, *groups):
        super().__init__(container, entity, *groups)
        self.walk_count = 0
        self.dead_id = 0
        self.last_hit = time.time()

        self.sheet[0].set_frames_skip(2)
        self.sheet[1].set_frames_skip(2)
        self.sheet[2].set_frames_skip(2)
        self.sheet[3].set_frames_skip(2)
        self.moving = LEFT
        self.life = 1

    def move(self):
        """
        Move the sprite towards current direction
        """
        if self.moving == RIGHT:
            self.move_right()
        elif self.moving == LEFT:
            self.move_left()

    def update(self, hero, zone_events, platforms, dt, gravity=pg.Vector2((0, 3.8))):
        if self.life > 0:
            self.move()
            self.walk_loop(dt)
            self.apply(platforms, dt)
        else:
            self.vel.x = 0
            zone_events.add(KittyPoint(hero, self.sheet, self.rect.bottomleft))
            self.kill()

    def is_hit(self, dangerous):
        """
        Checks if its hit by a dangerous platform and make some movement if enough time elapsed from last

        :param dangerous: list[Platform]
        """
        new_hit = time.time()
        if self.last_hit + 0.5 < new_hit:
            self.damage_effect(dangerous[0])
            self.last_hit = new_hit

    def is_shoot(self, bullet):
        """
        Play get shoot effects
        """
        self.life -= 1
        if self.life == 0:
            self.damage_effect(bullet)
            self.mixer.play_destroy_enemy()
        else:
            self.damage_effect(bullet)
            self.mixer.play_enemy_hit()

    def collide_ground(self, xvel, yvel, platforms, _):
        """
        Checks the collision with platforms, it makes the sprite to
        keep moving in the opposite direction when it hits a wall

        :param xvel: x speed
        :param yvel: y speed
        :param platforms: Platform list
        """
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
