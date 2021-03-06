import time

from src.levels.level import Level
from src.extern import parallax as px
from src.menu.menu import PauseMenu, GameOverMenu
from src.utils import assets

import pygame as pg
import sys


class VerticalScroller(Level):
    def __init__(self, builder):
        super().__init__(builder)
        self.load_background()
        self.fullscreen = False
        self.element_click = None
        self.last_scroll_x = 0
        self.last_scroll_y = 0
        self.falling = False
        self.block_right = False
        self.time_to_fall = False
        self.final_boos = self.enemies.get_final_boss()


    def load_background(self, n=6):
        self.bg = px.ParallaxSurface(
            (self.dto.map_width * self.dto.tile_size, self.dto.map_height * self.dto.tile_size), pg.RLEACCEL)
        for i in range(1, n):
            self.bg.add(assets.path_to('levels', self.dto.level_name, self.dto.bg, f"{i}.png"), (n - i))

    def normal_mode(self):
        self.enemies.on_gravity()
        self.hero.on_gravity()
        self.camera.normal_mode()
        self.falling = False

    def clear_mode(self):
        self.block_right = False
        self.camera.normal_mode()

    def falling_mode(self):
        if self.time_to_fall:
            self.enemies.shutdown_gravity(1.5)
            self.hero.shutdown_gravity(2.5)
            self.camera.falling_mode()
            self.falling = True
            self.block_right = False
        else:
            self.camera.active_id = -1
            self.hero.choose_mov(True, False)
            self.hero.getting_damage = True
            self.hero.jump()
            self.hero.num_jumps = 0
            self.block_right = True



    def enemy_limit(self, enemy):
        (x, y, h, w) = self.screen.get_rect()
        y += 32
        x += 32
        h -= 32
        w -= 32
        (cam_x, cam_y) = self.camera.camera_rect
        y -= cam_y
        x -= cam_x
        enemy.rect.clamp_ip((x, y, h, w))

    def events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYUP:
                if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                    self.bg.scroll(0)
                if event.key in [pg.K_UP | pg.K_w | pg.K_DOWN | pg.K_s]:
                    self.hero.reset_movement()
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_UP, pg.K_w, pg.K_SPACE]:
                    if not self.falling:
                        self.hero.jump()
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                self.element_click = None
                if len(self.h_bullets) < 5:
                    x, y = pg.mouse.get_pos()
                    self.hero.shoot((x - self.hero.rect.width / 2, y - self.hero.rect.height / 2))
                if self.pause.position_elem(event.pos):
                    self.element_click = self.pause
            if event.type == pg.MOUSEBUTTONUP:
                if self.pause.position_elem(event.pos):
                    if self.pause == self.element_click:
                        director = self.container.get_object('director')
                        director.stack_scene(PauseMenu(director))

        pressed = pg.key.get_pressed()

        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            self.hero.move_left()

        if (pressed[pg.K_RIGHT] or pressed[pg.K_d]) and not self.block_right:
            self.hero.move_right()

        if self.falling:
            if pressed[pg.K_UP] or pressed[pg.K_w]:
                self.hero.move_up()
            if pressed[pg.K_DOWN] or pressed[pg.K_s]:
                self.hero.move_down()

        (scroll_x, scroll_y) = self.camera.scroll

        if self.last_scroll_y > scroll_y:
            self.bg.scroll(-10, 'vertical')
        elif self.last_scroll_y < scroll_y:
            self.bg.scroll(10, 'vertical')

        if self.last_scroll_x > scroll_x:
            self.bg.scroll(1.5, 'horizontal')
        elif self.last_scroll_x < scroll_x:
            self.bg.scroll(-1.5, 'horizontal')

        self.last_scroll_x = scroll_x
        self.last_scroll_y = scroll_y
