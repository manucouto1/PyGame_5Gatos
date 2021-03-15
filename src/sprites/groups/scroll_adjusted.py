from pygame import Surface
from pygame.sprite import Group, LayeredUpdates


class ScrollAdjustedGroup(Group):
    def __init__(self, camera_scroll, *sprites):
        for sprite in sprites:
            sprite.scroll = camera_scroll
        super().__init__(*sprites)
        self.camera_rect = camera_scroll

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


class ScrollAdjustedLayeredGroup(ScrollAdjustedGroup, LayeredUpdates):
    def __init__(self, camera_scroll, *sprites):
        ScrollAdjustedGroup.__init__(self, camera_scroll)
        LayeredUpdates.__init__(self, *sprites)