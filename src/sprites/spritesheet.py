import pygame

from utils import assets


class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = assets.load_image(filename)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, color_key=None):
        rect = pygame.Rect(rectangle)

        image = pygame.Surface(rect.size, pygame.SRCALPHA)

        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)

        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]

        return self.images_at(tups, colorkey)


class SpriteStripAnim(Spritesheet):
    def __init__(self, filename, rect, count, colorkey=None, rows=1):
        super().__init__(filename)
        self.images = [
            Spritesheet.load_strip(self, pygame.Rect(rect[0], rect[1] + rect[3] * y, rect[2], rect[3]), count, colorkey)
            for y in range(rows)
        ]

        self.idx = [0] * rows
        self.frame = [count] * rows
        self.row = 0

    def __getitem__(self, item):
        self.row = item

        return self

    def next(self):
        if self.idx[self.row] >= len(self.images[0]):
            self.idx[self.row] = 0
        image = self.images[self.row][self.idx[self.row]]
        self.idx[self.row] += 1

        return image

    def __add__(self, spritesheet):
        self.images[self.row].extend(spritesheet.images)

        return self
