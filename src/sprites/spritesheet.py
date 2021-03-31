import pygame


class SpriteSheet(object):
    def __init__(self, sheet):
        self.sheet = sheet

    def image_at(self, rectangle, color_key=None, scale=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)

        if scale:
            image = pygame.transform.scale(image, scale)

        return image

    def images_at(self, rects, colorkey=None, scale=None):
        return [self.image_at(rect, colorkey, scale) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None, scale=None):
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups, colorkey, scale)

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
    def __init__(self, sheet, rect, frames, colorkey=None, rows=1, scale=None):
        super().__init__(sheet)
        self.frames = frames
        self.images = [
            SpriteSheet.load_strip(self, pygame.Rect(rect[0], rect[1] + rect[3] * y, rect[2], rect[3]), frames, colorkey, scale)
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
        self._dt_count = 0
        self._roll_once = True

    def __getitem__(self, item):
        self.row = item

        return self

    def set_frames_skip(self, i):
        self.frames_skip[self.row] = i

    def reset(self):
        self._roll_once = False
        self.idx = 0
        self._dt_count = 0

    def roll_once(self, dt):
        if not self._roll_once:
            image = self.next(dt)
        else:
            image = self.images[self.row][0]

        if self.idx == self.frames - 1:
            self._roll_once = True
            image = self.next(dt)

        return image

    def next(self, dt, interval=450):
        if self._dt_count < interval / 8:
            image = self.images[self.row][self.idx]
        else:
            self._dt_count = 0
            image = self.images[self.row][self.idx]

            self.frame -= 1
            if self.frame == 0:
                self.idx += 1
                self.frame = self.frames_skip[self.row]

        self._dt_count += dt

        if self.idx >= self.frames:
            self.idx = 0

        return image

    def get_mask(self):
        return self.masks[self.row][self.idx]

    def __add__(self, spritesheet):
        self.images[self.row].extend(spritesheet.images)
        self.masks[self.row].extend(spritesheet.masks)
        return self
