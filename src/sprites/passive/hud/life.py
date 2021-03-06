import pygame as pg
import src.utils.assets as assets
from src.sprites.passive.hud.hearts import Heart
from src.sprites.spritesheet import SpriteSheet
from math import ceil

LIFE_X = Heart.SIZE + 4
LIFE_Y = 30


class Life(pg.sprite.Group):
    """
    Class to manage player life HUD indicator

    :param container: Application container
    :param n_hearts: Number of hearts
    :param player: Player instance
    """
    def __init__(self, container, n_hearts, player):
        path = assets.path_to("player", "Corazon-Sheet.png")
        sheet = container.image_from_path(path)
        sheet = pg.transform.scale(sheet, (Heart.SIZE * 21, Heart.SIZE))
        self.sheet = SpriteSheet(sheet)
        self.hearts = []
        self.player = player
        pos = ceil(self.player.life / 2) - 1

        # Full hearts
        for i in range(pos):
            heart = Heart(self.sheet, 0)
            self.heart_pos(heart, i)
            self.hearts.append(heart)

        # Half hearts
        heart = Heart(self.sheet, self.player.life % 2)
        self.heart_pos(heart, pos)
        self.hearts.append(heart)

        # Empty hearts
        for i in range(pos + 1, n_hearts):
            heart = Heart(self.sheet, 2)
            self.heart_pos(heart, i)
            self.hearts.append(heart)

        self.queue = []
        super().__init__(self.hearts)

    @staticmethod
    def heart_pos(heart, pos):
        heart.rect[0] = 4 + LIFE_X * pos
        heart.rect[1] = LIFE_Y

    def decrease(self):
        if self.player.life > 1:
            self.hearts[ceil(self.player.life / 2) - 1].decrease()
            self.player.life -= 1
        elif self.player.life == 1:
            self.hearts[0].decrease()
            self.player.life -= 1

    def increase(self):
        self.player.hearts += 1
        if self.player.life < 6:
            self.player.life += 1
            self.hearts[ceil(self.player.life / 2) - 1].increase()
        elif self.player.life == 1:
            self.player.life += 1
            self.hearts[0].increase()
