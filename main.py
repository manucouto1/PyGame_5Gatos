#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pygame as pg
#from pygame.locals import *

import sys
import os

from level import Level
from player import Player

white = (255, 255, 255) 
SCREEN_WIDTH = 2400
SCREEN_HEIGHT = 1024
FPS = 15


def main():
    x = 0  
    y = 150 

    pg.init()

    bg = pg.image.load(("assets"+os.sep+"background.png"))
    screen = pg.display.set_mode((bg.get_width(), bg.get_height()))
    pg.display.set_caption("tutorial pygame parte 2")
   

    level = Level("test_tile")
    #Habría Se le pasa un layer pero debería poder pasarse todos los layers 
    player = Player(128, 128, 8, level.layers[0].plataforms_group)

    player.rect.x = x
    player.rect.y = y
    
    all_sprites_list = pg.sprite.Group()
    all_sprites_list.add(player)
    #Bucle de "Juego"

    clock=pg.time.Clock()

    while True:
        movement = False
        screen.blit(bg, (0,0))

        for event in pg.event.get():    #Cuando ocurre un evento...
            if event.type == pg.QUIT:   #Si el evento es cerrar la ventana
                pg.quit()               #Se cierra pygame
                sys.exit()     
                

        level.update()
        #Game Logic
        all_sprites_list.update()

        pressed = pg.key.get_pressed()  
        
             
        # if pressed[pg.K_DOWN]: 

        player.control(0,0)
        if pressed[pg.K_UP]: 
            player.jump() 
        if pressed[pg.K_LEFT]: 
            player.control(-8,0)
            movement = True
        if pressed[pg.K_RIGHT]: 
            player.control(8,0)
            movement = True

        player.state(movement)
        player.gravity()

        level.draw(screen)
        all_sprites_list.draw(screen)
        
        pg.display.flip()         

        clock.tick(FPS)

        #      #Genera la ventana
if __name__ == "__main__":
    main()

