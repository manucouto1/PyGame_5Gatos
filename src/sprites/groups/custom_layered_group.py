from pygame import Surface
from pygame.sprite import LayeredUpdates
from src.sprites.groups.custom import Custom


class CustomLayeredGroup(Custom, LayeredUpdates):
    def __init__(self, camera_rect, *sprites):
        Custom.__init__(self, camera_rect)
        LayeredUpdates.__init__(self, *sprites)

