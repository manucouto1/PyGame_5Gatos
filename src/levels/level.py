import pygame as pg
import parallax as px
from pygame.sprite import collide_mask

from src.sprites.groups.Events import EventsBuilder
from src.sprites.groups.layers import LayersBuilder
from src.sprites.active.hero import HeroBuilder
from src.sprites.groups.camera import CameraBuilder
from src.sprites.groups.enemies import EnemiesBuilder
from src.sprites.groups.scroll_adjusted import ScrollAdjustedGroup
from src.sprites.passive.cursor import Cursor
from src.utils import assets

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

white = (255, 255, 255)

SCREEN_SIZE = pg.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class LevelBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        self.level_dto = level_dto
        self.layers_builder = LayersBuilder(container, self.level_dto)
        self.enemies_builder = EnemiesBuilder(container, self.level_dto)
        self.hero_builder = HeroBuilder(container, self.level_dto)
        self.camera_builder = CameraBuilder(container, self.level_dto, SCREEN_SIZE)
        self.zone_events_builder = EventsBuilder(container, self.level_dto)
        self.platforms = pg.sprite.Group()
        self.dangerous = pg.sprite.Group()
        self.h_bullets, self.enemies, self.e_bullets, self.camera = None, None, None, None
        self.hero, self.a, self.layers, self.zone_events = None, None, None, None
        self.level_sounds = container.get_object("game").sounds[level_dto.sounds]
        self.level_music = container.get_object("game").music[level_dto.music]

    def build(self, player):
        self.hero = self.hero_builder.build(player)
        self.camera = self.camera_builder.build(self.hero)
        self.h_bullets = ScrollAdjustedGroup(self.camera.scroll)
        self.e_bullets = ScrollAdjustedGroup(self.camera.scroll)
        self.container.set_object('e_bullets', self.e_bullets)
        self.container.set_object('hero', self.hero)
        self.enemies = self.enemies_builder.build(self.camera.scroll)
        self.layers = self.layers_builder.build(self.camera.scroll)
        self.platforms = self.layers.get_ground()
        self.dangerous = self.layers.get_dangerous()
        return self.container.object_from_name(self.level_dto.path, self)


class Level:
    def __init__(self, builder: LevelBuilder):
        self.container = builder.container
        self.screen_rect = pg.Rect(SCREEN_SIZE)
        self.monitor_size = [pg.display.Info().current_w, pg.display.Info().current_h]
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
        self.cursor = Cursor(self.container, pg.mouse.get_pos())
        pg.mouse.set_visible(False)

        try:
            self.dto = builder.level_dto
            self.limit = self.dto.map_height * self.dto.tile_size
            self.bg = px.ParallaxSurface(
                (self.dto.map_width * self.dto.tile_size, self.dto.map_height * self.dto.tile_size), pg.RLEACCEL)
            for i in range(1, 6):
                self.bg.add(assets.path_to('levels', self.dto.level_name, self.dto.bg, f"{i}.png"), 6 - i)
            self.layers = builder.layers
            self.enemies = builder.enemies
            self.hero = builder.hero
            self.camera = builder.camera
            self.platforms = builder.platforms
            self.dangerous = builder.dangerous
            self.h_bullets = builder.h_bullets
            self.e_bullets = builder.e_bullets
            self.zone_events = builder.zone_events_builder.build(self, self.camera.scroll)
            self.dead_enemies = ScrollAdjustedGroup(self.camera.scroll)
            self.container.set_object('zone_events', self.zone_events)
            self.container.get_object('mixer').load_new_profile(builder.level_sounds)
            self.container.get_object('mixer').load_music(builder.level_music)

        except IOError:
            print("Level Error")

    def check_limits(self, bll):
        return not self.dto.map_width * self.dto.tile_size > bll.x > 0 or \
               not self.dto.map_height * self.dto.tile_size > bll.y > 0

    def check_bullets_hits(self):
        pg.sprite.groupcollide(self.h_bullets, self.platforms, True, False, collided=collide_mask)
        enemies_hits = pg.sprite.groupcollide(self.h_bullets, self.enemies, True, False)
        for bullet, enemies_damaged in enemies_hits.items():
            for enemy_hit in enemies_damaged:
                enemy_hit.is_shoot(bullet)
                if enemy_hit.life == 0:
                    self.enemies.remove(enemy_hit)
                    self.dead_enemies.add(enemy_hit)

        self.h_bullets.remove(list(filter(self.check_limits, self.h_bullets.sprites())))
        self.hero.is_hit_destroy(self.e_bullets)

        pg.sprite.groupcollide(self.e_bullets, self.platforms, True, False, collided=collide_mask)
        self.e_bullets.remove(list(filter(self.check_limits, self.e_bullets.sprites())))

    def notify(self, event):
        print(event)

    def next_level(self):
        director = self.container.get_object('director')
        director.exit_scene()

    def check_event_reached(self):
        pg.sprite.spritecollide(self.hero, self.zone_events, dokill=True)

    def update(self, dt):
        self.check_bullets_hits()
        self.check_event_reached()

        self.hero.is_hit(self.dangerous)
        self.hero.is_hit(self.enemies)
        self.hero.is_hit(self.e_bullets)
        self.enemies.is_hit(self.dangerous)

        self.h_bullets.update(dt)
        self.e_bullets.update(dt)

        self.layers.update(dt, self.camera.world_size.size, self.hero)
        self.enemies.update(self.platforms, dt)
        self.dead_enemies.update(self.platforms, dt)
        self.camera.update(self.platforms, self.dangerous, dt)
        self.cursor.update(pg.mouse.get_pos())

    def map_limit(self):
        (x, y, h, w) = self.screen.get_rect()
        (cam_x, cam_y) = self.camera.camera_rect
        y -= cam_y
        x -= cam_x
        self.hero.rect.clamp_ip((x, y, h, w))

    def draw(self):
        self.bg.draw(self.screen)
        self.map_limit()
        self.layers.draw(self.screen)
        self.enemies.draw(self.screen)
        self.dead_enemies.draw(self.screen)
        self.camera.draw(self.screen)
        self.cursor.draw(self.screen)
        self.h_bullets.draw(self.screen)
        self.e_bullets.draw(self.screen)
        self.hero.life.draw(self.screen)
        self.zone_events.draw(self.screen)
