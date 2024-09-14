import os
import time

import pygame
from pygame._sdl2 import Window

from default_path import DEFAULT_PATH
from event_manager import EventManager
from music_manager import MusicManager

try:
    with open('last_position.txt', 'r') as fi:
        x, y = map(int, fi.read().splitlines()[0].split(','))
except:
    with open('last_position.txt', 'w') as fo:
        fo.write('200,200')
    x, y = 200, 200

os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

with open('times.txt', 'a') as fo:
    fo.write(f"start={time.time()}\n")

pygame.init()
pygame.display.init()
window = pygame.display.set_mode((300, 70))
window_info = Window.from_display_module()
previous_position = window_info.position

pygame.display.set_icon(pygame.image.load("icon.png"))

PLAY = pygame.image.load("play.png")
PLAY_RECT = pygame.Rect(10, 10, 50, 50)
PAUSE = pygame.image.load("pause.png")
NEXT = pygame.image.load("next.png")
NEXT_RECT = pygame.Rect(10 + PLAY.get_width() + 10, 10, 50, 50)

VOLUME_COLOR = (20, 20, 20)
VOLUME_UNSELECTED_COLOR = (200, 200, 200)
VOLUME_RECT = pygame.Rect(130, 31, 160, 8)
VOLUME_HITBOX = pygame.Rect(VOLUME_RECT.left, 10, VOLUME_RECT.width, 50)

FONT = pygame.font.SysFont("arial", 10)

try:
    with open('path.txt', 'r', encoding='utf-8') as fi:
        path = fi.read().splitlines()[0]
except:
    print('"path.txt" file not found, using default path and creating it...')
    with open('path.txt', 'w', encoding='utf-8') as fo:
        fo.write(DEFAULT_PATH)

    path = DEFAULT_PATH

try:
    with open('playlist.txt', 'r', encoding='utf-8') as fi:
        playlist = fi.read().splitlines()[0]
except:
    playlist = ""

try:
    with open('volume.txt', 'r', encoding='utf-8') as fi:
        volume = float(fi.read().splitlines()[0])
except:
    print('"volume.txt" file not found, using default volume and creating it...')
    volume = 0.5
    with open('volume.txt', 'w', encoding='utf-8') as fo:
        fo.write(str(volume))

event_manager = EventManager()

music_manager = MusicManager(path)
music_manager.load(playlist)
music_manager.set_volume(volume)

running = True
playing = True
changing_volume = False


def stop():
    global running
    running = False


def toggle_play():
    global playing
    playing = not playing
    if playing:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()


def next_music():
    music_manager.play_next()
    pygame.display.set_caption(f'[{len(music_manager.files)}] {music_manager.get_current_name()}')


next_music()


def on_click(data: dict):
    global changing_volume

    if data['button'] != 1:
        return

    changing_volume = False
    x, y = data['pos']
    if PLAY_RECT.collidepoint(x, y):
        toggle_play()
    elif NEXT_RECT.collidepoint(x, y):
        next_music()
    elif VOLUME_HITBOX.collidepoint(x, y):
        changing_volume = True
        music_manager.set_volume((x - VOLUME_HITBOX.left) / VOLUME_HITBOX.width)


def on_mouse_move(data: dict):
    if data['buttons'][0] != 1:
        return

    x, y = data['pos']
    if changing_volume:
        music_manager.set_volume((x - VOLUME_HITBOX.left) / VOLUME_HITBOX.width)


def get_volume_delta(mod: int):
    if mod & pygame.KMOD_CTRL > 0:
        return 0.001
    if mod & pygame.KMOD_SHIFT > 0:
        return 0.1
    return 0.01


def on_key(data: dict):
    key = data['unicode']
    mod = data['mod']
    if key == ' ' or key == 'p':
        toggle_play()
    elif key == 'n':
        next_music()
    elif key == '+':
        music_manager.set_volume(music_manager.volume + get_volume_delta(mod))
    elif key == '-':
        music_manager.set_volume(music_manager.volume - get_volume_delta(mod))


event_manager.set_quit_callback(stop)
event_manager.set_mouse_button_down_callback(on_click)
event_manager.set_mouse_motion_callback(on_mouse_move)
event_manager.set_key_down_callback(on_key)
event_manager.set_music_end_callback(next_music)

while running:
    current_position = window_info.position
    if current_position != previous_position:
        x, y = current_position
        with open('last_position.txt', 'w') as fo:
            fo.write(f'{x},{y}')
        previous_position = current_position

    event_manager.listen()
    screen = pygame.Surface((300, 100))
    screen.fill((230, 230, 230))

    screen.blit(PAUSE if playing else PLAY, PLAY_RECT.topleft)

    screen.blit(NEXT, NEXT_RECT.topleft)

    volume_rect = pygame.Rect(VOLUME_RECT.topleft, (int(music_manager.volume * VOLUME_RECT.width), VOLUME_RECT.height))
    pygame.draw.rect(screen, VOLUME_UNSELECTED_COLOR, VOLUME_RECT)
    pygame.draw.rect(screen, VOLUME_COLOR, volume_rect)

    text = FONT.render(f'{100 * music_manager.volume:.1f} %', True, VOLUME_COLOR)
    screen.blit(text, (VOLUME_RECT.left + (VOLUME_RECT.width - text.get_width()) / 2, VOLUME_RECT.bottom + 5))

    window.blit(screen, (0, 0))
    pygame.display.update()

pygame.display.quit()
pygame.quit()

with open('times.txt', 'a') as fo:
    fo.write(f"stop={time.time()}\n")
