from src.game.dto.entity_dto import EntityDTO
from src.game.dto.event_dto import EventDTO
from src.game.dto.layer_dto import LayerDTO
import src.utils.assets as assets
import json


class LevelDTO:
    def __init__(self, level_name):
        try:
            self.level_name = level_name
            with open(assets.path_to('levels', level_name, level_name + '_config.json')) as f:
                level_config = json.load(f)
                if level_config is not None:
                    self.path = level_config["path"]
                    self.bg = level_config["background"]
                    tiles = level_config["tiles"]
                    entities = level_config["entities"]
                    events = level_config['events']

                    self.tiles_image = tiles['image']

            with open(assets.path_to('levels', level_name, tiles['config'])) as f:
                tiles_config = json.load(f)
                if tiles_config is not None:
                    self.tile_size = tiles_config["tile_size"]
                    self.map_width = tiles_config["map_width"]
                    self.map_height = tiles_config["map_height"]
                    layers = tiles_config["layers"]

                    self.layers = []
                    for layer in layers:
                        self.layers.append(LayerDTO(layer))

            with open(assets.path_to('levels', level_name, entities)) as f:
                entities_config = json.load(f)
                self.hero = EntityDTO(entities_config['hero'])

                self.enemies = []
                for entity in entities_config["enemies"]:
                    self.enemies.append(EntityDTO(entity))

            with open(assets.path_to('levels', level_name, events)) as f:
                entities_config = json.load(f)
                self.events = []
                for event in entities_config['events']:
                    self.events.append(EventDTO(event))

        except IOError as e:
            print("Level data loading error > ", e)
