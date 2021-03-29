from pygame.sprite import Group

from src.sprites.passive.hud.point_text import PointText
from src.sprites.passive.hud.points_animation import PointAnim


class Punctuation(Group):
    def __init__(self, container, player):
        self.player = player
        self.icon = PointAnim(container)
        self.scorer = PointText(container, player)
        super().__init__(self.scorer, self.icon)

    def increase(self):
        self.icon.run_animation()
        self.scorer.increase()

        self.player.punctuation += 1
