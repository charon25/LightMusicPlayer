import os
import random

import pygame.mixer as mixer


VALID_FORMATS = ['wav', 'mp3', 'ogg']


class MusicManager:
    def __init__(self, path: str):
        self.path = path if path.endswith('\\') else path + '\\'
        self.files: list[str] = list()
        self.currently_playing: str = None
        mixer.init()
        mixer.music.set_volume(1.0)

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
        if len(self.files) == 1:
            self.currently_playing = self.files[0]
        else:
            playing = self.currently_playing
            while playing == self.currently_playing:
                playing = random.choice(self.files)
            self.currently_playing = playing

        mixer.music.load(self.currently_playing)
        mixer.music.play(loops=0)

    def get_current_name(self) -> str:
        if self.currently_playing is None:
            return 'Aucune musique courante'

        return '.'.join(self.currently_playing.split('\\')[-1].split('.')[:-1])
