#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pygame as pg

import assets
import os
import sys

from camera import Camera
from enemy import Enemy
from level import Level
from player import Player
from projectile import Projectile

white = (255, 255, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_SIZE = pg.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 20


def update_cursor(mouse_pos, screen, cursor):
    cursor_rect = cursor.get_rect()
    mx, my = mouse_pos
    cursor_rect.center = (mx, my)
    screen.blit(cursor, cursor_rect)


def main():
    pg.init()
    pg.mouse.set_visible(False)
    cursor = pg.transform.scale(assets.load_image("cursor", "single-cursor.png"), (32, 32))
    bg = pg.image.load(assets.path_to("background.png"))
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("tutorial pygame parte 2")

    level = Level("tiles_32x32")
    platforms = pg.sprite.Group()
    player = Player(32, 64, 16, 8, platforms)
    camera = Camera(player, pg.Rect(0, 0, level.map_width * 32, level.map_height * 32), SCREEN_SIZE)
    level.load_platforms(platforms, camera)

    # Main loop
    clock = pg.time.Clock()
    bullets = pg.sprite.Group()
    enemies = pg.sprite.Group()
    enemy = Enemy(32, 64, 16, 8, platforms)
    enemies.add(enemy)

    while True:
        screen.blit(bg, (0, 0))

        # If window closed event is detected, end program
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                # conditions for double jumping
                if event.key in [pg.K_UP, pg.K_w, pg.K_SPACE]:
                    player.jump()
            if event.type == pg.MOUSEBUTTONDOWN:
                # mouse shutting
                if len(bullets) < 5:
                    # look to shoot direction
                    bullets.add(player.shoot(camera))

        to_remove = list(filter(lambda bll: SCREEN_HEIGHT < bll.x or bll.x < 0 or SCREEN_WIDTH < bll.y or bll.y < 0,
                                bullets.sprites()))
        bullets.remove(to_remove)

        bullets.update()
        camera.update()
        enemies.update()

        pressed = pg.key.get_pressed()

        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            player.move_left()
        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            player.move_right()

        screen_rect = screen.get_rect()
        screen_rect[2] += level.map_width * level.tile_size - SCREEN_WIDTH
        player.rect.clamp_ip(screen_rect)

        bullets.draw(screen)
        camera.draw(screen)
        enemies.draw(screen)
        update_cursor(pg.mouse.get_pos(), screen, cursor)
        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
