import pygame as pg

from sprites.spritesheet import SpriteStripAnim
from src.sprites.active.active_entity import ActiveEntity
import src.utils.assets as assets
GRAVITY = pg.Vector2((0, 2.8))


class Enemy(ActiveEntity):

    def __init__(self, initial_pos, *groups):
        sheet_path = assets.path_to("characters", "enemy", "enemy_full.png")
        sheet = SpriteStripAnim(sheet_path, (0, 0, 32, 32), 8, rows=4)

        super().__init__(initial_pos, sheet, *groups)

        self.path = [20 * 32, 20 * 32 + 100]
        self.walk_count = 0
        self.life = 2
        self.dead_id = 0

        self.sheet[0].set_frames_skip(2)
        self.sheet[1].set_frames_skip(2)
        self.sheet[2].set_frames_skip(2)
        self.sheet[3].set_frames_skip(2)

    def move(self):
        if self.vel.x > 0:
            if self.rect[0] < self.path[1] + self.vel.x:
                self.move_right()
            else:
                self.sheet.reset()
                self.move_left()
        else:
            if self.rect[0] > self.path[0] - self.vel.x:
                self.move_left()
            else:
                self.sheet.reset()
                self.move_right()

    def dead_loop(self):
        self.image = self.sheet[3].next()

    def update(self, platforms):
        if self.life > 0:
            self.move()
            self.walk_loop()
            self.apply(platforms)
        else:
            self.vel.x = 0
            self.dead_loop()
            self.apply(platforms)

    def is_hit(self):
        # TODO ver como implementar daño en enemigo
        self.life -= 1
