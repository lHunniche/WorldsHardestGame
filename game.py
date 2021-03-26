'''Doc String'''
import pygame
import random
from player import Player


clock = pygame.time.Clock()
size = (1400, 1050) #1400×1050
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Worlds Hardest Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COLOR_BACKGROUND = (190, 173, 255)

def handle_keydown_event(event):
    pass


def play():
    keep_playing = True
    player = Player()
    while keep_playing:
        # main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_playing = False
            if event.type == pygame.KEYDOWN:
                handle_keydown_event(event)


        # game logic here
        keys = pygame.key.get_pressed()
        player.move(keys)

        # drawing goes here
        screen.fill(COLOR_BACKGROUND)
        player.draw(screen)

        # update screen
        pygame.display.flip()

        # limit game to 60 fps
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    play()
    pygame.quit()