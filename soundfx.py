import pygame

pygame.mixer.init()
class SoundFX:
    #def __init__(self):
    #    self.player_hit = pygame.mixer.Sound("/resources/smack.wav")
    player_hit = pygame.mixer.Sound("resources/smack.wav")
    point = pygame.mixer.Sound("resources/ding.wav")
    music = pygame.mixer.Sound("resources/music.wav")
    