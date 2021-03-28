import pygame.mixer as mixer

from src.utils import assets

MAX_VOLUME = 0.8


class Mixer:
    def __init__(self):
        self.changed = False
        self.playing = False
        self.jump_sound = None
        self.shoot_sound = None
        self.hero_hit_sound = None
        self.enemy_hit_sound = None
        self.destroy_enemy_sound = None
        self.button_click_sound = None

        self.music = None

    @staticmethod
    def load_sound(sound):
        return mixer.Sound(assets.path_to("sounds", sound)) if sound else None

    def load_new_profile(self, sound_dto):
        self.jump_sound = self.load_sound(sound_dto.jump)
        self.shoot_sound = self.load_sound(sound_dto.shoot)
        self.hero_hit_sound = self.load_sound(sound_dto.hero_hit)
        self.enemy_hit_sound = self.load_sound(sound_dto.enemy_hit)
        self.destroy_enemy_sound = self.load_sound(sound_dto.destroy_enemy)
        self.button_click_sound = self.load_sound(sound_dto.button_click)

    def load_music(self, music):
        if music != self.music:
            mixer.music.stop()
            self.playing = False
            mixer.music.unload()
            mixer.music.load(assets.path_to("sounds", music))
            if not mixer.get_busy():
                mixer.music.play(-1)
                mixer.music.set_volume(MAX_VOLUME)
                self.playing = True
            self.music = music

    def play_jump(self):
        self.jump_sound.play() if self.jump_sound else print("Jump not loaded")

    def play_shoot(self):
        self.shoot_sound.play() if self.shoot_sound else print("Shoot not loaded")

    def play_hero_hit(self):
        self.hero_hit_sound.play() if self.hero_hit_sound else print("Hero hit not loaded")

    def play_enemy_hit(self):
        self.enemy_hit_sound.play() if self.enemy_hit_sound else print("Enemy hit not loaded")

    def play_destroy_enemy(self):
        self.enemy_hit_sound.stop() if self.enemy_hit_sound else print("Enemy hit not loaded")
        self.destroy_enemy_sound.play() if self.destroy_enemy_sound else print("Destroy enemy not loaded")

    def play_button_click(self):
        self.button_click_sound.play()

    def check_busy(self):
        if not mixer.get_busy() and not self.playing:
            mixer.music.play(-1)
            mixer.music.set_volume(MAX_VOLUME)
            self.playing = True

        if mixer.get_busy() and not self.changed:
            mixer.music.set_volume(MAX_VOLUME * 0.3)

            self.changed = True

        elif not mixer.get_busy() and self.changed:
            mixer.music.set_volume(MAX_VOLUME)
            self.changed = False
