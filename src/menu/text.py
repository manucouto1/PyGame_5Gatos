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


class TextPlay(TextGUI):

    def __init__(self, screen):
        font = pg.font.SysFont('arial', 26)
        TextGUI.__init__(self, screen, font, (0, 0, 0), 'Play', (SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/2))

    def action(self):
        self.screen.menu.execute_game()


class TextExit(TextGUI):

    def __init__(self, screen):
        font = pg.font.SysFont('arial', 26)
        TextGUI.__init__(self, screen, font, (0, 0, 0), 'Exit', (SCREEN_WIDTH/2 + 200, SCREEN_HEIGHT/2))

    def action(self):
        self.screen.menu.exit_program()
