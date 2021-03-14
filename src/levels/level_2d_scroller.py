from src.levels.level import Level
import pygame as pg
import sys
import src.utils.assets as assets


class Scroller2D(Level):

    def __init__(self, level_name):
        super().__init__(level_name)
        self.bg = assets.load_image("background.png")

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
                if len(self.bullets) < 5:
                    # look to shoot direction
                    bullet = self.hero.shoot(self.camera)
                    self.bullets.add(bullet)

        pressed = pg.key.get_pressed()

        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            self.hero.move_left()
        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            self.hero.move_right()