class Layer:

    def __init__(self, name, level_name, positions, tile_size, *groups):
        self.name = name
        self.platforms_list = []

        for position in positions:
            self.platforms_list.append()
            # TODO
