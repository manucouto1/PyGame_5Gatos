import pygame as pg
import math
import time


class Projectile(pg.sprite.Sprite):
    def __init__(self, image, x, y, radius):
        super().__init__()
        self.born_moment = time.time()
        self.life_time = 1.75
        self.x = x
        self.y = y
        self.image = image
        self.vel = pg.Vector2((25, 25))
        self.angle = 0
        self.rect = pg.Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)

    def trajectory(self, pos):
        mx, my = pos
        slope_x = mx - self.x
        slope_y = my - self.y
        self.angle = math.atan2(slope_y, slope_x)

    def update(self, dt):
        if time.time() - self.born_moment > self.life_time:
            self.kill()
        else:
            self.x += math.cos(self.angle) * self.vel.x / 50 * dt
            self.y += math.sin(self.angle) * self.vel.y / 50 * dt
            self.rect.x = self.x
            self.rect.y = self.y
