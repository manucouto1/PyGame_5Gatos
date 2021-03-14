from src.sprites.pasive.platforms import Platform
from src.sprites.groups.custom_layered_group import CustomLayeredGroup


class Layers(CustomLayeredGroup):

    def __init__(self, layers, sheet, tile_size, camera_rect):
        super().__init__(camera_rect)

        for lyr in layers:
            layer_id = int(lyr["name"])
            for position in lyr["positions"]:
                self.add(Platform(sheet, tile_size, position["x"], position["y"], position["id"]), layer=layer_id)

    def get_ground(self):
        return self.get_sprites_from_layer(layer=1)

    def get_dangerous(self):
        return self.get_sprites_from_layer(layer=2)
