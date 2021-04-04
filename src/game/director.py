import pygame as pg

from src.levels.level import LevelBuilder
from src.game.dto.game_dto import GameDTO
from src.game.mixer import Mixer
from src.game.player import Player
from src.game.container import Container
from src.menu.menu import VictoryMenu

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
        self.mixer = Mixer()
        self.game = GameDTO("game_config.json")
        self.container.set_object('mixer', self.mixer)
        self.container.set_object('game', self.game)
        self.container.set_object('director', self)
        self.levels = [LevelBuilder(self.container, self.game.levels[x])
                       for x in range(len(self.game.levels))]
        self.container.set_object('levels', self.levels)
        self.scene = None

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

    def loop(self, scene_builder):
        self.exit = False
        pg.event.clear()

        if isinstance(scene_builder, LevelBuilder):
            self.scene = scene_builder
            scene_level = scene_builder.build(self.player)
            self.scenes.pop()
            self.scenes.append(scene_level)
        elif isinstance(scene_builder, VictoryMenu):
            scene_level = scene_builder.build()
        else:
            scene_level = scene_builder

        while not self.exit:
            dt = self.clock.tick(self.game.fps)
            scene_level.events(pg.event.get())
            scene_level.update(dt)
            self.mixer.check_busy()
            scene_level.draw()

            pg.display.flip()
