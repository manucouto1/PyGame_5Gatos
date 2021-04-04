import src.utils.assets as assets
import pygame as pg


class Container:
    def __init__(self):
        self.clazz = {}
        self.DTOs = {}
        self.images = {}
        self.sound = {}
        self.objects = {}

    def set_object(self, name, obj):
        key = name.__hash__()
        self.objects[key] = obj

    def get_object(self, name):
        key = name.__hash__()
        if key in self.objects:
            return self.objects[key]
        else:
            return None

    def image_from_path(self, path):
        key = path.__hash__()
        if key in self.images:
            return self.images[key]
        else:
            try:
                f = pg.image.load(path)
                self.images[key] = f
            except Exception:
                print('Unable to load spritesheet image:', path)
                raise SystemExit

            return self.images[key]

    def image_from_parts(self, *parts: str):
        path = assets.path_to(*parts)
        return self.image_from_path(path)

    def object_from_name(self, path, *args):

        key = path.__hash__()
        if key in self.clazz:
            m = self.clazz[key]
            return m(*args)
        else:
            m = assets.get_class(path)
            self.clazz[key] = m
            return m(*args)
