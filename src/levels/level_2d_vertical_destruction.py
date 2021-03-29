from pygame.sprite import collide_mask

from src.levels.level_2d_scroller import Scroller2D
import pygame as pg


class Scroller2DVerticalDestruction(Scroller2D):
    def __init__(self, builder):
        super().__init__(builder)
        self.falling_platforms = self.layers.get_falling()

    def check_bullets_hits(self):
        super().check_bullets_hits()
        pg.sprite.groupcollide(self.h_bullets, self.falling_platforms, True, False)
        pg.sprite.groupcollide(self.e_bullets, self.falling_platforms, True, False)

    def update(self, dt):
        self.check_bullets_hits()
        self.check_event_reached()

        self.hero.is_hit(self.dangerous)
        self.hero.is_hit(self.enemies)
        self.hero.is_hit(self.e_bullets)
        self.enemies.are_hit(self.dangerous)

        self.h_bullets.update(dt)
        self.e_bullets.update(dt)
        self.enemies.update(self.hero, self.zone_events, self.platforms+self.falling_platforms, dt)
        self.camera.update(self.platforms, self.dangerous, dt, self.falling_platforms)
        self.zone_events.update(dt)
        self.layers.update()
        self.cursor.update(pg.mouse.get_pos())



