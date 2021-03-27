from src.sprites.active.shooter_entity import ShooterEntity
import numpy as np


class EnemyTurretShooter(ShooterEntity):
    def __init__(self, container, entity, *groups):
        ShooterEntity.__init__(self, container, entity, *groups)
        self.hero = container.get_object('hero')
        self.e_bullets = container.get_object('e_bullets')
        self.walk_count = 0
        self.life = 2
        self.dead_id = 0
        self.dt_count = 0
        self.wait_time = 900/5
        self.shots = 0

        self.sheet[0].set_frames_skip(2)
        self.sheet[1].set_frames_skip(2)
        self.sheet[2].set_frames_skip(2)
        self.sheet[3].set_frames_skip(2)

    def move(self, dt):
        a = (self.rect.x - self.hero.rect.x) ** 2
        b = (self.rect.y - self.hero.rect.y) ** 2

        distance = np.sqrt(a + b)
        self.dt_count += dt

        if distance < 300:
            if self.shots < 5:
                if self.dt_count >= self.wait_time:
                    self.wait_time = 450 / 5
                    self.dt_count = 0
                    bullet = self.shoot((self.hero.rect.x, self.hero.rect.y))
                    self.e_bullets.add(bullet)
                    self.shots += 1
            else:
                self.wait_time = 14400 / 5
                self.shots = 0
        else:
            self.wait_time = 450 / 5

    def dead_loop(self, dt):
        self.image = self.sheet[3].next(dt)
        self.mask = self.sheet.get_mask()

    def update(self, platforms, dt):
        if self.life > 0:
            self.idle_loop(dt)
            self.move(dt)
            self.apply(platforms, dt)
        else:
            self.vel.x = 0
            self.dead_loop(dt)
            self.apply(platforms, dt)

    def is_hit(self):
        self.life -= 1