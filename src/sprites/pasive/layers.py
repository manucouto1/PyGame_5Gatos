from sprites.groups.scroll_adjusted import ScrollAdjustedLayeredGroup
from src.sprites.pasive.platforms import Platform


class Layers(ScrollAdjustedLayeredGroup):
    def __init__(self, layers, sheet, tile_size, camera_scroll):
        super().__init__(camera_scroll)

        for lyr in layers:
            layer_id = int(lyr["name"])
            for position in lyr["positions"]:
                self.add(Platform(sheet, tile_size, position["x"], position["y"], position["id"]), layer=layer_id)

    def get_ground(self):
        return self.get_sprites_from_layer(layer=1)

    def get_dangerous(self):
        return self.get_sprites_from_layer(layer=2)
