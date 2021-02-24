import json
import os

from platforms import Platform


class Level:
    def __init__(self, level_name):
        with open('..'+os.sep+'assets' + os.sep + level_name + os.sep + level_name + '.txt') as f:
            config = json.load(f)
            if config is not None:
                self.level_name = level_name
                self.tile_size = config["tile_size"]
                self.map_width = config["map_width"]
                self.map_height = config["map_height"]
                self.layers_config = config["layers"]
                self.layers = []
            else:
                raise ValueError("Problems with level config file")
    
    def load_platforms(self, *groups):
        for layer in self.layers_config:
            for position in layer["positions"]:
                Platform(self.level_name, self.tile_size, position["x"], position["y"], position["id"], *groups)
