import pygame as pg

from game.director import Director
from src.menu.screen import ScreenGUIInitial
from src.sprites.pasive.cursor import Cursor
from src.levels.level_2d_scroller import Scroller2D


class Menu:

    def __init__(self, director):
        pg.mouse.set_visible(True)

        self.director = director
        self.scenes_list = []
        self.scenes_list.append(ScreenGUIInitial(self, "background2.png"))
        self.cursor = Cursor(pg.mouse.get_pos())
        self.show_initial_scene()

    # static menu
    def update(self, *args):
        return

    def events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.exit_program()
            elif event.type == pg.QUIT:
                self.director.exit_program()
        self.scenes_list[self.initial_scene].events(events)

    def init_level(self, player):
        self.show_initial_scene()

    def draw(self):
        self.scenes_list[self.initial_scene].draw()

    def exit_program(self):
        self.director.exit_program()

    def execute_game(self):
        self.director.change_scene(Scroller2D("level1"))

    def show_initial_scene(self):
        self.initial_scene = 0


class Pause(Menu):
    def __init__(self, curr):
        super().__init__(Director())
        self.curr = curr

    def execute_game(self):
        self.director.stack_scene()(self.curr)

    # def show_configuration_scene(self):
    #    self.configuration_scene = 1
