from pygame import Surface
from pygame.sprite import Group


class CustomGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

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