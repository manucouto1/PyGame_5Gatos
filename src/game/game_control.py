import sys
import pygame as pg
import src.utils.assets as assets
from src.game.player import Player
from src.levels.level import Level

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

        self.clock = pg.time.Clock()
        self.bg = pg.image.load(assets.path_to("background.png"))
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.actual_level = 0
        self.player = Player()
        self.levels = [Level("level1")]

    def control(self):
        level = self.levels[self.actual_level]
        hero = level.hero
        camera = level.camera

        self.screen.blit(self.bg, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                # conditions for double jumping
                if event.key in [pg.K_UP, pg.K_w, pg.K_SPACE]:
                    hero.jump()
            if event.type == pg.MOUSEBUTTONDOWN:
                # mouse shutting
                if len(level.bullets) < 5:
                    # look to shoot direction
                    bullet = hero.shoot(camera)
                    level.bullets.add(bullet)

        pressed = pg.key.get_pressed()

        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            hero.move_left()
        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            hero.move_right()

        screen_rect = self.screen.get_rect()
        screen_rect[2] += level.map_width * level.tile_size - SCREEN_WIDTH
        hero.rect.clamp_ip(screen_rect)

        self.clock.tick(FPS)

    def init_level(self):
        self.levels[self.actual_level].load_platforms()
        self.levels[self.actual_level].load_dangerous()
        self.levels[self.actual_level].load_enemies()
        self.levels[self.actual_level].load_hero(SCREEN_SIZE, self.player)

    def update(self):
        self.levels[self.actual_level].update()

    def draw(self):
        self.levels[self.actual_level].draw(self.screen)
