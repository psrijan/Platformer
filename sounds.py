import pygame
import os
from enum import Enum

pygame.mixer.init()


class SoundType(Enum):
    SHOT = ("shot", "wav")
    EXPLOSION = ("explosion", "wav")
    HURT = ("hurt", "wav")
    POWER_UP = ("power_up", "wav")
    JUMP = ("jump", "wav")
    LAUNCH_GRANADE = ("launch_granade", "wav")

    @staticmethod
    def from_str(label):
        label = label.lower()
        if label == "shot":
            return SoundType.SHOT
        elif label == "explosion":
            return SoundType.EXPLOSION
        elif label == "hurt":
            return SoundType.HURT
        elif label == "power_up":
            return SoundType.POWER_UP
        elif label == "jump":
            return SoundType.JUMP
        elif label == "launch_granade":
            return SoundType.LAUNCH_GRANADE
        else:
            raise Exception("Label not found Exception")


class SoundModule:

    def __init__(self):
        self.sound_dict = {}
        sounds = os.listdir("./assets/sounds/")
        print(f"sounds {sounds}")

        for sound_name in sounds:
            loaded_sound = pygame.mixer.Sound(f"./assets/sounds/{sound_name}")
            name = sound_name.split(".")[0]
            try:
                label = SoundType.from_str(name)
                self.sound_dict[label] = loaded_sound
            except Exception:
                print("No label found")

    def shoot(self, vol=.5) :
        sound = self.sound_dict[SoundType.SHOT]
        self._play(sound, vol)

    def explosion(self, vol=.5):
        sound = self.sound_dict[SoundType.EXPLOSION]
        self._play(sound, vol)
    def jump(self, vol=.5):
        sound = self.sound_dict[SoundType.JUMP]
        self._play(sound, vol)

    def launch_granade(self, vol=.5):
        sound = self.sound_dict[SoundType.LAUNCH_GRANADE]
        self._play(sound, vol)

    def _play(self, sound, vol):
        sound.set_volume(vol)
        sound.play()