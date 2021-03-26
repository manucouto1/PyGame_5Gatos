from src.sprites.groups.scroll_adjusted import ScrollAdjustedGroup
from src.sprites.spritesheet import SpriteSheet
from src.utils import assets


class EventsBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        self.events = level_dto.events

    def build(self, level, camera_scroll):
        return Events(camera_scroll, level, self)


class Events(ScrollAdjustedGroup):
    def __init__(self, camera_scroll, level, builder: EventsBuilder):
        super().__init__(camera_scroll)
        sheet = SpriteSheet(builder.container, assets.path_to('characters', 'catcifer', 'standing', 'Sprite-catcifer-standing-Sheet.png'))
        for event in builder.events:
            self.add(builder.container.object_from_name(event.path, sheet, event, level))
