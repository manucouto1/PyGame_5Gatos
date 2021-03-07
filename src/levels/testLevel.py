from game.level import Level
from utils import assets


class TestLevel(Level):
    def __init__(self):
        super().__init__('test_level')
        self.bg = assets.load_image("background.png")
