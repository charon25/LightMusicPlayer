import os
import random

import pygame.mixer as mixer

import event_manager

VALID_FORMATS = ['wav', 'mp3', 'ogg']


class MusicManager:
    def __init__(self, path: str):
        self.path = path if path.endswith('\\') else path + '\\'
        self.files: list[str] = list()
        self.currently_playing: str = None
        self.volume: float = 0.0
        mixer.init()
        mixer.music.set_volume(0.0)
        mixer.music.set_endevent(event_manager.MUSICENDEVENT)

    def load(self, playlist: str):
        playlist_path = self.path + (playlist if playlist.endswith('\\') else playlist + '\\')
        for file in os.listdir(playlist_path):
            if not any(file.endswith(fm) for fm in VALID_FORMATS):
                continue
            filepath = playlist_path + file
            self.files.append(filepath)

        if not self.files:
            exit()

    def play_next(self):
        self.currently_playing = random.choice(self.files)

        mixer.music.load(self.currently_playing)
        mixer.music.play(loops=0)

    def get_current_name(self) -> str:
        if self.currently_playing is None:
            return 'Aucune musique courante'

        return '.'.join(self.currently_playing.split('\\')[-1].split('.')[:-1])

    def set_volume(self, volume: float):
        self.volume = min(1.0, max(0.0, volume))
        mixer.music.set_volume(self.volume)
        with open('volume.txt', 'w') as fo:
            fo.write(str(self.volume))
