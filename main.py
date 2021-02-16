#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pygame as pg
#from pygame.locals import *

import sys
import os

from level import Level
from player import Player
from camera import Camera

white = (255, 255, 255) 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_SIZE = pg.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 20

def main():

    pg.init()

    bg = pg.image.load(("assets"+os.sep+"background.png"))
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("tutorial pygame parte 2")
   
    level = Level("tiles_32x32")
    platforms = pg.sprite.Group()
    player = Player(64, 64, 8, platforms)
    camera = Camera(player, pg.Rect(0,0,level.map_width*32, level.map_height*32), SCREEN_SIZE)
    level.load_platforms(platforms, camera)

    #Bucle de "Juego"

    clock=pg.time.Clock()

    while True:
        screen.blit(bg, (0,0))

        for event in pg.event.get():    #Cuando ocurre un evento...
            if event.type == pg.QUIT:   #Si el evento es cerrar la ventana
                pg.quit()               #Se cierra pygame
                sys.exit()     
                

        # all_sprites_list.update()
        camera.update()

        pressed = pg.key.get_pressed()  
        
        if pressed[pg.K_UP]: 
            player.jump() 
            print("Jumped")
        if pressed[pg.K_LEFT]: 
            player.moveLeft()
        if pressed[pg.K_RIGHT]: 
            player.moveRight()

        camera.draw(screen)
        pg.display.update()
        clock.tick(FPS)

        #      #Genera la ventana
if __name__ == "__main__":
    main()

