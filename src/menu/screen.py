import pygame as pg
import src.utils.assets as assets
from src.menu.button import ButtonPlay, ButtonControls, ButtonOptions, ButtonLevels, ButtonExit, ButtonBack, ButtonQuit, \
    ButtonLevel1, ButtonLevel2, ButtonLevel3, ButtonLevel4, ButtonPlayAgain
from src.menu.button import ButtonMusicLouder, ButtonMusicLower, ButtonSoundLouder, ButtonSoundLower, ButtonResume
from src.menu.text import TextPlay, TextReplay, TextControls, TextOptions, TextLevels, TextExit, TextBack, TextQuit
from src.menu.text import TextLevel1, TextLevel2, TextLevel3, TextLevel4, TextResume
from src.sprites.spritesheet import SpriteStripAnim, SpriteSheet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class ScreenGUI:
    """
    Class to create screen objects

    :param menu: scene menu
    :param image: image of the background (png file)
    """
    def __init__(self, menu, image):
        self.menu = menu
        self.element_click = None
        self.bg = assets.load_image(image)
        self.font = pg.font.Font('../assets/fonts/Purisa Bold.ttf', 26)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # list of elementGUI
        self.elementGUI = []

    def draw(self):
        """
        Call draw method of each elementGUI on the screen
        """
        self.screen.blit(self.bg, (0, 0))
        for element in self.elementGUI:
            element.draw(self.screen)

    def events(self, event_list):
        """
        To know what elementGUI has been clicked, we ask all of them
        and call action method of the clicked one
        """
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
    """
    Initial menu screen
    """
    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonPlay(self, (305, 270)))
        self.elementGUI.append(ButtonExit(self, (305, 670)))
        self.elementGUI.append(ButtonControls(self, (305, 370)))
        self.elementGUI.append(ButtonOptions(self, (305, 470)))
        self.elementGUI.append(ButtonLevels(self, (305, 570)))
        self.elementGUI.append(TextPlay(self, (380, 270)))
        self.elementGUI.append(TextExit(self, (380, 670)))
        self.elementGUI.append(TextOptions(self, (355, 470)))
        self.elementGUI.append(TextControls(self, (340, 370)))
        self.elementGUI.append(TextLevels(self, (355, 570)))

    def draw(self):
        ScreenGUI.draw(self)
        font = pg.font.Font('../assets/fonts/yukari.ttf', 78)
        title = font.render('5Gatos', True, (255, 255, 255))
        self.screen.blit(title, (280, 60))


class ScreenGUIControls(ScreenGUI):
    """
    Controls screen
    """
    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonBack(self, (500, 670)))
        self.elementGUI.append(TextBack(self, (570, 670)))

    def draw(self):
        ScreenGUI.draw(self)
        text1 = self.font.render('Move: use the WASD keys or the arrow keys', True, (0, 0, 0))
        text2 = self.font.render('Aim and Shoot: use the mouse', True, (0, 0, 0))
        text3 = self.font.render('Jump: use UP arrow, W key or SPACE BAR', True, (0, 0, 0))
        text4 = self.font.render('Double Jump: press for jump while in the air', True, (0, 0, 0))
        self.screen.blit(text1, (80, 70))
        self.screen.blit(text2, (80, 260))
        self.screen.blit(text3, (80, 460))
        self.screen.blit(text4, (80, 560))
        self.screen.blit(pg.transform.scale(assets.load_image("menu", "arrows.png"), (200, 150)), (100, 120))
        self.screen.blit(pg.transform.scale(assets.load_image("menu", "mouse.png"), (150, 150)), (100, 300))
        self.screen.blit(pg.transform.scale(assets.load_image("menu", "click.png"), (120, 120)), (250, 320))


class ScreenGUIOptions(ScreenGUI):
    """
    Options screen
    """
    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonBack(self, (500, 670)))
        self.elementGUI.append(TextBack(self, (570, 670)))
        self.elementGUI.append(ButtonMusicLower(self, (370, 140)))
        self.elementGUI.append(ButtonMusicLouder(self, (490, 140)))
        self.elementGUI.append(ButtonSoundLower(self, (370, 240)))
        self.elementGUI.append(ButtonSoundLouder(self, (490, 240)))

    def draw(self):
        ScreenGUI.draw(self)
        text1 = self.font.render('Volume settings:', True, (0, 0, 0))
        text2 = self.font.render('Sounds settings:', True, (0, 0, 0))
        text3 = self.font.render(str(int(self.menu.mixer.get_music_volume() * 10)), True, (0, 0, 0))
        text4 = self.font.render(str(int(self.menu.mixer.get_sound_volume() * 10)), True, (0, 0, 0))
        self.screen.blit(text1, (80, 100))
        self.screen.blit(text2, (80, 200))
        self.screen.blit(text3, (450, 100))
        self.screen.blit(text4, (450, 200))


class ScreenGUILevels(ScreenGUI):
    """
    Levels screen
    """
    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonLevel1(self, (305, 150)))
        self.elementGUI.append(ButtonLevel2(self, (305, 250)))
        self.elementGUI.append(ButtonLevel3(self, (305, 350)))
        self.elementGUI.append(ButtonLevel4(self, (305, 450)))
        self.elementGUI.append(ButtonBack(self, (500, 670)))
        self.elementGUI.append(TextBack(self, (570, 670)))
        self.elementGUI.append(TextLevel1(self, (350, 150)))
        self.elementGUI.append(TextLevel2(self, (350, 250)))
        self.elementGUI.append(TextLevel3(self, (350, 350)))
        self.elementGUI.append(TextLevel4(self, (350, 450)))


class ScreenGUIGameOver(ScreenGUI):
    """
    Game Over screen
    """
    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonPlayAgain(self, (305, 300)))
        self.elementGUI.append(ButtonQuit(self, (305, 400)))
        self.elementGUI.append(TextReplay(self, (330, 300)))
        self.elementGUI.append(TextQuit(self, (370, 400)))

    def draw(self):
        ScreenGUI.draw(self)
        font = pg.font.Font('../assets/fonts/yukari.ttf', 78)
        title = font.render('Game Over :(', True, (255, 255, 255))
        self.screen.blit(title, (215, 80))


class ScreenGUIPause(ScreenGUI):
    """
    Pause Menu screen
    """
    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonResume(self, (305, 270)))
        self.elementGUI.append(ButtonQuit(self, (305, 570)))
        self.elementGUI.append(ButtonControls(self, (305, 370)))
        self.elementGUI.append(ButtonOptions(self, (305, 470)))
        self.elementGUI.append(TextResume(self, (360, 270)))
        self.elementGUI.append(TextQuit(self, (370, 570)))
        self.elementGUI.append(TextOptions(self, (355, 470)))
        self.elementGUI.append(TextControls(self, (340, 370)))


class ScreenGUIVictory(ScreenGUI):
    """
    Victory Screen
    """
    def __init__(self, menu, image):
        ScreenGUI.__init__(self, menu, image)
        self.elementGUI.append(ButtonQuit(self, (500, 750)))
        self.elementGUI.append(TextQuit(self, (570, 750)))

    def draw(self):
        ScreenGUI.draw(self)
        font = pg.font.Font('../assets/fonts/yukari.ttf', 78)
        title = font.render('VICTORY!!', True, (255, 255, 255))
        font = pg.font.Font('../assets/fonts/Purisa Bold.ttf', 40)
        subtitle = font.render('Anything is paw-sible for you', True, (255, 255, 255))

        image_points = self.get_points_sprite("characters", "enemy", "enemy_full.png")
        image_hearts = self.get_heart_sprite("player", "Corazon-Sheet.png")

        image_cookie = assets.load_image("treat.png")
        image_cookie = pg.transform.scale(image_cookie, (48, 48))

        player = self.menu.director.player
        punctuation = player.punctuation
        n_hearts = player.hearts
        n_cookies = player.cookies
        text_points = font.render(str(punctuation), True, (0, 0, 0))
        text_hearts = font.render(str(n_hearts), True, (0, 0, 0))
        text_cookies = font.render(str(n_cookies), True, (0, 0, 0))

        self.screen.blit(title, (270, 80))
        self.screen.blit(subtitle, (50, 200))
        self.screen.blit(text_points, (470, 300))
        self.screen.blit(text_hearts, (470, 400))
        self.screen.blit(text_cookies, (470, 500))

        self.screen.blit(image_points, (290, 300))
        self.screen.blit(image_hearts, (300, 400))
        self.screen.blit(image_cookie, (300, 500))

    def get_points_sprite(self, *parts):

        container = self.menu.director.container

        path = assets.path_to(*parts)
        sheet = container.image_from_path(path)
        sheet = SpriteStripAnim(sheet, (0, 0, 32, 32), 8, rows=4)
        sheet[3].set_frames_skip(2)
        image = sheet[3].next(0)
        return pg.transform.scale(image, (64, 64))

    def get_heart_sprite(self, *parts):

        container = self.menu.director.container

        path = assets.path_to(*parts)
        sheet = container.image_from_path(path)
        sheet = pg.transform.scale(sheet, (50 * 21, 50))
        sheet = SpriteSheet(sheet)
        return sheet.image_at((0, 0, 50, 50))
