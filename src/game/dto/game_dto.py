import json

from src.game.dto.character_dto import CharacterDTO
from src.game.dto.level_dto import LevelDTO
import src.utils.assets as assets


class GameDTO:
    def __init__(self, game):

        try:
            with open(assets.path_to(game)) as f:
                game_config = json.load(f)
                self.fps = game_config["fps"]
                self.cursor = game_config["cursor"]
                with open(assets.path_to(game_config["characters"])) as f2:
                    characters = json.load(f2)
                    self.characters = dict(map(lambda k,v: (k, CharacterDTO(v)), characters.keys(), characters.values()))
                self.levels = list(map(lambda x: LevelDTO(x), game_config["levels"]))
        except IOError:
            print("Game data loading error")
