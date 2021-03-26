from src.sprites.active.active_entity import ActiveEntity
from src.sprites.passive.projectile import Projectile
import pygame as pg
import src.utils.assets as assets
from src.sprites.spritesheet import SpriteSheet


class ShutterEntity(ActiveEntity):
    def __init__(self, container, entity, character, *groups):
        path_projectiles = assets.path_to('projectiles', character.projectile)
        self.projectile_sheet = SpriteSheet(container, path_projectiles)
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

        image = self.projectile_sheet.image_at((0, 0, 64, 64))
        image = pg.transform.scale(image, (32, 32))
        bullet = Projectile(image, round(self.rect.x + correct), round(self.rect.y + self.rect.height // 2), 6)

        bullet.trajectory(m_pos)

        return bullet
