
class EntityDTO:
    def __init__(self, entity):
        self.name = entity['name']
        self.sheet = entity['sheet']
        self.path = entity['path']
        self.pos = (entity['x'], entity['y'])
