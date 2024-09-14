import pygame

from event_manager import EventManager

pygame.init()
pygame.display.init()
window = pygame.display.set_mode((300, 70))

# pygame.display.set_icon(pygame.image.load("icon.png"))

PLAY = pygame.image.load("play.png")
PLAY_RECT = pygame.Rect(10, 10, 50, 50)
PAUSE = pygame.image.load("pause.png")
NEXT = pygame.image.load("next.png")
NEXT_RECT = pygame.Rect(10 + PLAY.get_width() + 10, 10, 50, 50)

manager = EventManager()

running = True
playing = True


def stop():
    global running
    running = False


def toggle_play():
    global playing
    playing = not playing


def next_music():
    pass


def on_click(data: dict):
    if data['button'] != 1:
        return
    x, y = data['pos']
    if PLAY_RECT.collidepoint(x, y):
        toggle_play()
    elif NEXT_RECT.collidepoint(x, y):
        next_music()


manager.set_quit_callback(stop)
manager.set_mouse_button_down_callback(on_click)

while running:
    manager.listen()
    screen = pygame.Surface((300, 100))
    screen.fill((230, 230, 230))

    screen.blit(PAUSE if playing else PLAY, PLAY_RECT.topleft)

    screen.blit(NEXT, NEXT_RECT.topleft)

    window.blit(screen, (0, 0))
    pygame.display.update()


pygame.display.quit()
pygame.quit()
