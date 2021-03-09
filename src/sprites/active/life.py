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
        self.sprites()[ceil(self.player.life / 2) - 1].update()

    def decrease(self):
        self.sprites()[ceil(self.player.life / 2) - 1].decrease()
    
    def draw(self, win):
        x = 54
        y = 50
        for i in range(self.n_hearts):
            self.sprites()[i].draw(win, 4 +  x * i, y)


# Player:
# get_damage()
# life.decrease()
# life = life - 1