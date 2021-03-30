import pygame as pg
from src.levels.level import LevelBuilder
from src.menu.screen import ScreenGUIInitial
from src.menu.screen import ScreenGUIControls
from src.menu.screen import ScreenGUIOptions
from src.sprites.passive.cursor import Cursor

MAX_VOLUME = 0.8


class Menu:

    def __init__(self, director):
        self.current_screen = -1
        self.director = director
        self.mixer = director.container.get_object('mixer')
        self.scenes_list = []
        self.scenes_list.append(ScreenGUIInitial(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIControls(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIOptions(self, "menu/menu_background.png"))
        self.cursor = Cursor(director.container, pg.mouse.get_pos())
        self.show_initial_screen()

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
        self.scenes_list[self.current_screen].events(events)

    def build(self, _):
        sounds_profile = self.director.container.get_object('game').sounds["menu"]
        self.director.container.get_object('mixer').load_music("menu.ogg")
        self.director.container.get_object('mixer').load_new_profile(sounds_profile)
        self.show_initial_screen()
        return self

    def draw(self):
        self.scenes_list[self.current_screen].draw()

    def exit_program(self):
        self.director.exit_program()

    def execute_game(self):
        container = self.director.container
        self.mixer.play_button_click()

        game = self.director.game

        for level in game.levels:
            self.director.stack_scene(LevelBuilder(container, level))

    def show_initial_screen(self):
        self.current_screen = 0

    def show_controls_screen(self):
        self.current_screen = 1

    def show_options_screen(self):
        self.current_screen = 2

    def music_louder(self):
        self.mixer.music_louder()

    def music_lower(self):
        self.mixer.music_lower()

    def sound_louder(self):
        self.mixer.sound_louder()

    def sound_lower(self):
        self.mixer.sound_lower()