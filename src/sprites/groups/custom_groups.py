from pygame.sprite import Group
from pygame import Surface
from src.sprites.groups.custom import Custom


class CustomGroup(Custom, Group):
    def __init__(self, camera_rect, *sprites):
        Custom.__init__(self, camera_rect)
        Group.__init__(self, *sprites)

