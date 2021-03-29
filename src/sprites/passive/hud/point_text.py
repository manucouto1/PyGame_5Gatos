import pygame as pg

POINT_Y = 50


class PointText(pg.sprite.Sprite):
    def __init__(self, container, player):
        super().__init__()
        self.font = pg.font.SysFont("", 64)
        self.player = player
        self.image = self.font.render(f'x {player.punctuation}', True, (0, 0, 0))
        self.rect = self.image.get_rect()
        game = container.get_object('game')
        self.rect.x = game.screen_width - 2 * 64 - 4
        self.rect.y = POINT_Y + 28
        self.increasing = False

    def increase(self):
        self.increasing = True

    def update(self, _):
        if self.increasing:
            self.image = self.font.render(f'x {self.player.punctuation}', True, (0, 0, 0))
            self.increasing = False
