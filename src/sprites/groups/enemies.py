import numpy as np

from src.sprites.groups.scroll_adjusted import ScrollAdjustedLayeredGroup
import pygame as pg


class EnemiesBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        self.level_dto = level_dto

    def build(self, camera_scroll):
        return Enemies(camera_scroll, self)


class Enemies(ScrollAdjustedLayeredGroup):
    def __init__(self, camera_scroll, builder: EnemiesBuilder):
        super().__init__(camera_scroll)
        game = builder.container.get_object('game')
        for entity in builder.level_dto.enemies:
            character = game.characters[entity.name]
            self.add(builder.container.object_from_name(character.path, builder.container, entity, character))

    @staticmethod
    def calc_distance(sprite, target):
        a = (sprite.rect.x - abs(target[0])) ** 2
        b = (sprite.rect.y - abs(target[1])) ** 2
        return np.sqrt(a + b)

    def are_hit(self, dangerous):
        enemies = pg.sprite.groupcollide(self, dangerous, False, False)
        for (enemy, dangerous) in enemies.items():
            enemy.is_hit(dangerous)

    def are_shot(self, bullets):
        enemies = pg.sprite.groupcollide(self, bullets, False, True)
        for (enemy, bullet) in enemies.items():
            enemy.is_shoot(bullet[0])

    def update(self, hero, *args):
        for enemy in self.sprites():
            if self.calc_distance(enemy, self.camera_rect) < 1132:
                enemy.update(hero, *args)

