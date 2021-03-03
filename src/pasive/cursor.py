import pygame as pg
import assets


class Cursor(pg.sprite.Sprite):

    def __init__(self, mouse_pos):
        super().__init__()
        self.mouse_pos = mouse_pos
        self.image = pg.transform.scale(assets.load_image("cursor", "single-cursor.png"), (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = self.mouse_pos

    def update_pos(self, mouse_pos):
        self.mouse_pos = mouse_pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.center = self.mouse_pos
