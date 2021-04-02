import math
import time

import numpy as np

from src.sprites.active.active_entity import ActiveEntity
from src.sprites.passive.projectile import Projectile
import pygame as pg
import src.utils.assets as assets


class ShooterEntity(ActiveEntity):
    """
    Class for the sprites that can shoot

    :param container: Application container
    :param entity: Enemy map DTO
    :param character: Character DTO
    """
    def __init__(self, container, entity, character, *groups):
        path = assets.path_to('projectiles', character.projectile)
        image = container.image_from_path(path)
        self.projectile = pg.transform.scale(image, (32, 32))
        ActiveEntity.__init__(self, container, entity, character, *groups)
        self.maniac_time = 10
        self.maniac_init = time.time()
        self.maniac = False

    def shoot(self, target):
        """
        Shoot a bullet aimed towards a target

        :param target: Target position (x, y)
        """
        (m_x, m_y) = target
        m_pos = (t_x, _) = (m_x - self.scroll.x, m_y - self.scroll.y)

        if t_x > self.rect.x:
            self.direction = pg.K_RIGHT
            correct = self.rect.width / 2
        elif t_x < self.rect.x:
            self.direction = pg.K_LEFT
            correct = -self.rect.width / 2
        else:
            correct = 0

        if self.rect.width > 32:
            orig = round(self.rect.x), round(self.rect.y + (self.rect.height / 2))
            bullet = Projectile(self.projectile, orig, m_pos, 6)
        else:
            orig = round(self.rect.x + correct), round(self.rect.y)
            bullet = Projectile(self.projectile, orig, m_pos, 6)

        self.mixer.play_shoot()

        return bullet

    def shoot_maniac(self, bullet_group):
        """
        Shoots bullets all around the sprite

        :param bullet_group: Group to add the bullets
        """
        shots_count = 0
        if self.maniac:
            if time.time() - self.maniac_init <= self.maniac_time:
                if len(bullet_group) < 8:
                    for i in np.arange(0, 2 * math.pi, math.pi / 8):
                        x = math.cos(i) * 100
                        y = math.sin(i) * 100
                        bullet = ShooterEntity.shoot(self, (self.rect.x + self.scroll.x + x,
                                                            self.rect.y + self.scroll.y + y))
                        bullet_group.add(bullet)

                        shots_count += 1
            else:
                self.maniac = False

        return shots_count
