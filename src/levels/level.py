import json
import src.utils.assets as assets
import pygame as pg
from src.sprites.pasive.life import Life
from src.sprites.active.enemy import Enemy
from src.sprites.active.hero import Hero
from src.sprites.groups.custom_groups import CustomGroup
from src.sprites.groups.camera import Camera
from src.sprites.pasive.cursor import Cursor

from src.sprites.spritesheet import Spritesheet
from src.sprites.pasive.layers import Layers
import numpy as np


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

white = (255, 255, 255)

SCREEN_SIZE = pg.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Level:
    def __init__(self, level_name):
        with open(assets.path_to('levels', level_name, level_name + '.txt')) as f:
            config = json.load(f)
            if config is not None:
                self.bg = None
                self.screen_rect = pg.Rect(SCREEN_SIZE)
                self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                self.sheet = Spritesheet(assets.path_to('levels', level_name, f"{level_name}.png"))
                self.tile_size = config["tile_size"]
                self.map_width = config["map_width"]
                self.map_height = config["map_height"]
                self.layers_config = config["layers"]
                self.cursor = Cursor(pg.mouse.get_pos())
                self.hero = None
                self.camera = None
                self.life = None
                self.layers = None
                self.enemies = None
                self.bullets = None
                self.platforms = pg.sprite.Group()
                self.dangerous = pg.sprite.Group()
            else:
                raise ValueError("Problems with level config file")

    def init_level(self, player):
        self.load_hero(player)
        self.load_platforms()
        self.load_enemies()
        self.load_dangerous()

    def load_hero(self, player):
        self.life = Life(3, player)
        self.hero = Hero("Hero_full.png", 32, 32, 0, 8, self.life)
        self.camera = Camera(self.hero, pg.Rect(0, 0, self.map_width * 32, self.map_height * 32), SCREEN_SIZE)
        self.bullets = CustomGroup(self.camera.cam)

    def load_platforms(self):
        self.layers = Layers(self.layers_config, self.sheet, self.tile_size, self.camera.cam)
        self.platforms.add(self.layers.get_ground())

    def load_dangerous(self):
        self.dangerous.add(self.layers.get_dangerous())

    def load_enemies(self):
        # todo Cargar enemigos desde json
        self.enemies = CustomGroup(self.camera.cam)
        Enemy("enemy_full.png", 32, 32, 0, 8, self.enemies)

    def check_bullets_hits(self):
        pg.sprite.groupcollide(self.bullets, self.platforms, True, False)
        enemies_damaged = list(pg.sprite.groupcollide(self.bullets, self.enemies, True, False).values())
        enemies_damaged = np.array(enemies_damaged).flatten()
        for enemy_hit in enemies_damaged:
            enemy_hit.is_hit()

        list_remove = list(
            filter(lambda bll: not self.map_width * 32 > bll.x > 0 or not self.map_height * 32 > bll.y > 0,
                   self.bullets.sprites()))
        self.bullets.remove(list_remove)

    def update(self):
        self.check_bullets_hits()

        # Para los enemigos algo parecido
        self.hero.is_hit(self.dangerous)
        self.hero.is_hit(self.enemies)

        self.bullets.update()
        self.layers.update()
        self.enemies.update(self.platforms)
        self.camera.update(self.platforms, self.dangerous)
        self.cursor.update(pg.mouse.get_pos())

    def map_limit(self):
        screen_rect = self.screen.get_rect()
        screen_rect[2] += self.map_width * self.tile_size - SCREEN_SIZE.x
        self.hero.rect.clamp_ip(screen_rect)

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.map_limit()

        self.layers.draw(self.screen)
        self.camera.draw(self.screen)
        self.cursor.draw(self.screen)
        self.camera.draw(self.screen)
        self.life.draw(self.screen)
        self.bullets.draw(self.screen)
        self.enemies.draw(self.screen)
