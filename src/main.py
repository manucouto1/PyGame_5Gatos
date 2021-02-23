#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pygame as pg

import sys
import os

from src.level import Level
from src.player import Player
from src.camera import Camera

white = (255, 255, 255) 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_SIZE = pg.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 20


def main():
    pg.init()

    bg = pg.image.load("assets" + os.sep + "background.png")
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("tutorial pygame parte 2")
   
    level = Level("tiles_32x32")
    platforms = pg.sprite.Group()
    player = Player(64, 64, 8, platforms)
    camera = Camera(player, pg.Rect(0, 0, level.map_width * 32, level.map_height * 32), SCREEN_SIZE)
    level.load_platforms(platforms, camera)

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
        
        if pressed[pg.K_UP]: 
            player.jump() 
            print("Jumped")
        if pressed[pg.K_LEFT]: 
            player.move_left()
        if pressed[pg.K_RIGHT]: 
            player.move_right()

        camera.draw(screen)
        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
