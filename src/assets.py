import os
from pathlib import Path


ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent.joinpath('assets').__str__()


def path_to(*parts: str) -> str:
    orig = Path(ROOT)
    for part in parts:
        orig = orig.joinpath(part)

    return orig.__str__()
