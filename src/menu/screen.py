from src.menu.button import *
from src.menu.text import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class ScreenGUI:

    def __init__(self, menu, image):
        self.menu = menu
        self.element_click = None
        self.bg = assets.load_image(image)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
                self.element_click = None
                for element in self.elementGUI:
                    if element.position_elem(event.pos):
                        self.element_click = element
            if event.type == pg.MOUSEBUTTONUP:
                for element in self.elementGUI:
                    if element.position_elem(event.pos):
                        if element == self.element_click:
                            element.action()


class ScreenGUIInitial(ScreenGUI):

    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonPlay(self))
        self.elementGUI.append(ButtonExit(self))
        self.elementGUI.append(ButtonControls(self))
        self.elementGUI.append(ButtonOptions(self))
        self.elementGUI.append(TextTitle(self))
        self.elementGUI.append(TextPlay(self))
        self.elementGUI.append(TextExit(self))
        self.elementGUI.append(TextOptions(self))
        self.elementGUI.append(TextControls(self))


class ScreenGUIControls(ScreenGUI):

    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonBack(self))
        self.elementGUI.append(TextBack(self))

    def draw(self):
        ScreenGUI.draw(self)
        font = pg.font.SysFont('purisa', 26)
        text1 = font.render('Move: use the WASD keys or the arrow keys', True, (0, 0, 0))
        text2 = font.render('Aim and Shoot: use the mouse', True, (0, 0, 0))
        text3 = font.render('Jump: use UP arrow, W key or SPACE BAR', True, (0, 0, 0))
        text4 = font.render('Double Jump: press for jump while in the air', True, (0, 0, 0))
        self.screen.blit(text1, (80, 70))
        self.screen.blit(text2, (80, 260))
        self.screen.blit(text3, (80, 460))
        self.screen.blit(text4, (80, 560))
        self.screen.blit(pg.transform.scale(assets.load_image("menu", "arrows.png"), (200, 150)), (100, 120))
        self.screen.blit(pg.transform.scale(assets.load_image("menu", "mouse.png"), (150, 150)), (100, 300))
        self.screen.blit(pg.transform.scale(assets.load_image("menu", "click.png"), (120, 120)), (250, 320))


class ScreenGUIOptions(ScreenGUI):

    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonBack(self))
        self.elementGUI.append(TextBack(self))
        self.elementGUI.append(ButtonMusicLower(self))
        self.elementGUI.append(ButtonMusicLouder(self))
        self.elementGUI.append(ButtonSoundLower(self))
        self.elementGUI.append(ButtonSoundLouder(self))

    def draw(self):
        ScreenGUI.draw(self)
        font = pg.font.SysFont('purisa', 26)
        text1 = font.render('Volume settings:', True, (0, 0, 0))
        text2 = font.render('Sounds settings:', True, (0, 0, 0))
        self.screen.blit(text1, (80, 100))
        self.screen.blit(text2, (80, 200))
