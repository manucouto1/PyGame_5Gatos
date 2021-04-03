#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from src.game.director import Director
from src.menu.menu import InitialMenu


def main():
    game = Director()
    game.stack_scene(InitialMenu(game).build())
    game.run()


if __name__ == "__main__":
    main()
