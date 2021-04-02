'''Doc String'''
import pygame
import random
from player import Player
from level import Level, LevelGen


pygame.font.init()
myfont = pygame.font.SysFont('Tahoma', 50)

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
        #print("Drawn")


def draw_an_enemy(screen):
    enemy_rect = pygame.Rect(0,0, 20, 20)
    enemy_rect.center = (475, 475)
    pygame.draw.circle(screen, BLACK, enemy_rect.center, 13)
    pygame.draw.circle(screen, ENEMY_BLUE, enemy_rect.center, 7)


def init_levels():
    global LEVELS, enemy_level
    import enemy
    import coin
    #LEVELS.append(Level(LevelGen.level_1()).set_enemies(enemy.level_one()))
    LEVELS.append(Level(LevelGen.level_2()).set_enemies(enemy.level_two()).set_coins(coin.level_two()))

    LEVELS.append(Level(LevelGen.all_floor()).set_enemies([]))


def play():
    from soundfx import SoundFX
    #SoundFX.music.play()

    keep_playing = True
    current_level_index = 0
    player = Player(LEVELS[current_level_index].spawn)
    current_state = STATE_CHANGING_LEVELS
    text_surface = myfont.render('Get Ready', False, (0, 0, 0))
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
                screen.blit(text_surface,(width/2-100, height/2-100))
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
            print("X: {} - Y: {}".format(player.black_rect.centerx, player.black_rect.centery))

    
        # update screen
        pygame.display.flip()


        # limit game to 60 fps
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    init_levels()
    play()
    pygame.quit()