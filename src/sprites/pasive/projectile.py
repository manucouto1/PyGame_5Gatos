import pygame as pg
import math


class Projectile(pg.sprite.Sprite):
    def __init__(self, x, y, radius, color=(0, 0, 0)):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pg.Surface((int(radius * 2), int(radius * 2)))
        self.radius = radius
        self.color = color
        self.vel = pg.Vector2((25, 25))
        self.angle = 0
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

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
