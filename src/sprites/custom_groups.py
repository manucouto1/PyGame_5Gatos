from pygame import Surface
from pygame.sprite import Group


class CustomGroup(Group):
    def __init__(self, camera_rect, *sprites):
        super().__init__(*sprites)
        self.camera_rect = camera_rect

    def draw(self, surface: Surface) -> None:
        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits((spr.image, spr.rect.move(self.camera_rect)) for spr in sprites)
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect)
        self.lostsprites = []