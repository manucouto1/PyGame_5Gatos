from pygame.sprite import Group

from src.sprites.passive.hud.point_text import PointText
from src.sprites.passive.hud.points_animation import PointAnim

POINT_Y = 10


class KittenScore(Group):
    """
    Class to manage kitten score

    :param container: Application container
    :param player: Player instance
    """
    def __init__(self, container, player):
        self.player = player
        self.icon = PointAnim(container, POINT_Y)
        self.scorer = PointText(container, player, POINT_Y)
        super().__init__(self.scorer, self.icon)

    def increase(self):
        """
        Increments the score one point
        """
        self.icon.run_animation()
        self.scorer.increase()
        self.player.punctuation += 1
