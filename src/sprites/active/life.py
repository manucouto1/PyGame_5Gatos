import pygame as pg
from src.sprites.spritesheet import Spritesheet
import src.utils.assets as assets
from src.sprites.active.hearts import Heart
from math import ceil

class Life(pg.sprite.Group):
    def __init__(self, n_hearts, player):
        sheet = Spritesheet(assets.path_to("player", "Corazon-Sheet.png"))
        hearts = []
        self.player = player
        pos = ceil(self.player.life / 2) - 1
        
        # Necessary when updating a decreasing heart
        self.decreasing = False
        self.animation = 0

        # Full hearts
        for _ in range(pos):
            hearts.append(Heart(sheet, 0))
        
        # Check actual player life
        hearts.append(Heart(sheet, self.player.life % 2))
        
        #Empty hearts
        for _ in range(pos+1, n_hearts):
            hearts.append(Heart(sheet, 2))
        
        super().__init__(hearts)
        self.n_hearts = n_hearts

    def update(self):
        # When decreasing, it's necessary to increase player.life by 1
        # to update the correct heart. This lasts for 'animation' frames.
        if self.decreasing:
            pos = ceil((self.player.life + 1) / 2) - 1
            self.animation = self.animation - 1
            if self.animation == 0:
                self.decreasing = False
        else:
            pos = ceil(self.player.life / 2) - 1
        self.sprites()[pos].update()
        

    def decrease(self):
        self.sprites()[ceil(self.player.life / 2) - 1].decrease()
        self.decreasing = True
        self.animation = self.sprites()[ceil(self.player.life / 2) - 1].animation
    
    def draw(self, win):
        x = 54
        y = 50
        for i in range(self.n_hearts):
            self.sprites()[i].draw(win, 4 +  x * i, y)


# Player:
# get_damage()
# life.decrease()
# life = life - 1

# To check if it works right, add in game_control.py:
# if event.key == pg.K_k:
#     level.life.decrease()
#     level.hero.life = level.hero.life - 1