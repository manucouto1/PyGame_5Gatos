import json
import os
import src.utils.assets as assets
import pygame as pg

from src.sprites.pasive.platforms import Platform
from src.sprites.active.enemy import Enemy
from src.sprites.active.hero import Hero
from src.sprites.custom_groups import CustomGroup
from src.sprites.camera import Camera
from src.sprites.pasive.cursor import Cursor
from src.sprites.active.life import Life
from src.sprites.spritesheet import Spritesheet
from src.sprites.pasive.layers import Layers


class Level:
    def __init__(self, level_name):
        with open(assets.path_to('levels', level_name, level_name + '.txt')) as f:
            config = json.load(f)
            if config is not None:
                self.sheet = Spritesheet(assets.path_to('levels', level_name, f"{level_name}.png"))
                self.tile_size = config["tile_size"]
                self.map_width = config["map_width"]
                self.map_height = config["map_height"]
                self.layers_config = config["layers"]
                self.layers = []
                self.hero = None
                self.camera = None
                self.life = None
                self.layers = Layers(self.layers_config, self.sheet, self.tile_size)
                self.cursor = Cursor(pg.mouse.get_pos())
                self.enemies = CustomGroup()
                self.platforms = CustomGroup()
                self.bullets = CustomGroup()
            else:
                raise ValueError("Problems with level config file")

    def load_hero(self, screen_size):
        self.hero = Hero(32, 64, 16, 8)
        self.life = Life(3, self.hero)
        self.camera = Camera(self.hero, pg.Rect(0, 0, self.map_width * 32, self.map_height * 32), screen_size)

    def load_platforms(self):
        self.platforms.add(self.layers.get_ground())

    def load_dangerous(self):
        self.dangerous.add(self.layers.get_dangerous())

    def load_enemies(self):
        # todo Cargar enemigos desde json
        Enemy(32, 64, 16, 8, self.enemies)

    def update(self):
        pg.sprite.groupcollide(self.bullets, self.platforms, True, False)

        list_remove = list(filter(lambda bll: not self.map_width * 32 > bll.x > 0 or not self.map_height * 32 > bll.y > 0,
                                  self.bullets.sprites()))
        self.bullets.remove(list_remove)

        self.bullets.update()
        self.layers.update()
        self.enemies.update(self.platforms)
        self.camera.update(self.platforms)
        self.cursor.update(pg.mouse.get_pos())
        self.life.update()

    def draw(self, screen):
        self.layers.draw(screen, self.camera.cam)
        self.camera.draw(screen)
        self.life.draw(screen)
        self.cursor.draw(screen)
        self.camera.draw(screen)
        self.bullets.draw(screen, self.camera.cam)
        self.enemies.draw(screen, self.camera.cam)
