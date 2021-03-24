import pygame as pg
from src.game.player import Player
from src.game.container import Container

FPS = 30


class Director:
    _instance = None

    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        pg.display.set_caption('5Gatos')

        self.scenes = []
        self.exit = False
        self.clock = pg.time.Clock()
        self.player = Player()
        self.container = Container()

    def __new__(cls):
        if Director._instance is None:
            Director._instance = object.__new__(cls)

        return Director._instance

    def exit_scene(self):
        self.exit = True
        if len(self.scenes) > 0:
            self.scenes.pop()

    def exit_program(self):
        self.scenes = []
        self.exit = True

    def change_scene(self, scene):
        self.exit_scene()
        self.scenes.append(scene)

    def stack_scene(self, scene):
        self.exit = True
        self.scenes.append(scene)

    def run(self):
        while len(self.scenes) > 0:
            scene = self.scenes[len(self.scenes) - 1]
            self.loop(scene)

    def loop(self, scene):
        self.exit = False
        pg.event.clear()
        scene = scene.build(self.player)

        dt = self.clock.tick(FPS)
        while not self.exit:
            print(dt)
            scene.events(pg.event.get())
            scene.update(dt)
            scene.draw()

            pg.display.update()
            dt = self.clock.tick(FPS)
