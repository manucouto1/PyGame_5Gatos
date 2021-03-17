import pygame as pg
from src.menu.element import ElementGUI
import src.utils.assets as assets

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class Button(ElementGUI):

    def __init__(self, screen, image, position):
        self.image = pg.image.load(assets.path_to(image))
        self.image = pg.transform.scale(self.image, (99, 39))
        ElementGUI.__init__(self, screen, self.image.get_rect())
        self.set_position(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class ButtonPlay(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'green_button.png', (SCREEN_WIDTH/2 - 220, SCREEN_HEIGHT/2 + 5))

    def action(self):
        self.screen.menu.execute_game()


class ButtonExit(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'red_button.png', (SCREEN_WIDTH/2 + 180, SCREEN_HEIGHT/2 + 5))

    def action(self):
        self.screen.menu.exit_program()
