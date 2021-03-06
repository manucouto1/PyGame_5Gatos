
class EntityDTO:
    def __init__(self, entity):
        self.name = entity['name']
        try:
            scale = int(entity['scale'])
            self.pos = (int(entity['x'])*scale, int(entity['y'])*scale)
        except Exception:
            self.pos = (entity['x'], entity['y'])

