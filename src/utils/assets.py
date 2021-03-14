import os
from pathlib import Path
import pygame as pg

ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.joinpath('assets').__str__()

cached = {}


def load_image(*parts: str):
    path = path_to(*parts)
    key = path.__hash__()
    if key in cached:
        return cached[key]
    else:
        try:
            f = pg.image.load(path)
            cached[key] = f
        except Exception:
            print('Unable to load spritesheet image:', path)
            raise SystemExit

        return cached[key]


def path_to(*parts: str):
    orig = Path(ROOT)
    for part in parts:
        orig = orig.joinpath(part)

    return orig.__str__()
