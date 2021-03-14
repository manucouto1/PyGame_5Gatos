#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from src.game.director import Director
from src.levels.level_2d_scroller import Scroller2D


def main():
    # Main loop
    game = Director()
    game.stack_scene(Scroller2D("level1"))
    game.run()


if __name__ == "__main__":
    main()
