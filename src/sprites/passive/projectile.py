import pygame as pg
import math
import time


class Projectile(pg.sprite.Sprite):
    """
    Class to handle projectiles in screen
    """
    def __init__(self, image, pos, target, radius):
        super().__init__()
        self.born_moment = time.time()
        self.life_time = 1.75
        self.image = image
        self.vel = pg.Vector2((25, 25))
        self.angle = 0
        self.rect = pg.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)
        self._trajectory(target)

    def _trajectory(self, target):
        """
        Sets angle for trajectory

        :param target: Target position (x, y)
        """
        mx, my = target
        dx = mx - self.rect[0]
        dy = my - self.rect[1]
        self.angle = math.atan2(dy, dx)

    def update(self, dt):
        if time.time() - self.born_moment > self.life_time:
            self.kill()
        else:
            self.rect.x += math.cos(self.angle) * self.vel.x / 50 * dt
            self.rect.y += math.sin(self.angle) * self.vel.y / 50 * dt
