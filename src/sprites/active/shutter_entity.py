from src.sprites.active.active_entity import ActiveEntity
from src.sprites.pasive.projectile import Projectile
import pygame as pg


class ShutterEntity(ActiveEntity):

    def shoot(self, target):
        (m_x, m_y) = target
        m_pos = (m_x - self.scroll.x, m_y - self.scroll.y)

        if m_x > self.rect.x + self.scroll.x:
            self.direction = pg.K_RIGHT
            correct = self.rect.width
        elif m_x < self.rect.x + self.scroll.x:
            self.direction = pg.K_LEFT
            correct = 0
        else:
            correct = 0

        bullet = Projectile(round(self.rect.x + correct),
                            round(self.rect.y + self.rect.height // 2), 6)

        bullet.trajectory(m_pos)

        return bullet
