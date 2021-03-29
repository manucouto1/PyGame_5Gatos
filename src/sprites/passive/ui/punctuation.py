import pygame as pg

from src.sprites.passive.ui.point_text import PointText
from src.sprites.passive.ui.points_animation import PointAnim


class Punctuation(pg.sprite.Group):
    def __init__(self, container, player):
        self.player = player
        self.points = [PointAnim(container), PointText(container, player)]
        super().__init__(self.points)

    def increase(self):
        self.player.punctuation += 1
        for point in self.points:
            point.increase()
