import pygame as pg
import math

GRAVITY = pg.Vector2((0, 4.8))


class Projectile(pg.sprite.Sprite):
    def __init__(self, x, y, radius,color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.h = 0
        self.radius = radius
        self.color = color
        self.vel = pg.Vector2((8, 8))
        self.angle = 0

    def trajectory(self, pos):
        (mx, my) = pos

        slope_x = mx - self.x
        slope_y = my - self.y

        self.angle = math.atan2(slope_y, slope_x)

    def update(self):
        self.x += math.cos(self.angle) * self.vel.x
        self.y += math.sin(self.angle) * self.vel.y

    def draw(self, win):
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius)
