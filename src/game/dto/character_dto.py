
class CharacterDTO:
    def __init__(self, character):
        self.name = character['name']
        self.sheet = character['sheet']
        self.projectile = character['projectile']
        self.rows = character['rows']
        self.path = character['path']
