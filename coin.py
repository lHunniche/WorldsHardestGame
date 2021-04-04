import pygame
from game import BLACK

COIN_YELLOW = (255, 213, 0)

class Coin:
    def __init__(self, x, y):
        self.outer_radius = 13
        self.inner_radius = 7
        self.rect = pygame.Rect(0,0,self.outer_radius*2, self.outer_radius*2)
        self.rect.centerx = x
        self.rect.centery = y
        self.inner_color = COIN_YELLOW
        self.outer_color = BLACK



class CoinLevel:
    def __init__(self):
        self.coins = []

    def add_coin(self, coin):
        self.coins.append(coin)

    
def level_two():
    level = CoinLevel()

    c1 = Coin(700, 550)

    level.add_coin(c1)

    return level.coins