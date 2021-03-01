import pygame as pg
import math

GRAVITY = pg.Vector2((0, 4.8))


class Projectile(pg.sprite.Sprite):
    def __init__(self, x, y, radius, color=(0, 0, 0)):
        super().__init__()
        self.x = x
        self.y = y
        self.h = 0
        self.image = pg.Surface((int(radius*2), int(radius*2)))
        self.radius = radius
        self.color = color
        self.vel = pg.Vector2((18, 18))
        self.angle = 0
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def trajectory(self, pos):
        (mx, my) = pos
        slope_x = mx - self.x
        slope_y = my - self.y
        self.angle = math.atan2(slope_y, slope_x)

    def update(self):
        self.x += math.cos(self.angle) * self.vel.x
        self.y += math.sin(self.angle) * self.vel.y
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, win):
        win.blit(self.image, (int(self.x - self.radius), int(self.y - self.radius)))
