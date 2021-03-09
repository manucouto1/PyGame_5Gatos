#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pygame as pg
from src.game.game_control import GameControl


def main():
    # Main loop
    game = GameControl()
    game.init_level()

    while True:
        game.control()
        game.update()
        game.draw()
        pg.display.update()


if __name__ == "__main__":
    main()
