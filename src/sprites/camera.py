import pygame as pg


class Camera(pg.sprite.LayeredUpdates):

    def __init__(self, target, world_size, screen_size):
        super().__init__()
        self.target = target
        self.cam = pg.Vector2(0, 0)
        self.world_size = world_size
        self.screen_size = screen_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + self.screen_size.width / 2
            y = -self.target.rect.center[1] + self.screen_size.height / 2
            self.cam += ((pg.Vector2((x, y)) - self.cam) * 0.05)
            self.cam.x = max(-(self.world_size.width - self.screen_size.width), min(0, round(self.cam.x)))
            self.cam.y = max(-(self.world_size.height - self.screen_size.height), min(0, round(self.cam.y)))

    def draw(self, surface: pg.Surface) -> None:
        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits((spr.image, spr.rect.move(self.cam)) for spr in sprites)
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect)
        self.lostsprites = []
