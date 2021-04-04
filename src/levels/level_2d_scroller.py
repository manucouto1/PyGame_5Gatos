from src.levels.level import Level
import pygame as pg
import sys
from extern import parallax as px

from src.menu.menu import PauseMenu
from src.utils import assets


class Scroller2D(Level):

    def __init__(self, builder):
        super().__init__(builder)
        self.load_background()
        self.fullscreen = False
        self.element_click = None
        self.last_scroll_x = 0
        self.last_scroll_y = 0

    def load_background(self, n=6):
        self.bg = px.ParallaxSurface(
            (self.dto.map_width * self.dto.tile_size, self.dto.map_height * self.dto.tile_size), pg.RLEACCEL)
        for i in range(1, n):
            self.bg.add(assets.path_to('levels', self.dto.level_name, self.dto.bg, f"{i}.png"), 6 - i)

    def events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYUP:
                if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                    self.bg.scroll(0)
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_UP, pg.K_w, pg.K_SPACE]:
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

        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            self.hero.move_right()

        (scroll_x, scroll_y) = self.camera.scroll

        if self.last_scroll_x > scroll_x:
            self.bg.scroll(1.5, 'horizontal')
        elif self.last_scroll_x < scroll_x:
            self.bg.scroll(-1.5, 'horizontal')
        else:
            self.bg.scroll(0, 'horizontal')

        self.last_scroll_x = scroll_x


