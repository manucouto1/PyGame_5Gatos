#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pygame as pg

import sys
import os
import assets

from level import Level
from player import Player
from camera import Camera

white = (255, 255, 255) 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_SIZE = pg.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 20


def main():
    pg.init()

    bg = pg.image.load(assets.path_to("background.png"))
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("tutorial pygame parte 2")
   
    level = Level("tiles_32x32")
    platforms = pg.sprite.Group()
    player = Player(32, 64, 16, 8, platforms)
    camera = Camera(player, pg.Rect(0, 0, level.map_width * 32, level.map_height * 32), SCREEN_SIZE)
    level.load_platforms(platforms, camera)

    can_double = False
    num_jumps = 0

    # Main loop
    clock = pg.time.Clock()

    while True:
        screen.blit(bg, (0, 0))

        # If window closed event is detected, end program
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()     

        # all_sprites_list.update()
        camera.update()

        pressed = pg.key.get_pressed()  

        # conditions for double jumping
        if not pressed[pg.K_UP] and num_jumps == 1:
            can_double = True
        elif num_jumps == 2:
            can_double = False
            num_jumps = 0
        
        if pressed[pg.K_UP]: 
            player.jump(can_double) 
            num_jumps += 1
        if pressed[pg.K_LEFT]: 
            player.move_left()
        if pressed[pg.K_RIGHT]: 
            player.move_right()

        screen_rect = screen.get_rect()
        screen_rect[2] += level.map_width * level.tile_size - SCREEN_WIDTH
        player.rect.clamp_ip(screen_rect)

        camera.draw(screen)
        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
