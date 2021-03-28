'''Doc String'''
import pygame
import random
from player import Player
from level import Level, LevelGen, WALL


clock = pygame.time.Clock()
size = (1400, 1050) #1400×1050
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Worlds Hardest Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COLOR_BACKGROUND = (190, 173, 255)
LEVELS = []


def handle_keydown_event(event, screen):
    if event.key == pygame.K_SPACE:
        first_rect = pygame.Rect(200, 200, 50, 50)
        second_rect = pygame.Rect(225, 255, 50, 50)
        pygame.draw.rect(screen, GREEN, first_rect)
        pygame.draw.rect(screen, GREEN, second_rect)
        pygame.display.flip()
        print("Drawn")


def init_levels():
    global LEVELS
    #LEVELS.append(Level(LevelGen.all_floor()))
    LEVELS.append(Level(LevelGen.level_1()))

def play():
    keep_playing = True
    current_level_index = 0
    player = Player(LEVELS[current_level_index].spawn)
    


    while keep_playing:
        # main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_playing = False
            if event.type == pygame.KEYDOWN:
                handle_keydown_event(event, screen)


        # game logic here
        keys = pygame.key.get_pressed()
        player.move(keys, LEVELS[current_level_index])

        # drawing goes here
        screen.fill(COLOR_BACKGROUND)
        LEVELS[current_level_index].draw(screen)
        player.draw(screen)
        
        
        # update screen
        pygame.display.flip()


        # limit game to 60 fps
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    init_levels()
    play()
    pygame.quit()