import os
from pathlib import Path
import pygame as pg
from pygame.surface import Surface

ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.joinpath('assets').__str__()

cached = {}


def load_image(*parts: str) -> Surface:
    path = path_to(*parts)
    key = path.__hash__()
    if key in cached:
        return cached[key]
    else:
        f = pg.image.load(path)
        cached[key] = f

        return cached[key]


def path_to(*parts: str) -> str:
    orig = Path(ROOT)
    for part in parts:
        orig = orig.joinpath(part)

    return orig.__str__()
