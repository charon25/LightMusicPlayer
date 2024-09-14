import pygame

from default_path import DEFAULT_PATH
from event_manager import EventManager
from music_manager import MusicManager

pygame.init()
pygame.display.init()
window = pygame.display.set_mode((300, 70))

# pygame.display.set_icon(pygame.image.load("icon.png"))

PLAY = pygame.image.load("play.png")
PLAY_RECT = pygame.Rect(10, 10, 50, 50)
PAUSE = pygame.image.load("pause.png")
NEXT = pygame.image.load("next.png")
NEXT_RECT = pygame.Rect(10 + PLAY.get_width() + 10, 10, 50, 50)

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

event_manager = EventManager()

music_manager = MusicManager(path)
music_manager.load(playlist)

running = True
playing = True


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
    pygame.display.set_caption(music_manager.get_current_name())


next_music()


def on_click(data: dict):
    if data['button'] != 1:
        return
    x, y = data['pos']
    if PLAY_RECT.collidepoint(x, y):
        toggle_play()
    elif NEXT_RECT.collidepoint(x, y):
        next_music()


event_manager.set_quit_callback(stop)
event_manager.set_mouse_button_down_callback(on_click)

while running:
    event_manager.listen()
    screen = pygame.Surface((300, 100))
    screen.fill((230, 230, 230))

    screen.blit(PAUSE if playing else PLAY, PLAY_RECT.topleft)

    screen.blit(NEXT, NEXT_RECT.topleft)

    window.blit(screen, (0, 0))
    pygame.display.update()

pygame.display.quit()
pygame.quit()
