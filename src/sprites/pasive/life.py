import pygame as pg
from src.sprites.spritesheet import Spritesheet
import src.utils.assets as assets
from src.sprites.pasive.hearts import Heart
from math import ceil


LIFE_X = Heart.SIZE + 4
LIFE_Y = 50


class Life(pg.sprite.Group):
    def __init__(self, n_hearts, player):
        sheet = Spritesheet(assets.path_to("player", "Corazon-Sheet.png"))
        self.hearts = []
        self.player = player
        pos = ceil(self.player.life / 2) - 1

        # Full hearts
        for i in range(pos):
            heart = Heart(sheet, 0)
            self.heart_pos(heart, i)
            self.hearts.append(heart)

        # Check actual player life
        heart = Heart(sheet, self.player.life % 2)
        self.heart_pos(heart, pos)
        self.hearts.append(heart)

        # Empty hearts
        for i in range(pos + 1, n_hearts):
            heart = Heart(sheet, 2)
            self.heart_pos(heart, i)
            self.hearts.append(heart)

        super().__init__(self.hearts)

    @staticmethod
    def heart_pos(heart, pos):
        heart.rect[0] = 4 + LIFE_X * pos
        heart.rect[1] = LIFE_Y

    def decrease(self):
        self.hearts[ceil(self.player.life / 2) - 1].decrease()
        # TODO esto no deberia estar aqui
        self.player.life -= 1


# Player:
# get_damage()
# life.decrease()
# life = life - 1

# To check if it works right, add in game_control.py:
# if event.key == pg.K_k:
#     level.life.decrease()
#     level.hero.life = level.hero.life - 1
