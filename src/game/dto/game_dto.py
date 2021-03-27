import json

from src.game.dto.character_dto import CharacterDTO
from src.game.dto.level_dto import LevelDTO
import src.utils.assets as assets
from src.game.dto.sound_dto import SoundDTO


class GameDTO:
    def __init__(self, game):

        try:
            with open(assets.path_to(game)) as f:
                game_config = json.load(f)

                self.fps = game_config["fps"]
                self.cursor = game_config["cursor"]
                self.levels = list(map(lambda x: LevelDTO(x), game_config["levels"]))

                with open(assets.path_to(game_config["characters"])) as f2:
                    characters = json.load(f2)
                    self.characters = dict(
                        map(lambda k,v: (k, CharacterDTO(v)), characters.keys(), characters.values()))

                with open(assets.path_to(game_config["sounds"])) as f3:
                    profiles = json.load(f3)
                    sounds = profiles["sounds"]
                    self.sounds = dict(
                        map(lambda k, v: (k, SoundDTO(v)), sounds.keys(), sounds.values()))
                    self.music = profiles["music"]

        except IOError as ex:
            print("Game data loading error", ex)
