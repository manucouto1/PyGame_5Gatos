import pygame as pg

from src.sprites.pasive.life import Life
from src.sprites.spritesheet import SpriteStripAnim
from src.sprites.pasive.projectile import Projectile
from src.sprites.active.active_entity import ActiveEntity
import src.utils.assets as assets
import time


class HeroBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        self.entity_dto = level_dto.hero

    def build(self, player):
        return Hero(player, self)


class Hero(ActiveEntity):
    def __init__(self, player, builder: HeroBuilder):
        name = builder.entity_dto.name
        sheet = builder.entity_dto.sheet
        sheet_path = assets.path_to("characters", name, f"{sheet}.png")
        sheet = SpriteStripAnim(builder.container, sheet_path, (0, 0, 32, 32), 8, rows=6)

        super().__init__(builder.entity_dto.pos, sheet)
        self.last_hit = time.time()
        self.life = Life(builder.container, 3, player)

    def shoot(self):
        # Look towards shoot direction
        (m_x, m_y) = pg.mouse.get_pos()
        m_pos = (m_x - self.scroll.x, m_y - self.scroll.y)

        if m_x > self.rect.x + self.scroll.x:
            self.direction = pg.K_RIGHT
        elif m_x < self.rect.x + self.scroll.x:
            self.direction = pg.K_LEFT

        bullet = Projectile(round(self.rect.x + self.rect.width // 2),
                            round(self.rect.y + self.rect.height // 2), 6)

        bullet.trajectory(m_pos)

        return bullet

    def walk_loop(self, dt):
        if self.direction == pg.K_LEFT:
            self.image = self.sheet[1].next(dt)
        elif self.direction == pg.K_RIGHT:
            self.image = self.sheet[2].next(dt)

    def is_hit(self, dangerous):
        collide_l = pg.sprite.spritecollideany(self, dangerous)
        if collide_l:
            new_hit = time.time()
            if self.last_hit + 2 < new_hit:
                self.last_hit = new_hit
                self.life.decrease()

    def update(self, platforms, _, dt):
        if self.movement:
            self.walk_loop(dt)
        else:
            self.idle_loop(dt)
        self.life.update()
        self.apply(platforms, dt)
        self.reset_movement()
