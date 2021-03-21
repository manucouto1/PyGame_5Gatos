import pygame as pg
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
        pg.mixer.music.load("sounds/menu.ogg")
        self.init_sound = pg.mixer.Sound("sounds/init_game.wav")
        pg.mixer.music.play(-1)

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
        pg.mixer.music.stop()
        self.init_sound.play()
        pg.mixer.music.load("sounds/game.ogg")
        pg.mixer.music.play(-1)
        self.director.stack_scene(Scroller2D("level1"))

    def show_initial_scene(self):
        self.initial_scene = 0

    # def show_configuration_scene(self):
    #    self.configuration_scene = 1
