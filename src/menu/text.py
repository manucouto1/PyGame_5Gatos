import pygame as pg
from src.menu.element import ElementGUI

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class TextGUI(ElementGUI):

    def __init__(self, screen, font, color, text, position):
        self.image = font.render(text, True, color)
        ElementGUI.__init__(self, screen, self.image.get_rect())
        self.set_position(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class TextTitle(TextGUI):

    def __init__(self, screen):
        # font = pg.font.Font('Mikodacs.otf', 78)
        font = pg.font.Font('../assets/fonts/yukari.ttf', 78)
        TextGUI.__init__(self, screen, font, (255, 255, 255), '5Gatos', (SCREEN_WIDTH / 2 - 120, 150))


class TextPlay(TextGUI):

    def __init__(self, screen):
        font = pg.font.SysFont('purisa', 26)
        TextGUI.__init__(self, screen, font, (0, 0, 0), 'Play', (380, 270))

    def action(self):
        self.screen.menu.execute_game()


class TextControls(TextGUI):

    def __init__(self, screen):
        font = pg.font.SysFont('purisa', 26)
        TextGUI.__init__(self, screen, font, (0, 0, 0), 'How to play', (320, 370))

    def action(self):
        self.screen.menu.show_controls_screen()


class TextOptions(TextGUI):

    def __init__(self, screen):
        font = pg.font.SysFont('purisa', 26)
        TextGUI.__init__(self, screen, font, (0, 0, 0), 'Options', (355, 470))

    def action(self):
        self.screen.menu.show_options_screen()


class TextExit(TextGUI):

    def __init__(self, screen):
        font = pg.font.SysFont('purisa', 26)
        TextGUI.__init__(self, screen, font, (0, 0, 0), 'Exit', (380, 570))

    def action(self):
        self.screen.menu.exit_program()


class TextBack(TextGUI):

    def __init__(self, screen):
        font = pg.font.SysFont('purisa', 26)
        TextGUI.__init__(self, screen, font, (0, 0, 0), 'Back', (570, 670))

    def action(self):
        self.screen.menu.show_initial_screen()
