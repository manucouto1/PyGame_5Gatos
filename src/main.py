#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pygame as pg

from levels.testLevel import TestLevel
from src.game.game_control import Director

FPS = 20


def main():

    game = Director()
    game.stack_scene(TestLevel())
    game.run()


if __name__ == "__main__":
    main()
