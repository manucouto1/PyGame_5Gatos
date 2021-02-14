import pygame as pg
from  spritesheet import Spritesheet
import os

class Platform(pg.sprite.Sprite):

    def __init__(self, level_name, tile_size, x, y, id):
        super().__init__()

        self.sheet = Spritesheet("assets"+os.sep+level_name+os.sep+level_name+".png")
        self.rect = pg.Rect(id*tile_size, 0, tile_size, tile_size)
        #Esto me vuelve loco, cuando se le pasa el rectángulo a sheet.image_at seleccionas de la imagen la posición del tile que cogemos
        self.image = self.sheet.image_at(self.rect)
        #Pero aquí le indicamos la posición en la pantalla ???!!?!?!?!
        self.rect.x = x*tile_size
        self.rect.y = y*tile_size