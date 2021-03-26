
class GapsDTO:
    def __init__(self, gaps):
        self.name = gaps['name']
        self.list = list(map(lambda gap: dict(map(lambda k, v: (k, v * gaps['scale']), gap.keys(), gap.values())),
                             gaps['gaps']))


