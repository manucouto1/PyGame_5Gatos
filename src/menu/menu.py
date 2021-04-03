import pygame as pg
from src.levels.level import LevelBuilder
from src.menu.screen import ScreenGUIInitial, ScreenGUIGameOver, ScreenGUIPause
from src.menu.screen import ScreenGUIControls
from src.menu.screen import ScreenGUIOptions
from src.menu.screen import ScreenGUILevels


class Menu:

    def __init__(self, director):
        self.current_screen = -1
        self.director = director
        self.mixer = director.container.get_object('mixer')
        self.scenes_list = []
        self.scenes_list.append(ScreenGUIInitial(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIControls(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIOptions(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUILevels(self, "menu/menu_background.png"))
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
        game = self.director.container.get_object('game')
        self.director.container.get_object('mixer').load_music(game.music["menu"])
        self.director.container.get_object('mixer').load_new_profile(game.sounds["menu"])
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

    def execute_level(self, level):
        container = self.director.container
        self.mixer.play_button_click()

        game = self.director.game

        self.director.stack_scene(LevelBuilder(container, game.levels[level]))

    def show_initial_screen(self):
        self.current_screen = 0

    def show_controls_screen(self):
        self.current_screen = 1

    def show_options_screen(self):
        self.current_screen = 2

    def show_levels_screen(self):
        self.current_screen = 3

    def music_louder(self):
        self.mixer.music_louder()

    def music_lower(self):
        self.mixer.music_lower()

    def sound_louder(self):
        self.mixer.sound_louder()

    def sound_lower(self):
        self.mixer.sound_lower()


class GameOverMenu:
    def __init__(self, director):
        self.director = director
        self.mixer = director.container.get_object('mixer')
        self.screen = ScreenGUIGameOver(self, "menu/menu_background.png")

    def draw(self):
        self.screen.draw()

    def exit_program(self):
        self.director.exit_program()

    def execute_game(self):
        container = self.director.container
        self.mixer.play_button_click()
        game = self.director.game
        for level in game.levels:
            self.director.stack_scene(LevelBuilder(container, level))

    def build(self, _):
        game = self.director.container.get_object('game')
        self.director.container.get_object('mixer').load_music(game.music["game_over"])
        self.director.container.get_object('mixer').load_new_profile(game.sounds["game_over"])
        return self

    def events(self, events):
        if not pg.mouse.get_visible():
            pg.mouse.set_visible(True)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.exit_program()
            elif event.type == pg.QUIT:
                self.director.exit_program()
        self.screen.events(events)

    def update(self, *args):
        return


class PauseMenu:

    def __init__(self, director):
        self.current_screen = -1
        self.director = director
        self.mixer = director.container.get_object('mixer')
        self.scenes_list = []
        self.scenes_list.append(ScreenGUIPause(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIControls(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIOptions(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUILevels(self, "menu/menu_background.png"))
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
                    self.resume_game()
            elif event.type == pg.QUIT:
                self.director.exit_program()
        self.scenes_list[self.current_screen].events(events)

    def build(self, _):
        game = self.director.container.get_object('game')
        self.director.container.get_object('mixer').load_music(game.music["menu"])
        self.director.container.get_object('mixer').load_new_profile(game.sounds["menu"])
        self.show_initial_screen()
        return self

    def draw(self):
        self.scenes_list[self.current_screen].draw()

    def quit_game(self):
        self.director.exit_program()
        self.director.stack_scene(Menu(self.director))

    def resume_game(self):
        self.mixer.play_button_click()
        self.director.exit_scene()

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