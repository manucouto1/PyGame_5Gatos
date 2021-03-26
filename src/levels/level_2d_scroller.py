from src.levels.level import Level
import pygame as pg
import sys


class Scroller2D(Level):

    def __init__(self, level_name):
        super().__init__(level_name)
        self.fullscreen = False

    def events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.VIDEORESIZE:
                if not self.fullscreen:
                    self.screen = pg.display.set_mode((event.w, event.h), pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
                    self.screen_rect = self.screen.get_rect()
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_UP, pg.K_w, pg.K_SPACE]:
                    self.hero.jump()
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_f:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pg.display.set_mode(self.monitor_size, pg.HWSURFACE | pg.DOUBLEBUF | pg.FULLSCREEN)
                        self.screen_rect = self.screen.get_rect()
                    else:
                        self.screen = pg.display.set_mode((self.screen.get_width(), self.screen.get_height()),
                                                          pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
                        self.screen_rect = self.screen.get_rect()

            if event.type == pg.MOUSEBUTTONDOWN:
                if len(self.h_bullets) < 5:
                    x, y = pg.mouse.get_pos()
                    # bullet = self.hero.shoot((x - 15, y - 15))
                    bullet = self.hero.shoot((x - self.dto.tile_size / 2, y - self.dto.tile_size / 2))
                    self.h_bullets.add(bullet)

        pressed = pg.key.get_pressed()

        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            self.hero.move_left()
        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            self.hero.move_right()
