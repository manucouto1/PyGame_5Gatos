import pygame as pg
import src.utils.assets as assets
from src.menu.button import ButtonPlay
from src.menu.button import ButtonExit
from src.menu.text import TextPlay
from src.menu.text import TextExit

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class ScreenGUI:

    def __init__(self, menu, image):
        self.menu = menu
        self.bg = assets.load_image(image)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        # list of elementGUI
        self.elementGUI = []

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        for element in self.elementGUI:
            element.draw(self.screen)

    def events(self, event_list):
        # to know what elementGUI has been clicked, we ask all of them
        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.elementClic = None
                for element in self.elementGUI:
                    if element.position_elem(event.pos):
                        self.elementClic = element
            if event.type == pg.MOUSEBUTTONUP:
                for element in self.elementGUI:
                    if element.position_elem(event.pos):
                        if element == self.elementClic:
                            element.action()


class ScreenGUIInitial(ScreenGUI):

    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        button_play = ButtonPlay(self)
        button_exit = ButtonExit(self)
        self.elementGUI.append(button_play)
        self.elementGUI.append(button_exit)
        text_play = TextPlay(self)
        text_exit = TextExit(self)
        self.elementGUI.append(text_play)
        self.elementGUI.append(text_exit)
