import pygame as pg
import src.utils.assets as assets
from src.sprites.spritesheet import SpriteSheet


class Cursor(pg.sprite.Sprite):

    def __init__(self, container, mouse_pos):
        super().__init__()
        game = container.get_object('game')
        self.sheet = SpriteSheet(container, assets.path_to("cursor", game.cursor))
        self.image = pg.transform.scale(self.sheet.image_at((64, 0, 16, 16)), (16, 16))
        self.rect = self.image.get_rect()
        self.rect.center = mouse_pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, mouse_pos):
        self.rect.center = mouse_pos
