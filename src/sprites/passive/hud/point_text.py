import pygame as pg
import math


class PointText(pg.sprite.Sprite):
    """
    Class to manage score numbering

    :param container: Application container
    :param player: Player instance
    :param point_y: Score height
    """
    def __init__(self, container, player, point_y):
        super().__init__()
        self.font = pg.font.Font('../assets/fonts/Purisa Bold.ttf', 48)
        self.player = player
        self.image = self.font.render(f'x{player.punctuation}', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        game = container.get_object('game')
        self.base_offset = game.screen_width - 3 * 64
        self.rect.x = self.base_offset - 24 * (math.log10(max(1, self.player.punctuation)))
        self.rect.y = point_y + 8
        self.increasing = False

    def increase(self):
        """
        Increase the score number in one
        """
        self.increasing = True

    def update(self, _):
        if self.increasing:
            self.image = self.font.render(f'x{self.player.punctuation}', True, (0, 0, 0))
            self.rect.x = self.base_offset - 24 * (math.log10(max(1, self.player.punctuation)))
            self.increasing = False
