import pygame as pg
from src.menu.element import ElementGUI


class TextGUI(ElementGUI):
    """
    Class to create texts on screen

    :param screen: reference to the screen that the element belongs to
    :param color: color of the text
    :param text: content of the text
    :param position: position of the element (x, y)
    """
    def __init__(self, screen, color, text, position):
        font = pg.font.Font('../assets/fonts/Purisa Bold.ttf', 26)
        self.image = font.render(text, True, color)
        ElementGUI.__init__(self, screen, self.image.get_rect())
        self.set_position(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


"""
Child classes that implement action() method
"""


class TextPlay(TextGUI):
    """
    Text that calls for execute_game menu method
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Play', position)

    def action(self):
        self.screen.menu.execute_game()


class TextReplay(TextGUI):
    """
    Text that calls for execute_game menu method (different text param than the above one)
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Play again', position)

    def action(self):
        print("cosa de texto")
        self.screen.menu.reset_scene()


class TextControls(TextGUI):
    """
    Text that calls for the show_controls_screen menu method
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Controls', position)

    def action(self):
        self.screen.menu.show_controls_screen()


class TextOptions(TextGUI):
    """
    Text that calls for the show_options_screen menu method
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Options', position)

    def action(self):
        self.screen.menu.show_options_screen()


class TextLevels(TextGUI):
    """
    Text that calls for the show_levels_screen menu method
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Levels', position)

    def action(self):
        self.screen.menu.show_levels_screen()


class TextExit(TextGUI):
    """
    Button that calls for exit_program menu method
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Exit', position)

    def action(self):
        self.screen.menu.exit_program()


class TextBack(TextGUI):
    """
    Text that calls for the show_initial_screen menu method
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Back', position)

    def action(self):
        self.screen.menu.show_initial_screen()


class TextLevel1(TextGUI):
    """
    Text that calls for execute_level menu method for level 1
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Level 1', position)

    def action(self):
        self.screen.menu.execute_level(3)


class TextLevel2(TextGUI):
    """
    Text that calls for execute_level menu method for level 2
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Level 2', position)

    def action(self):
        self.screen.menu.execute_level(2)


class TextLevel3(TextGUI):
    """
    Text that calls for execute_level menu method for level 3
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Level 3', position)

    def action(self):
        self.screen.menu.execute_level(1)


class TextLevel4(TextGUI):
    """
    Text that calls for execute_level menu method for level 4
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Level 4', position)

    def action(self):
        self.screen.menu.execute_level(0)


class TextResume(TextGUI):
    """
    Text that calls for the resume_game menu method
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Resume', position)

    def action(self):
        self.screen.menu.resume_game()


class TextQuit(TextGUI):
    """
    Text that calls for the quit_game menu method
    """
    def __init__(self, screen, position):
        TextGUI.__init__(self, screen, (0, 0, 0), 'Quit', position)

    def action(self):
        self.screen.menu.quit_game()
