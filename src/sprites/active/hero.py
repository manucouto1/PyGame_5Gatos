import pygame as pg
from src.sprites.pasive.projectile import Projectile
from src.sprites.active.active_entity import ActiveEntity

GRAVITY = pg.Vector2((0, 4.8))


class Hero(ActiveEntity):

    def __init__(self, width, height, offset, frames):
        super().__init__(width, height, offset, frames)


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

    def update(self, platforms):
        if self.movement:
            self.walk_loop()
        else:
            self.idle_loop()

        self.apply(platforms)
        self.reset_movement()

