from src.sprites.groups.scroll_adjusted import ScrollAdjustedLayeredGroup
from src.sprites.passive.platform import Platform
from src.sprites.spritesheet import SpriteSheet
from src.utils import assets


class LayersBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        path = assets.path_to('levels', level_dto.level_name, level_dto.tiles_image)
        self.sheet = SpriteSheet(container, path)
        self.level_dto = level_dto

    def build(self, camera_scroll):
        return Layers(camera_scroll, self)


class Layers(ScrollAdjustedLayeredGroup):
    def __init__(self, camera_scroll, builder: LayersBuilder):
        super().__init__(camera_scroll)
        self.layers_id = builder.level_dto.layers_id
        for layer in builder.level_dto.layers:
            for platform in layer.platforms:
                self.add(builder.container.object_from_name(layer.path, builder.sheet, builder.level_dto.tile_size,
                                                            platform), layer=layer.id)

    def get_ground(self):
        return self.get_sprites_from_layer(self.layers_id["ground"])

    def get_dangerous(self):
        return self.get_sprites_from_layer(self.layers_id["danger"])

    def get_falling(self):
        return self.get_sprites_from_layer(self.layers_id["falling"])
