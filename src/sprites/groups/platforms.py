import numpy as np


class Platforms:
    """
    Class to manage the platform set

    :param game: Game DTO
    :param platforms: The map platforms
    """
    def __init__(self, game, platforms):
        self.center_x = game.screen_width/2
        self.center_y = game.screen_height/2
        self.max_distance = np.sqrt(self.center_x ** 2 + self.center_y ** 2)
        self.sprites = dict()
        self.sprites['actives'] = platforms
        self.sprites['freezes'] = []

    def get_actives(self):
        """
        Get the platforms that need to be updated

        :rtype: list[Platform]
        """
        return self.sprites['actives']

    def get_freezes(self):
        """
        Get the platforms that are too far to be updated

        :rtype: list[Platform]
        """
        return self.sprites['freezes']

    def _calc_distance(self, sprite, target):
        a = (sprite.rect.x - abs(target[0] - self.center_x)) ** 2
        b = (sprite.rect.y - abs(target[1] - self.center_y)) ** 2

        return np.sqrt(a + b)

    def update(self, target):
        # Decide which platforms to keep active
        actives = self.sprites['actives']
        freezes = self.sprites['freezes']

        for sprite in actives:
            distance = self._calc_distance(sprite, target.camera_rect)
            if distance >= self.max_distance:
                self.sprites['actives'].remove(sprite)
                self.sprites['freezes'].append(sprite)

        for sprite in freezes:
            distance = self._calc_distance(sprite, target.camera_rect)
            if distance < self.max_distance:
                self.sprites['actives'].append(sprite)
                self.sprites['freezes'].remove(sprite)
