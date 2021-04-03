import pygame as pg

from pygame.sprite import collide_mask

from src.menu.button import ButtonPause
from src.menu.menu import GameOverMenu
from src.sprites.groups.events import EventsBuilder
from src.sprites.groups.platforms import Platforms
from src.sprites.groups.layers import LayersBuilder
from src.sprites.active.hero import HeroBuilder
from src.sprites.groups.camera import CameraBuilder
from src.sprites.groups.enemies import EnemiesBuilder
from src.sprites.groups.scroll_adjusted import ScrollAdjustedGroup
from src.sprites.passive.cursor import Cursor

white = (255, 255, 255)


class LevelBuilder:
    def __init__(self, container, level_dto):
        container.set_object('level_dto', level_dto)
        self.container = container
        self.game_dto = container.get_object("game")
        self.screen_size = pg.Rect((0, 0, self.game_dto.screen_width, self.game_dto.screen_height))
        self.level_dto = level_dto
        self.layers_builder = LayersBuilder(container, self.level_dto)
        self.enemies_builder = EnemiesBuilder(container, self.level_dto)
        self.hero_builder = HeroBuilder(container, self.level_dto)
        self.camera_builder = CameraBuilder(container, self.level_dto, self.screen_size)
        self.zone_events_builder = EventsBuilder(container, self.level_dto)
        self.h_bullets, self.e_bullets, self.camera, self.hero = None, None, None, None
        self.level_sounds = self.game_dto.sounds[level_dto.sounds]
        self.level_music = self.game_dto.music[level_dto.music]

    def build(self, player):
        self.hero = self.hero_builder.build(player)
        self.camera = self.camera_builder.build(self.hero)
        self.h_bullets = ScrollAdjustedGroup(self.camera.scroll)
        self.e_bullets = ScrollAdjustedGroup(self.camera.scroll)
        self.container.set_object('e_bullets', self.e_bullets)
        self.container.set_object('h_bullets', self.h_bullets)
        self.container.set_object('hero', self.hero)
        return self.container.object_from_name(self.level_dto.path, self)


class Level:
    def __init__(self, builder: LevelBuilder):
        self.container = builder.container
        self.container.set_object('level', self)
        self.screen_rect = builder.screen_size
        self.monitor_size = [pg.display.Info().current_w, pg.display.Info().current_h]
        self.screen = pg.display.set_mode((builder.game_dto.screen_width, builder.game_dto.screen_height), pg.HWSURFACE | pg.DOUBLEBUF)
        self.cursor = Cursor(self.container, pg.mouse.get_pos())
        pg.mouse.set_visible(False)
        self.screen.set_alpha(None)
        self.pause = ButtonPause(self, (600, 80))

        try:
            self.bg = None
            self.dto = builder.level_dto
            self.limit = self.dto.map_height * self.dto.tile_size
            self.hero = builder.hero
            self.camera = builder.camera
            self.layers = builder.layers_builder.build(self.camera.scroll)
            self.enemies = builder.enemies_builder.build(self.camera.scroll)
            self.platforms = Platforms(builder.game_dto, self.layers.get_ground())
            self.dangerous = Platforms(builder.game_dto, self.layers.get_dangerous())
            self.falling_platforms = Platforms(builder.game_dto, self.layers.get_falling())
            self.h_bullets = builder.h_bullets
            self.e_bullets = builder.e_bullets

            self.zone_events = builder.zone_events_builder.build(self, self.camera.scroll)
            self.container.get_object('mixer').load_new_profile(builder.level_sounds)
            self.container.get_object('mixer').load_music(builder.level_music)

        except IOError as ex:
            print("Level Error > ", ex)

    def check_limits(self, bll):
        return not self.dto.map_width * self.dto.tile_size > bll.x > 0 or \
               not self.dto.map_height * self.dto.tile_size > bll.y > 0

    def check_bullets_hits(self):
        pg.sprite.groupcollide(self.h_bullets, self.platforms.get_actives(), True, False)
        pg.sprite.groupcollide(self.e_bullets, self.platforms.get_actives(), True, False)

        pg.sprite.groupcollide(self.h_bullets, self.falling_platforms.get_actives(), True, False, collided=collide_mask)
        pg.sprite.groupcollide(self.e_bullets, self.falling_platforms.get_actives(), True, False, collided=collide_mask)

        self.hero.is_hit_destroy(self.e_bullets)
        self.enemies.are_shot(self.h_bullets)

    def next_level(self):
        director = self.container.get_object('director')
        director.exit_scene()

    def check_event_reached(self):
        pg.sprite.spritecollide(self.hero, self.zone_events, dokill=True)

    def update(self, dt):
        self.check_bullets_hits()
        self.check_event_reached()

        self.hero.is_hit(self.dangerous.get_actives())
        self.hero.is_hit(self.enemies)
        self.hero.is_hit(self.e_bullets)
        self.enemies.are_hit(self.dangerous.get_actives())

        self.h_bullets.update(dt)
        self.e_bullets.update(dt)
        active_platforms = Platforms.get_sprites(self.platforms.get_actives(), self.falling_platforms.get_actives())
        self.enemies.update(self.hero, self.zone_events, active_platforms, dt)
        self.camera.update(self.platforms.get_actives(), self.dangerous.get_actives(), dt, self.falling_platforms.get_actives())

        self.platforms.update(self.camera)
        self.dangerous.update(self.camera)
        self.falling_platforms.update(self.camera)
        self.zone_events.update(dt)
        self.layers.update()
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
        self.camera.draw(self.screen)
        self.pause.draw(self.screen)
        self.cursor.draw(self.screen)
        self.h_bullets.draw(self.screen)
        self.e_bullets.draw(self.screen)
        self.hero.life.draw(self.screen)
        self.hero.points.draw(self.screen)
        self.zone_events.draw(self.screen)

        director = self.container.get_object('director')
        if director.player.life == 0:
            director.player.reset()
            director.change_scene(GameOverMenu(director).build(None))
