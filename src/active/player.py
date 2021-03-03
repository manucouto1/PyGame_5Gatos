import pygame as pg
from src.projectile import Projectile
from src.active.active_entity import ActiveEntity

GRAVITY = pg.Vector2((0, 4.8))


class Player(ActiveEntity):

    def __init__(self, width, height, offset, frames, level):
        super().__init__(width, height, offset, frames, level)

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

    def update(self):
        if self.movement:
            self.walk_loop()
        else:
            self.idle_loop()

        self.gravity()
        self.rect.x += self.vel.x
        self.collide_ground(self.vel.x, 0)
        self.rect.y += self.vel.y
        self.onGround = False
        self.collide_ground(0, self.vel.y)
        self.reset_movement()


