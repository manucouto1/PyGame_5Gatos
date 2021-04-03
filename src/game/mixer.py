import pygame.mixer as mixer

from src.utils import assets

MAX_MUSIC_VOLUME = 0.8
MAX_SOUND_VOLUME = 1


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
        self.point_sound = None
        self.one_up_sound = None
        self.cookie_sound = None
        self.die_sound = None

        self.music = None
        self.current_music_volume = MAX_MUSIC_VOLUME
        self.current_sound_volume = MAX_SOUND_VOLUME

    @staticmethod
    def load_sound(sound_file):
        return mixer.Sound(assets.path_to("sounds", sound_file)) if sound_file else None

    def get_music_volume(self):
        return self.current_music_volume

    def get_sound_volume(self):
        return self.current_sound_volume

    def load_new_profile(self, sound_dto):
        self.jump_sound = self.load_sound(sound_dto.jump)
        self.shoot_sound = self.load_sound(sound_dto.shoot)
        self.hero_hit_sound = self.load_sound(sound_dto.hero_hit)
        self.enemy_hit_sound = self.load_sound(sound_dto.enemy_hit)
        self.destroy_enemy_sound = self.load_sound(sound_dto.destroy_enemy)
        self.button_click_sound = self.load_sound(sound_dto.button_click)
        self.point_sound = self.load_sound(sound_dto.point)
        self.one_up_sound = self.load_sound(sound_dto.one_up)
        self.cookie_sound = self.load_sound(sound_dto.cookie)
        self.die_sound = self.load_sound(sound_dto.die)

        self.change_profile_volume(self.current_sound_volume)

    def load_music(self, music):
        if music != self.music:
            mixer.music.stop()
            self.playing = False
            mixer.music.unload()
            mixer.music.load(assets.path_to("sounds", music))
            if not mixer.get_busy():
                mixer.music.play(-1)
                mixer.music.set_volume(self.current_music_volume)
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
        mixer.music.stop()
        self.button_click_sound.play()

    def play_point(self):
        self.point_sound.play()

    def play_one_up(self):
        self.one_up_sound.play()

    def play_cookie(self):
        self.cookie_sound.play()

    def play_die(self):
        mixer.music.stop()
        self.die_sound.play()

    def music_louder(self):
        if self.current_music_volume < MAX_MUSIC_VOLUME:
            self.current_music_volume += 0.1
            if self.current_music_volume > MAX_MUSIC_VOLUME:
                self.current_music_volume = MAX_MUSIC_VOLUME
            mixer.music.set_volume(self.current_music_volume)

    def music_lower(self):
        if self.current_music_volume > 0.0:
            self.current_music_volume -= 0.1
            if self.current_music_volume < 0.1:
                self.current_music_volume = 0.0
            mixer.music.set_volume(self.current_music_volume)

    @staticmethod
    def change_volume(sound, volume):
        sound.set_volume(volume) if sound else None

    def change_profile_volume(self, volume):
        self.change_volume(self.jump_sound, 0.7 * volume)
        self.change_volume(self.shoot_sound, volume)
        self.change_volume(self.hero_hit_sound, volume)
        self.change_volume(self.enemy_hit_sound, volume)
        self.change_volume(self.destroy_enemy_sound, volume)
        self.change_volume(self.button_click_sound, volume)
        self.change_volume(self.point_sound, volume)
        self.change_volume(self.one_up_sound, volume)
        self.change_volume(self.cookie_sound, volume)
        self.change_volume(self.die_sound, volume)

    def sound_louder(self):
        if self.current_sound_volume < MAX_SOUND_VOLUME:
            self.current_sound_volume += 0.1
            if self.current_sound_volume > MAX_SOUND_VOLUME:
                self.current_sound_volume = MAX_SOUND_VOLUME
            self.change_profile_volume(self.current_sound_volume)

    def sound_lower(self):
        if self.current_sound_volume > 0.0:
            self.current_sound_volume -= 0.1
            if self.current_sound_volume < 0.1:
                self.current_sound_volume = 0.0
            self.change_profile_volume(self.current_sound_volume)

    def check_busy(self):
        if not mixer.get_busy() and not self.playing:
            mixer.music.play(-1)
            mixer.music.set_volume(self.current_music_volume)
            self.playing = True

        if mixer.get_busy() and not self.changed:
            mixer.music.set_volume(self.current_music_volume * 0.6)

            self.changed = True

        elif not mixer.get_busy() and self.changed:
            mixer.music.set_volume(self.current_music_volume)
            self.changed = False

