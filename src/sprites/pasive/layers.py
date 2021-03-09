import pygame as pg
from pygame import Surface
from src.sprites.pasive.platforms import Platform


class Layers(pg.sprite.LayeredUpdates):

    def __init__(self, layers, sheet, tile_size):
        super().__init__()

        for lyr in layers:
            layer_id = int(lyr["name"])
            for position in lyr["positions"]:
                self.add(Platform(sheet, tile_size, position["x"], position["y"], position["id"]), layer=layer_id)

    def get_ground(self):
        return self.get_sprites_from_layer(layer=1)

    def get_dangerous(self):
        return self.get_sprites_from_layer(layer=2)

    def draw(self, surface: Surface, camera_rect) -> None:
        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits((spr.image, spr.rect.move(camera_rect)) for spr in sprites)
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect)
        self.lostsprites = []
