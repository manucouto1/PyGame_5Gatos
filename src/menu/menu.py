import pygame as pg

from src.levels.level import LevelBuilder
from src.menu.screen import ScreenGUIInitial
from src.sprites.passive.cursor import Cursor
import src.utils.assets as assets


class Menu:

    def __init__(self, director):
        self.initial_scene = -1
        self.director = director
        self.scenes_list = []
        self.scenes_list.append(ScreenGUIInitial(self, "background2.png"))
        self.cursor = Cursor(director.container, pg.mouse.get_pos())
        self.show_initial_scene()

        pg.mixer.music.load(assets.path_to("sounds", "menu.ogg"))
        self.init_sound = pg.mixer.Sound(assets.path_to("sounds", "init_game.wav"))
        pg.mixer.music.play(-1)

    # static menu
    def update(self, *args):
        return

    def events(self, events):
        if not pg.mouse.get_visible():
            pg.mouse.set_visible(True)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.exit_program()
            elif event.type == pg.QUIT:
                self.director.exit_program()
        self.scenes_list[self.initial_scene].events(events)

    def build(self, _):
        self.show_initial_scene()
        return self

    def draw(self):
        self.scenes_list[self.initial_scene].draw()

    def exit_program(self):
        self.director.exit_program()

    def execute_game(self):
        pg.mixer.music.stop()
        self.init_sound.play()
        pg.mixer.music.load(assets.path_to("sounds", "game.ogg"))
        pg.mixer.music.play(-1)
        container = self.director.container
        game = self.director.game

        for level in game.levels:
            self.director.stack_scene(LevelBuilder(container, level))

    def show_initial_scene(self):
        self.initial_scene = 0
