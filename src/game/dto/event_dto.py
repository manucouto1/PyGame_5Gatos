

class EventDTO:
    def __init__(self, event):
        self.path = event['path']
        self.scale = event['scale']
        try:
            scale = int(event['scale'])
            self.pos = (int(event['x']) * scale, int(event['y']) * scale)
        except Exception:
            self.pos = (event['x'], event['y'])
