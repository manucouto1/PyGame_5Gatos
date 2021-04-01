import pygame


class SpriteSheet(object):
    """
    Utility class to manipulate sprite sheets
    :param sheet: pygame.Surface
    """
    def __init__(self, sheet):
        self.sheet = sheet

    def image_at(self, rectangle, color_key=None, scale=None):
        """
        Trim the image at the specific rect from the sprite sheet
    
        :param rectangle: x_l, y_t, w, h
        :param color_key: Background RGB key
        :param scale: Transform image scale (w, h)
        :retype: pygame.Surface
        """
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

    def images_at(self, rects, color_key=None, scale=None):
        """
        Trim the images at the specific rects
    
        :param rects: List of x_l, y_t, w, h
        :param color_key: Background RGB key
        :param scale: Transform image scale (w, h)
        :retype: list[pygame.Surface]
        """
        return [self.image_at(rect, color_key, scale) for rect in rects]

    def load_strip(self, rect, image_count, color_key=None, scale=None):
        """
        Load images in line from initial rect
    
        :param rect: x_l, y_t, w, h
        :param image_count: Number of inline images
        :param color_key: Background RGB key
        :param scale: Transform image scale (w, h)
        :rtype: list[pygame.Surface]
        """
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups, color_key, scale)


class SpriteStripAnim(SpriteSheet):
    """Utility class to manage sprite sheet frame strips"""
    def __init__(self, sheet, rect, frames, color_key=None, rows=1, scale=None):
        super().__init__(sheet)
        self.frames = frames
        self.images = [
            SpriteSheet.load_strip(self, pygame.Rect(rect[0], rect[1] + rect[3] * y, rect[2], rect[3]), frames,
                                   color_key, scale)
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
        """
        The array access causes the current selected row to be updated
        """
        self.row = item

        return self

    def set_frames_skip(self, i):
        """
        Sets the frame skip for the current row
        """
        self.frames_skip[self.row] = i

    def reset(self):
        """
        Reset to initial frame
        """
        self._roll_once = False
        self.idx = 0
        self._dt_count = 0

    def roll_once(self, dt):
        """
        Behaves like next, but after the strip of images completes a lap it will return the first frame until reset

        :param dt: Clock time elapsed (ms)
        :rtype: pygame.Surface
        """
        if not self._roll_once:
            image = self.next(dt)
        else:
            image = self.images[self.row][0]

        if self.idx == self.frames - 1:
            self._roll_once = True
            image = self.next(dt)

        return image

    def next(self, dt, interval=450):
        """
        Returns the images of the current row strip iteratively in round way, based on elapsed clock time.

        :param dt: Clock time elapsed (ms)
        :param interval: Time to change to the next image
        :rtype: list[pygame.Surface]
        """
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
        """
        Gets mask for current index and row
        """
        return self.masks[self.row][self.idx]
