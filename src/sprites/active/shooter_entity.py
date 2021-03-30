from src.sprites.active.active_entity import ActiveEntity
from src.sprites.passive.projectile import Projectile
import pygame as pg
import src.utils.assets as assets


class ShooterEntity(ActiveEntity):
    def __init__(self, container, entity, character, *groups):
        path = assets.path_to('projectiles', character.projectile)
        image = container.image_from_path(path)
        self.projectile = pg.transform.scale(image, (32, 32))
        ActiveEntity.__init__(self, container, entity, character, *groups)

    def shoot(self, target):
        (m_x, m_y) = target
        m_pos = (t_x, _) = (m_x - self.scroll.x, m_y - self.scroll.y)

        if t_x > self.rect.x:
            self.direction = pg.K_RIGHT
            correct = self.rect.width/2
        elif t_x < self.rect.x:
            self.direction = pg.K_LEFT
            correct = -self.rect.width/2
        else:
            correct = 0

        if self.rect.width > 32:
            bullet = Projectile(self.projectile, round(self.rect.x), round(self.rect.y + (self.rect.height/2)), 6)
        else:
            bullet = Projectile(self.projectile, round(self.rect.x + correct), round(self.rect.y), 6)

        bullet.trajectory(m_pos)
        self.mixer.play_shoot()

        return bullet
