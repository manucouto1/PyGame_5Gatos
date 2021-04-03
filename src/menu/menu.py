import pygame as pg
from src.menu.screen import ScreenGUIInitial, ScreenGUIGameOver, ScreenGUIPause
from src.menu.screen import ScreenGUIControls
from src.menu.screen import ScreenGUIOptions
from src.menu.screen import ScreenGUILevels


class Menu:
    """
    Class to create menu scenes

    :param director: Application director
    """
    def __init__(self, director):
        self.current_screen = -1
        self.director = director
        self.mixer = director.container.get_object('mixer')
        self.scenes_list = []

    def update(self, *args):
        """
        Update of the scene does nothing, since menu scenes are static
        """
        return

    def events(self, events):
        """
        Pass keyboard events to the current screen
        """
        if not pg.mouse.get_visible():
            pg.mouse.set_visible(True)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.exit_program()
            elif event.type == pg.QUIT:
                self.director.exit_program()
        self.scenes_list[self.current_screen].events(events)

    def build(self):
        """
        Build scene
        """
        game = self.director.container.get_object('game')
        self.director.container.get_object('mixer').load_music(game.music["menu"])
        self.director.container.get_object('mixer').load_new_profile(game.sounds["menu"])
        self.show_initial_screen()
        return self

    def draw(self):
        """
        Draw current screen
        """
        self.scenes_list[self.current_screen].draw()

    def exit_program(self):
        """
        Method that exits the game and closes window
        """
        self.director.exit_program()

    def show_initial_screen(self):
        """
        Method that changes current screen to the initial screen
        """
        self.current_screen = 0


class InitialMenu(Menu):
    """
    Initial menu scene
    """
    def __init__(self, director):
        Menu.__init__(self, director)
        self.scenes_list.append(ScreenGUIInitial(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIControls(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIOptions(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUILevels(self, "menu/menu_background.png"))
        self.show_initial_screen()

    def execute_game(self):
        """
        Method that executes the game
        """
        container = self.director.container
        self.mixer.play_button_click()

        game = self.director.game

        for level in range(len(game.levels)):
            self.director.stack_scene(container.get_object('levels')[level])

    def execute_level(self, level):
        """
        Method that executes a level

        param level: level number
        """
        container = self.director.container
        self.mixer.play_button_click()

        self.director.stack_scene(container.get_object('levels')[level])

    def show_controls_screen(self):
        """
        Method that changes current screen to the controls screen
        """
        self.current_screen = 1

    def show_options_screen(self):
        """
        Method that changes current screen to the options screen
        """
        self.current_screen = 2

    def show_levels_screen(self):
        """
        Method that changes current screen to the levels screen
        """
        self.current_screen = 3

    def music_louder(self):
        """
        Method that increases the volume of the music
        """
        self.mixer.music_louder()

    def music_lower(self):
        """
        Method that reduces the volume of the music
        """
        self.mixer.music_lower()

    def sound_louder(self):
        """
        Method that increases the volume of the sounds
        """
        self.mixer.sound_louder()

    def sound_lower(self):
        """
        Method that reduces the volume of the sounds
        """
        self.mixer.sound_lower()


class GameOverMenu(Menu):
    """
    Game Over menu scene
    """
    def __init__(self, director):
        Menu.__init__(self, director)
        self.scenes_list.append(ScreenGUIGameOver(self, "menu/game_over_background.png"))
        self.show_initial_screen()

    def execute_game(self):
        """
        Method that executes the game
        """
        container = self.director.container
        self.mixer.play_button_click()
        for level in container.get_object('levels'):
            self.director.stack_scene(level)

    def quit_game(self):
        """
        Button that finish game execution and changes to menu scene
        """
        self.director.exit_program()
        self.director.player.reset()
        self.director.stack_scene(InitialMenu(self.director).build())


class PauseMenu(Menu):
    """
    Pause menu scene
    """
    def __init__(self, director):
        Menu.__init__(self, director)
        self.scenes_list.append(ScreenGUIPause(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIControls(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUIOptions(self, "menu/menu_background.png"))
        self.scenes_list.append(ScreenGUILevels(self, "menu/menu_background.png"))
        self.show_initial_screen()

    def quit_game(self):
        """
        Method that finish game execution and changes to menu scene
        """
        self.director.exit_program()
        self.director.player.reset()
        self.director.stack_scene(InitialMenu(self.director).build())

    def resume_game(self):
        """
        Method that exits from current scene
        """
        self.mixer.play_button_click()
        self.director.exit_scene()

    def show_controls_screen(self):
        """
        Method that changes current screen to the controls screen
        """
        self.current_screen = 1

    def show_options_screen(self):
        """
        Method that changes current screen to the options screen
        """
        self.current_screen = 2

    def music_louder(self):
        """
        Method that increases the volume of the music
        """
        self.mixer.music_louder()

    def music_lower(self):
        """
        Method that reduces the volume of the music
        """
        self.mixer.music_lower()

    def sound_louder(self):
        """
        Method that increases the volume of the sounds
        """
        self.mixer.sound_louder()

    def sound_lower(self):
        """
        Method that reduces the volume of the sounds
        """
        self.mixer.sound_lower()