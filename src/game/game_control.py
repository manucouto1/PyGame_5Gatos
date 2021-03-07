import sys
import pygame as pg
import src.utils.assets as assets
from levels.testLevel import TestLevel

from src.game.level import Level

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

white = (255, 255, 255)

SCREEN_SIZE = pg.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 20


class GameControl:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        pg.display.set_caption("tutorial pygame parte 2")

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_level = 0
        # TODO cargar levels desde json
        self.levels = [TestLevel(), TestLevel()]

    def control(self):
        level = self.levels[self.current_level]
        player = level.player
        camera = level.camera

        self.screen.blit(self.levels[self.current_level].bg, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                # conditions for double jumping
                if event.key in [pg.K_UP, pg.K_w, pg.K_SPACE]:
                    player.jump()
            if event.type == pg.MOUSEBUTTONDOWN:
                # mouse shutting
                if len(level.bullets) < 5:
                    # look to shoot direction
                    bullet = player.shoot(camera)
                    level.bullets.add(bullet)

        pressed = pg.key.get_pressed()

        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            player.move_left()
        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            player.move_right()

        screen_rect = self.screen.get_rect()
        screen_rect[2] += level.map_width * level.tile_size - SCREEN_WIDTH
        player.rect.clamp_ip(screen_rect)

    def init_level(self):
        self.levels[self.current_level].load_player(SCREEN_SIZE)
        self.levels[self.current_level].load_platforms()
        self.levels[self.current_level].load_enemies()

    def update(self):
        self.levels[self.current_level].update()

    def draw(self):
        self.levels[self.current_level].draw(self.screen)
