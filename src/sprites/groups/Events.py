from src.sprites.groups.scroll_adjusted import ScrollAdjustedGroup
from src.sprites.spritesheet import SpriteSheet
from src.utils import assets


class EventsBuilder:
    def __init__(self, level, container, level_dto):
        super().__init__()
        self.level = level
        self.container = container
        self.events = level_dto.events

    def build(self, camera_scroll):
        return Events(camera_scroll, self)


class Events(ScrollAdjustedGroup):
    def __init__(self, camera_scroll, builder: EventsBuilder):
        super().__init__(camera_scroll)
        sheet = SpriteSheet(builder.container, assets.path_to('characters', 'catcifer', 'standing', 'Sprite-catcifer-standing-Sheet.png'))
        for event in builder.events:
            print('Here one event', event)
            self.add(builder.container.object_from_name(event.path, sheet, event, builder.level))
