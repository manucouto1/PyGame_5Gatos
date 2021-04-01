import pygame as pg
from src.sprites.groups.scroll_adjusted import ScrollAdjustedGroup


class CameraBuilder:
    def __init__(self, container, level_dto, screen_size):
        self.container = container
        self.world_size = pg.Rect(0, 0, level_dto.map_width * 32, level_dto.map_height * 32)
        self.screen_size = screen_size
        self.gaps = level_dto.gaps

    def build(self, hero):
        return self.container.object_from_name(self.gaps.name, hero, self)


class Camera(ScrollAdjustedGroup):
    """
    Class to manage camera scrolling

    :param target: pygame.Sprite to follow
    :param builder: Camera builder
    """
    def __init__(self, target, builder: CameraBuilder):
        self.scroll = pg.Vector2(0, 0)
        ScrollAdjustedGroup.__init__(self, self.scroll, target)
        self.target = target
        self.world_size = builder.world_size
        self.screen_size = builder.screen_size
        x = -self.target.rect.center[0] + self.screen_size.width / 2
        y = -self.target.rect.center[1] + self.screen_size.height / 2
        self._do_scroll(x, y, 1, 1)
        self.active_id = -1
        print("Cargamos Normal camera")

    def _do_scroll(self, x, y, smooth_x, smooth_y):
        (aux_x, aux_y) = (pg.Vector2((x, y)) - self.scroll)
        self.scroll += pg.Vector2((aux_x*smooth_x, aux_y*smooth_y))
        self._adjust()

    def _adjust(self):
        self.scroll.x = max(-(self.world_size.width - self.screen_size.width), min(0, round(self.scroll.x)))
        self.scroll.y = max(-(self.world_size.height - self.screen_size.height), min(0, round(self.scroll.y)))

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + self.screen_size.width / 2
            y = -self.target.rect.center[1] + self.screen_size.height / 2
            self._do_scroll(x, y, 0.05, 0.01)


class CameraVerticalGap(Camera):
    def __init__(self, target, builder: CameraBuilder):
        super().__init__(target, builder)
        self.gaps = builder.gaps.gaps
        print("Cargamos VerticalGap camera")

    def update(self, *args):
        ScrollAdjustedGroup.update(self, *args)
        if self.target:
            x = -self.target.rect.center[0] + self.screen_size.width / 2
            y = -self.target.rect.center[1] + self.screen_size.height / 2

            for gap in self.gaps:
                if gap["y_init"] < self.target.rect.center[1] < gap["y_end"]:
                    y = -(gap["y_init"]+gap['y_end'])/2 + self.screen_size.height / 2
                    self._do_scroll(x, y, 0.05, 0.05)
                    return

            self._do_scroll(x, y, 0.05, 0.05)


class CameraHorizontalGap(Camera):
    """
    Class to manage camera horizontal scrolling at level gaps

    :param target: pygame.Sprite to follow
    :param builder: Camera builder
    """
    def __init__(self, target, builder: CameraBuilder):
        super().__init__(target, builder)
        self.gaps = builder.gaps.gaps
        self.container = builder.container
        print("Cargamos VerticalGap camera")

    def update(self, *args):
        ScrollAdjustedGroup.update(self, *args)
        if self.target:
            x = -self.target.rect.center[0] + self.screen_size.width / 2
            y = -self.target.rect.center[1] + self.screen_size.height / 2

            for gap in self.gaps:
                if gap["x_init"] < self.target.rect.center[0] < gap["x_end"]:
                    if "action" in gap:
                        o = self.container.get_object('level')
                        getattr(o, gap["action"])()
                    x = -(gap["x_init"]+gap['x_end'])/2 + self.screen_size.width / 2
                    self._do_scroll(x, y, 0.1, 0.1)
                    return

            self._do_scroll(x, y, 0.1, 0.1)


class FallingCamera(Camera):
    """
    Class to manage camera scroll in the free fall level

    :param target: pygame.Sprite to follow
    :param builder: Camera class builder
    """
    def __init__(self, target, builder: CameraBuilder):
        super().__init__(target, builder)
        self.container = builder.container
        self.gaps = builder.gaps.gaps
        self.falling = False
        self.falling_target = 0
        print("Cargamos VerticalGap camera")

    def falling_mode(self):
        self.falling = True
        self.falling_target = self.target.rect.center[1]

    def normal_mode(self):
        self.falling = False

    def update(self, a, b, dt, *args):
        ScrollAdjustedGroup.update(self, a, b, dt, *args)
        if self.target:
            x = -self.target.rect.center[0] + self.screen_size.width / 2
            y = -self.target.rect.center[1] + self.screen_size.height / 2

            for gap in self.gaps:
                if 'x_init' in gap and 'y_init' in gap:
                    if gap["x_init"] < self.target.rect.center[0] < gap["x_end"] and \
                            gap['y_init'] < self.target.rect.center[1] < gap['y_end']:
                        if "action" in gap and gap['id'] != self.active_id:
                            self.active_id = gap['id']
                            o = self.container.get_object('level')
                            getattr(o, gap["action"])()
                        if "center" in gap:
                            if gap["center"] == "x":
                                x = -(gap["x_init"]+gap['x_end'])/2 + self.screen_size.width / 2
                            elif gap["center"] == "y" and not self.falling:
                                y = -(gap["y_init"] + gap['y_end']) / 2 + self.screen_size.height / 2
                            elif gap["center"] == "xy" and not self.falling:
                                x = -(gap["x_init"] + gap['x_end']) / 2 + self.screen_size.width / 2
                                y = -(gap["y_init"] + gap['y_end']) / 2 + self.screen_size.height / 2
                        break
                elif 'x_init' in gap and 'y_init' not in gap:
                    if gap["x_init"] < self.target.rect.center[0] < gap["x_end"]:
                        self.active_id = gap['id']
                        if "action" in gap and gap['id'] != self.active_id:
                            self.active_id = gap['id']
                            o = self.container.get_object('level')
                            getattr(o, gap["action"])()
                        x = -(gap["x_init"] + gap['x_end']) / 2 + self.screen_size.width / 2
                        break
                elif 'y_init' in gap and 'x_init' not in gap and not self.falling:
                    if gap["y_init"] < self.target.rect.center[1] < gap["y_end"]:
                        self.active_id = gap['id']
                        if "action" in gap and gap['id'] != self.active_id:
                            self.active_id = gap['id']
                            o = self.container.get_object('level')
                            getattr(o, gap["action"])()
                        y = -(gap["y_init"] + gap['y_end']) / 2 + self.screen_size.height / 2
                        break

            if self.falling:
                (aux_x, aux_y) = (x - self.scroll.x, -3/50*dt)
                self.scroll += pg.Vector2((aux_x*0.5, aux_y))
                self._adjust()
                print("Falling_mode > ", y)
            else:
                self._do_scroll(x, y, 0.1, 0.1)





