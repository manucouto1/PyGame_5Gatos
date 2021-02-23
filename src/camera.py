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
            self.cam += (pg.Vector2((x, y)) - self.cam) * 0.05
            self.cam.x = max(-(self.world_size.width - self.screen_size.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height - self.screen_size.height), min(0, self.cam.y))

    def draw(self, surface):
        dirty = self.lostsprites
        self.lostsprites = []
        init_rect = self._init_rect
        for sprite in self.sprites():
            rect = self.spritedict[sprite]
            new_rect = surface.blit(sprite.image, sprite.rect.move(self.cam))
            if rect is init_rect:
                dirty.append(new_rect)
            else:
                if new_rect.colliderect(rect):
                    dirty.append(new_rect.union(rect))
                else:
                    dirty.append(new_rect)
                    dirty.append(rect)
            self.spritedict[sprite] = new_rect
        return dirty
