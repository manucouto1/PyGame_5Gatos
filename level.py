import pygame as pg
import platforms
import json
import os

from  layers import Layer

class Level():

    def __init__(self, level_name):
        with open('assets'+os.sep+level_name+os.sep+level_name+'.txt') as f:
            config = json.load(f)
            if config is not None:
                self.tile_size = config["tile_size"]
                self.map_width = config["map_width"]
                self.map_height = config["map_height"]
                self.layers = []
                for layer in config["layers"]:
                    self.layers.append(Layer(layer["name"], level_name, layer["positions"], self.tile_size))
            else:
                raise ValueError("Problems with lavel config file")
    
    def update(self):
        for layer in self.layers:
            layer.update()
    
    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)
    