
class CharacterDTO:
    def __init__(self, character):
        self.layer = character['layer']
        self.name = character['name']
        self.width = character['width']
        self.height = character['height']
        self.rescale_x = character['rescale_x']
        self.rescale_y = character['rescale_y']
        self.sheet = character['sheet']
        self.projectile = character['projectile']
        self.rows = character['rows']
        self.path = character['path']
