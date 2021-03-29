import pygame
from game import BLACK

ENEMY_BLUE = (0, 69, 232)

class Enemy:
    def __init__(self, path, spawn_index):
        self.outer_radius = 13
        self.inner_radius = 7

        self.rect = pygame.Rect(0,0,self.outer_radius, self.outer_radius)
        self.inner_color = ENEMY_BLUE
        self.outer_color = BLACK
        self.path = path
        self.rect.centerx = self.path[spawn_index][0]
        self.rect.centery = self.path[spawn_index][1]
        self.target_index = (spawn_index+1) % len(path)
        

         

class EnemyLevel:
    def __init__(self):
        self.enemies = []

    def add_enemy(self, enemy):
        self.enemies.append(enemy)



def level_one():
    # (475,475) -> (925,475) (X,Y)
    level = EnemyLevel()
    e1_path = [(475, 475), (925, 475)]
    e2_path = [(475, 525), (925, 525)]
    e3_path = [(475, 575), (925, 575)]
    e4_path = [(475, 625), (925, 625)]


    level.add_enemy(Enemy(e1_path, 0))
    level.add_enemy(Enemy(e2_path, 1))
    level.add_enemy(Enemy(e3_path, 0))
    level.add_enemy(Enemy(e4_path, 1))

    return level.enemies