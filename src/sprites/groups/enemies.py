from src.sprites.groups.scroll_adjusted import ScrollAdjustedLayeredGroup


class EnemiesBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        self.level_dto = level_dto

    def build(self, container, camera_scroll):
        return Enemies(container, camera_scroll, self)


class Enemies(ScrollAdjustedLayeredGroup):
    def __init__(self, container, camera_scroll, builder: EnemiesBuilder):
        super().__init__(camera_scroll)

        for entity in builder.level_dto.enemies:
            self.add(container.object_from_name(entity.path, container, entity))
