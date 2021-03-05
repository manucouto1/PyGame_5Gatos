import pygame as pg
import assets


class Cursor(pg.sprite.Sprite):

    def __init__(self, mouse_pos):
        super().__init__()
        self.image = pg.transform.scale(assets.load_image("cursor", "single-cursor.png"), (16, 16))
        self.rect = self.image.get_rect()
        self.rect.center = mouse_pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, mouse_pos):
        self.rect.center = mouse_pos
