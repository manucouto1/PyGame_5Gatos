from  spritesheet import Spritesheet
from platforms import Platform

import pygame as pg
import os

class Layer():

    def __init__(self, name, level_name, positions, tile_size, *groups):
        self.name = name
        self.plataforms_list = []

        for position in positions:
            self.plataforms_list.append()
