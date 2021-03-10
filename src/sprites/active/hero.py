import pygame as pg
from src.sprites.pasive.projectile import Projectile
from src.sprites.active.active_entity import ActiveEntity
import time

GRAVITY = pg.Vector2((0, 4.8))


class Hero(ActiveEntity):

    def __init__(self, width, height, offset, frames, life):
        super().__init__(width, height, offset, frames)
        self.last_hit = time.time()
        self.life = life

    def shoot(self, camera):
        # look to shoot direction
        (m_x, m_y) = pg.mouse.get_pos()
        m_pos = (m_x - camera.cam.x, m_y - camera.cam.y)

        if m_x > self.rect.x + camera.cam.x:
            self.direction = pg.K_RIGHT
        elif m_x < self.rect.x + camera.cam.x:
            self.direction = pg.K_LEFT

        if self.direction == pg.K_LEFT:
            offset = -self.offset
        else:
            offset = self.offset

        bullet = Projectile(round(self.rect.x + self.rect.width // 2 + offset),
                            round(self.rect.y + self.rect.height // 2), 6)

        bullet.trajectory(m_pos)
        return bullet

    def is_hit(self, dangerous):
        collide_l = pg.sprite.spritecollideany(self, dangerous)
        if collide_l:
            new_hit = time.time()
            if self.last_hit + 2 < new_hit:
                self.last_hit = new_hit
                self.life.decrease()

    def update(self, platforms, dangerous):
        if self.movement:
            self.walk_loop()
        else:
            self.idle_loop()
        self.life.update()
        self.apply(platforms)
        self.reset_movement()
