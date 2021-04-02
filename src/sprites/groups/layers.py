from src.sprites.groups.scroll_adjusted import ScrollAdjustedLayeredGroup
from src.sprites.spritesheet import SpriteSheet
from src.utils import assets


class LayersBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        path = assets.path_to('levels', level_dto.level_name, level_dto.tiles_image)
        sheet = container.image_from_path(path)
        self.sheet = SpriteSheet(sheet)
        self.level_dto = level_dto

    def build(self, camera_scroll):
        return Layers(camera_scroll, self)


class Layers(ScrollAdjustedLayeredGroup):
    """
    Class to manage the layered groups of platforms

    :param camera_scroll: Current scroll pointer [x, y]
    """
    def __init__(self, camera_scroll, builder: LayersBuilder):
        super().__init__(camera_scroll)
        self.layers_id = builder.level_dto.layers_id
        for layer in builder.level_dto.layers:
            for platform in layer.platforms:
                self.add(builder.container.object_from_name(
                    layer.path, builder.sheet, builder.level_dto.tile_size, platform), layer=layer.id)

    def get_ground(self):
        """
        Get normal platforms

        :rtype: list[Platform]
        """
        return self.get_sprites_from_layer(self.layers_id["ground"])

    def get_dangerous(self):
        """
        Get dangerous platforms

        :rtype: list[Platform]
        """
        return self.get_sprites_from_layer(self.layers_id["danger"])

    def get_falling(self):
        """
        Get falling platforms

        :rtype: list[Platform]
        """
        return self.get_sprites_from_layer(self.layers_id["falling"])
