from src.sprites.groups.scroll_adjusted import ScrollAdjustedGroup
from src.sprites.spritesheet import SpriteSheet
from src.utils import assets


class EventsBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        self.events = level_dto.events
        path = assets.path_to('levels', level_dto.level_name, level_dto.tiles_image)
        sheet = container.image_from_path(path)
        self.sheet = SpriteSheet(sheet)

    def build(self, level, camera_scroll):
        return Events(camera_scroll, level, self)


class Events(ScrollAdjustedGroup):
    def __init__(self, camera_scroll, level, builder: EventsBuilder):
        super().__init__(camera_scroll)
        for event in builder.events:
            self.add(builder.container.object_from_name(event.path, builder.sheet, event, level))
