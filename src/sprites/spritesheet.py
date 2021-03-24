import pygame


class SpriteSheet(object):
    def __init__(self, container, path):
        self.sheet = container.image_from_path(path)

    def image_at(self, rectangle, color_key=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)

        return image

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]

        return self.images_at(tups, colorkey)

    def image_mask_at(self, rectangle, color_key=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        mask = pygame.mask.from_surface(image)
        image.blit(self.sheet, (0, 0), rect)

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)

        return image, mask

    def images_masks_at(self, rects, colorkey=None):
        return [self.image_mask_at(rect, colorkey) for rect in rects]

    def load_strip2(self, rect, image_count, colorkey=None):
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]

        return self.images_masks_at(tups, colorkey)


class SpriteStripAnim(SpriteSheet):
    def __init__(self, container, filename, rect, count, colorkey=None, rows=1):
        super().__init__(container, filename)
        self.images = [
            SpriteSheet.load_strip(self, pygame.Rect(rect[0], rect[1] + rect[3] * y, rect[2], rect[3]), count, colorkey)
            for y in range(rows)
        ]
        self.masks = [
            list(pygame.mask.from_surface(image) for image in row_image)
            for row_image in self.images
        ]
        self.row = 0
        self.idx = 0
        self.frames_skip = [1] * rows
        self.frame = 1
        self.dt_count = 0

    def __getitem__(self, item):
        self.row = item

        return self

    def set_frames_skip(self, i):
        self.frames_skip[self.row] = i

    def reset(self):
        self.idx = 0

    def next(self, dt):
        if self.dt_count < 450 / 8:
            image = self.images[self.row][self.idx]
        else:
            self.dt_count = 0
            image = self.images[self.row][self.idx]

            self.frame -= 1
            if self.frame == 0:
                self.idx += 1
                self.frame = self.frames_skip[self.row]

        self.dt_count += dt

        if self.idx >= len(self.images[0]):
            self.idx = 0

        return image

    def get_mask(self):
        return self.masks[self.row][self.idx]

    def __add__(self, spritesheet):
        self.images[self.row].extend(spritesheet.images)
        self.masks[self.row].extend(spritesheet.masks)
        return self
