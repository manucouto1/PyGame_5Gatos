import pygame as pg

from pygame.sprite import collide_mask
from src.sprites.active.shooter_entity import ShooterEntity
from src.sprites.passive.hud.life import Life
import time
from src.sprites.passive.hud.punctuation import Punctuation


class HeroBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        self.entity_dto = level_dto.hero

    def build(self, player):
        return Hero(player, self)


class Hero(ShooterEntity):
    def __init__(self, player, builder: HeroBuilder):
        game = builder.container.get_object('game')
        character = game.characters[builder.entity_dto.name]
        ShooterEntity.__init__(self, builder.container, builder.entity_dto, character)

        self.last_hit = time.time()
        self.life = Life(builder.container, 3, player)
        self.points = Punctuation(builder.container, player)

    def walk_loop(self, dt):
        if self.direction == pg.K_LEFT:
            self.image = self.sheet[1].next(dt)
        elif self.direction == pg.K_RIGHT:
            self.image = self.sheet[2].next(dt)

    def is_hit_destroy(self, dangerous):
        #list_e_bullets = pg.sprite.spritecollide(self, dangerous, True, collided=collide_mask)
        its_hit = pg.sprite.spritecollideany(self, dangerous, collided=collide_mask)
        if its_hit:
            new_hit = time.time()
            if self.last_hit + 1 < new_hit:
                #for its_hit in list_e_bullets:
                its_hit.kill()
                self.damage_effect(its_hit)
                self.jump()
                self.last_hit = new_hit
                self.life.decrease()
                self.mixer.play_hero_hit()

    def is_hit(self, dangerous):
        its_hit = pg.sprite.spritecollideany(self, dangerous, collided=collide_mask)
        if its_hit:
            new_hit = time.time()
            self.damage_effect(its_hit)
            if self.last_hit + 2 < new_hit:
                self.last_hit = new_hit
                self.life.decrease()
                self.mixer.play_hero_hit()

    def add_life(self):
        self.last_hit = time.time()
        self.life.increase()
        self.mixer.play_one_up()

    def add_point(self):
        self.points.increase()
        self.mixer.play_point()

    def update(self, platforms, _, dt, platforms2=None):
        if self.movement:
            self.walk_loop(dt)
        else:
            self.idle_loop(dt)

        self.apply(platforms, dt)
        if platforms2 is not None:
            self.collide_ground_falling(0, self.vel.y, platforms2, collide_mask)

        if not self.getting_damage:
            self.reset_movement()
        else:
            new_time = time.time()
            if self.damage_time + 0.5 < new_time:
                self.getting_damage = False
                self.reset_movement()

        self.life.update()
        self.points.update(dt)
