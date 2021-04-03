'''Doc String'''
import pygame
import random
from player import Player
from level import Level, LevelGen


pygame.font.init()
myfont = pygame.font.SysFont('Tahoma', 60)

clock = pygame.time.Clock()
width, height = 1400, 1050
size = (width, height) #1400×1050
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Worlds Hardest Game")



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COLOR_BACKGROUND = (190, 173, 255)
YELLOW = (255, 255, 0)
ENEMY_BLUE = (0, 69, 232)
LEVELS = []
TEXT_FRAMES = 5

STATE_PLAYING = 0
STATE_CHANGING_LEVELS = 1
STATE_MENU = 2


def handle_keydown_event(event, screen):
    pass
    #if event.key == pygame.K_SPACE:
        #first_rect = pygame.Rect(200, 200, 50, 50)
        #second_rect = pygame.Rect(225, 255, 50, 50)
        #pygame.draw.rect(screen, GREEN, first_rect)
        #pygame.draw.rect(screen, GREEN, second_rect)
        #pygame.display.flip()


def init_levels():
    global LEVELS
    LEVELS = LevelGen.load_levels()[-1:]


def play():
    from soundfx import SoundFX
    #SoundFX.music.play()

    keep_playing = True
    current_level_index = 0
    player = Player(LEVELS[current_level_index].spawn)
    current_state = STATE_CHANGING_LEVELS
    text_surface = myfont.render('GET READY', False, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(width//2, height//2))
    text_counter = 0
    

    while keep_playing:
        # main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_playing = False
            if event.type == pygame.KEYDOWN:
                handle_keydown_event(event, screen)

        if current_state == STATE_CHANGING_LEVELS:
            if text_counter < TEXT_FRAMES:
                screen.fill(COLOR_BACKGROUND)
                screen.blit(text_surface, text_rect)
                text_counter += 1
            else:
                current_state = STATE_PLAYING

        elif current_state == STATE_PLAYING:
            # game logic here
            keys = pygame.key.get_pressed()
            player.move(keys, LEVELS[current_level_index])
            LEVELS[current_level_index].move_enemies()
            LEVELS[current_level_index].check_collision_with_player(player)
            LEVELS[current_level_index].check_collision_with_coin(player)

            if LEVELS[current_level_index].player_reached_goal(player):
                current_level_index += 1
                player = Player(LEVELS[current_level_index].spawn)
                continue

            # drawing goes here
            screen.fill(COLOR_BACKGROUND)
            LEVELS[current_level_index].draw_level(screen)
            player.draw(screen)
            #print("X: {} - Y: {}".format(player.black_rect.centerx, player.black_rect.centery))

    
        # update screen
        pygame.display.flip()


        # limit game to 60 fps
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    init_levels()
    play()
    pygame.quit()