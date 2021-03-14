from pygame.sprite import LayeredUpdates
from src.sprites.groups.custom import CustomGroup


class CustomLayeredGroup(CustomGroup, LayeredUpdates):
    def __init__(self, camera_rect, *sprites):
        CustomGroup.__init__(self, camera_rect)
        LayeredUpdates.__init__(self, *sprites)
