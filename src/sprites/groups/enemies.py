from src.sprites.groups.scroll_adjusted import ScrollAdjustedLayeredGroup


class EnemiesBuilder:
    def __init__(self, container, level_dto):
        self.container = container
        self.level_dto = level_dto

    def build(self, camera_scroll):
        return Enemies(camera_scroll, self)


class Enemies(ScrollAdjustedLayeredGroup):
    def __init__(self, camera_scroll, builder: EnemiesBuilder):
        super().__init__(camera_scroll)
        game = builder.container.get_object('game')
        for entity in builder.level_dto.enemies:
            character = game.characters[entity.name]
            self.add(builder.container.object_from_name(character.path, builder.container, entity, character))
