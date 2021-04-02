import pygame as pg
from src.menu.element import ElementGUI
import src.utils.assets as assets

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


class Button(ElementGUI):

    def __init__(self, screen, image, position, width, height):
        self.image = pg.image.load(assets.path_to(image))
        self.image = pg.transform.scale(self.image, (width, height))
        ElementGUI.__init__(self, screen, self.image.get_rect())
        self.set_position(position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class ButtonPlay(Button):
    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/button1.png', (305, 270), 200, 50)

    def action(self):
        self.screen.menu.execute_game()


class ButtonControls(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/button5.png', (305, 370), 200, 50)

    def action(self):
        self.screen.menu.show_controls_screen()


class ButtonOptions(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/button3.png', (305, 470), 200, 50)

    def action(self):
        self.screen.menu.show_options_screen()


class ButtonLevels(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/button1.png', (305, 570), 200, 50)

    def action(self):
        self.screen.menu.show_levels_screen()


class ButtonExit(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/button2.png', (305, 670), 200, 50)

    def action(self):
        self.screen.menu.exit_program()


class ButtonBack(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/button2.png', (500, 670), 200, 50)

    def action(self):
        self.screen.menu.show_initial_screen()


class ButtonMusicLouder(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/volume-up.png', (490, 140), 50, 50)

    def action(self):
        self.screen.menu.music_louder()


class ButtonMusicLower(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/volume-down.png', (370, 140), 50, 50)

    def action(self):
        self.screen.menu.music_lower()


class ButtonSoundLouder(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/volume-up.png', (490, 240), 50, 50)

    def action(self):
        self.screen.menu.sound_louder()


class ButtonSoundLower(Button):

    def __init__(self, screen):
        Button.__init__(self, screen, 'menu/volume-down.png', (370, 240), 50, 50)

    def action(self):
        self.screen.menu.sound_lower()
