from src.levels.level import Level
import pygame as pg
import sys


class Scroller2D(Level):

    def __init__(self, level_name):
        super().__init__(level_name)

    def events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                # conditions for double jumping
                if event.key in [pg.K_UP, pg.K_w, pg.K_SPACE]:
                    self.hero.jump()
            if event.type == pg.MOUSEBUTTONDOWN:
                # mouse shutting
                if len(self.h_bullets) < 5:
                    # look to shoot direction
                    x, y = pg.mouse.get_pos()
                    bullet = self.hero.shoot((x - 15, y - 15))
                    self.h_bullets.add(bullet)

        pressed = pg.key.get_pressed()

        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            self.hero.move_left()
        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            self.hero.move_right()
