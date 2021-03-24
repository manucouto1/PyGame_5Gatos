import pygame as pg
import numpy as np
from src.game.dto.level_dto import LevelDTO
from src.sprites.groups.layers import LayersBuilder
from src.sprites.active.hero import HeroBuilder
from src.sprites.groups.camera import CameraBuilder
from src.sprites.groups.enemies import EnemiesBuilder
from src.sprites.groups.scroll_adjusted import ScrollAdjustedGroup
from src.sprites.pasive.cursor import Cursor
from src.sprites.pasive.event import Item

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

white = (255, 255, 255)

SCREEN_SIZE = pg.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class LevelBuilder:
    def __init__(self, container, level_name):

        self.container = container
        self.level_dto = LevelDTO(level_name)
        self.layers_builder = LayersBuilder(container, self.level_dto)
        self.enemies_builder = EnemiesBuilder(container, self.level_dto)
        self.hero_builder = HeroBuilder(container, self.level_dto)
        self.camera_builder = CameraBuilder(self.level_dto, SCREEN_SIZE)
        self.platforms = pg.sprite.Group()
        self.dangerous = pg.sprite.Group()
        self.h_bullets, self.enemies, self.zone_events = None, None, None
        self.hero, self.camera, self.layers, self.e_bullets = None, None, None, None

    def build(self, player):
        self.hero = self.hero_builder.build(player)
        self.camera = self.camera_builder.build(self.hero)
        self.h_bullets = ScrollAdjustedGroup(self.camera.scroll)
        self.e_bullets = ScrollAdjustedGroup(self.camera.scroll)
        self.container.set_object('e_bullets', self.e_bullets)
        self.container.set_object('hero', self.hero)
        self.enemies = self.enemies_builder.build(self.container, self.camera.scroll)
        self.layers = self.layers_builder.build(self.camera.scroll)
        self.platforms = self.layers.get_ground()
        self.dangerous = self.layers.get_dangerous()

        return self.container.object_from_name(self.level_dto.path, self)


class Level:
    def __init__(self, builder: LevelBuilder):
        self.container = builder.container
        self.screen_rect = pg.Rect(SCREEN_SIZE)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.cursor = Cursor(pg.mouse.get_pos())
        pg.mouse.set_visible(False)

        try:

            self.dto = builder.level_dto
            self.bg = self.container.image_from_parts(self.dto.bg)
            self.layers = builder.layers
            self.enemies = builder.enemies
            self.hero = builder.hero
            self.camera = builder.camera
            self.platforms = builder.platforms
            self.dangerous = builder.dangerous
            self.h_bullets = builder.h_bullets
            self.e_bullets = builder.e_bullets
            self.zone_events = ScrollAdjustedGroup(self.camera.scroll)
            self.zone_events.add(Item(self))

        except IOError:
            print("Level Error")

    def check_bullets_hits(self):
        pg.sprite.groupcollide(self.h_bullets, self.platforms, True, False)
        enemies_damaged = list(pg.sprite.groupcollide(self.h_bullets, self.enemies, True, False).values())
        enemies_damaged = np.array(enemies_damaged).flatten()

        for enemy_hit in enemies_damaged:
            enemy_hit.is_hit()

        list_remove = list(
            filter(lambda bll: not self.dto.map_width * 32 > bll.x > 0 or not self.dto.map_height * 32 > bll.y > 0,
                   self.h_bullets.sprites()))
        self.h_bullets.remove(list_remove)

        pg.sprite.groupcollide(self.e_bullets, self.platforms, True, False)
        list_remove = list(
            filter(lambda bll: not self.dto.map_width * 32 > bll.x > 0 or not self.dto.map_height * 32 > bll.y > 0,
                   self.e_bullets.sprites()))

        self.e_bullets.remove(list_remove)

    def notify(self, event):
        print(event)

    def check_event_reached(self):
        pg.sprite.spritecollide(self.hero, self.zone_events, dokill=True)

    def update(self, dt):
        self.check_bullets_hits()
        self.check_event_reached()

        self.hero.is_hit(self.dangerous)
        self.hero.is_hit(self.enemies)
        self.hero.is_hit(self.e_bullets)

        self.layers.update()
        self.h_bullets.update(dt)
        self.e_bullets.update(dt)
        self.enemies.update(self.platforms, dt)
        self.camera.update(self.platforms, self.dangerous, dt)
        self.cursor.update(pg.mouse.get_pos())

    def map_limit(self):
        (x, y, h, w) = self.screen.get_rect()
        (cam_x, cam_y) = self.camera.camera_rect
        y -= cam_y
        x -= cam_x
        self.hero.rect.clamp_ip((x, y, h, w))

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.map_limit()

        self.layers.draw(self.screen)
        self.enemies.draw(self.screen)
        self.camera.draw(self.screen)
        self.cursor.draw(self.screen)
        self.h_bullets.draw(self.screen)
        self.e_bullets.draw(self.screen)
        self.hero.life.draw(self.screen)
        self.zone_events.draw(self.screen)
