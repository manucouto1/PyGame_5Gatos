import pygame as pg
from src.menu.element import ElementGUI
import src.utils.assets as assets


class Button(ElementGUI):
    """
    Class to create buttons on screen

    :param screen: reference to the screen that the element belongs to
    :param image: image of the button (png file)
    :param position: position of the element (x, y)
    :param width: width of the button
    :param height: height of the button
    """

    def __init__(self, screen, image, position, width, height):
        self.image = pg.image.load(assets.path_to(image))
        self.image = pg.transform.scale(self.image, (width, height))
        ElementGUI.__init__(self, screen, self.image.get_rect())
        self.set_position(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


"""
Child classes that implement action() method
"""


class ButtonPlay(Button):
    """
    Button that calls for execute_game menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_green.png', position, 200, 50)

    def action(self):
        self.screen.menu.execute_game()


class ButtonPlayAgain(Button):
    """
    Button that calls for execute_game menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_green.png', position, 200, 50)

    def action(self):
        print("button")
        self.screen.menu.reset_scene()


class ButtonControls(Button):
    """
    Button that calls for the show_controls_screen menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_yellow.png', position, 200, 50)

    def action(self):
        self.screen.menu.show_controls_screen()


class ButtonOptions(Button):
    """
    Button that calls for the show_options_screen menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_pink.png', position, 200, 50)

    def action(self):
        self.screen.menu.show_options_screen()


class ButtonLevels(Button):
    """
    Button that calls for the show_levels_screen menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_green.png', position, 200, 50)

    def action(self):
        self.screen.menu.show_levels_screen()


class ButtonLevel1(Button):
    """
    Button that calls for execute_level menu method for level 1
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_lilac.png', position, 200, 50)

    def action(self):
        self.screen.menu.execute_level(0)


class ButtonLevel2(Button):
    """
    Button that calls for execute_level menu method for level 2
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_pink.png', position, 200, 50)

    def action(self):
        self.screen.menu.execute_level(1)


class ButtonLevel3(Button):
    """
    Button that calls for execute_level menu method for level 3
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_green.png', position, 200, 50)

    def action(self):
        self.screen.menu.execute_level(2)


class ButtonLevel4(Button):
    """
    Button that calls for execute_level menu method for level 4
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_yellow.png', position, 200, 50)

    def action(self):
        self.screen.menu.execute_level(3)


class ButtonExit(Button):
    """
    Button that calls for exit_program menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_lilac.png', position, 200, 50)

    def action(self):
        self.screen.menu.exit_program()


class ButtonBack(Button):
    """
    Button that calls for the show_initial_screen menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_orange.png', position, 200, 50)

    def action(self):
        self.screen.menu.show_initial_screen()


class ButtonMusicLouder(Button):
    """
    Button that calls for the music louder menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/volume-up.png', position, 50, 50)

    def action(self):
        self.screen.menu.music_louder()


class ButtonMusicLower(Button):
    """
    Button that calls for the music_lower menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/volume-down.png', position, 50, 50)

    def action(self):
        self.screen.menu.music_lower()


class ButtonSoundLouder(Button):
    """
    Button that calls for the sound_louder menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/volume-up.png', position, 50, 50)

    def action(self):
        self.screen.menu.sound_louder()


class ButtonSoundLower(Button):
    """
    Button that calls for the sound_lower menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/volume-down.png', position, 50, 50)

    def action(self):
        self.screen.menu.sound_lower()


class ButtonResume(Button):
    """
    Button that calls for the resume_game menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_green.png', position, 200, 50)

    def action(self):
        self.screen.menu.resume_game()


class ButtonQuit(Button):
    """
    Button that calls for the quit_game menu method
    """

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/button_lilac.png', position, 200, 50)

    def action(self):
        self.screen.menu.quit_game()


class ButtonPause(Button):

    def __init__(self, screen, position):
        Button.__init__(self, screen, 'menu/pause.png', position, 50, 50)
