import pygame as pg
import math


class Projectile(pg.sprite.Sprite):
    def __init__(self, image, x, y, radius):
        super().__init__()
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
        self.x += math.cos(self.angle) * self.vel.x / 50 * dt
        self.y += math.sin(self.angle) * self.vel.y / 50 * dt
        self.rect.x = self.x
        self.rect.y = self.y
