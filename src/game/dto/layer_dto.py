from src.game.dto.platform_dto import PlatformDTO


class LayerDTO:
    def __init__(self, layer):
        self.id = int(layer["name"])
        self.path = layer['path']
        self.platforms = []
        for platform in layer["positions"]:
            self.platforms.append(PlatformDTO(platform))
