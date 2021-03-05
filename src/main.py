#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pygame as pg
from game_control import GameControl

FPS = 20


def main():
    # Main loop
    clock = pg.time.Clock()

    game = GameControl()
    game.init_level()

    while True:
        game.control()
        game.update()
        game.draw()
        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
