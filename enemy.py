import pygame
from game import BLACK

ENEMY_BLUE = (0, 69, 232)

SPEED_MEDIUM = 5
SPEED_FAST = 8
SPEED_FASTER = 10

class Enemy:
    def __init__(self, path, spawn_index, speed):
        self.outer_radius = 13
        self.inner_radius = 7
        self.speed = 5

        self.rect = pygame.Rect(0,0,self.outer_radius*2, self.outer_radius*2)
        self.inner_color = ENEMY_BLUE
        self.outer_color = BLACK
        self.path = path
        self.rect.centerx = self.path[spawn_index][0]
        self.rect.centery = self.path[spawn_index][1]
        self.target_index = (spawn_index+1) % len(path)
        self.vectors = self.make_vectors_from_path()

    def make_vectors_from_path(self):
        vectors = []
        for x,y in self.path:
            vectors.append(pygame.Vector2(x,y))
        return vectors

    def move(self):
        # move enemy towards target point
        target_vector = self.vectors[self.target_index]
        direction_vector = (target_vector - self.rect.center).normalize()*self.speed
        self.rect.move_ip(direction_vector)

        # check if we should switch target vector
        if target_vector.distance_to(self.rect.center) < self.speed:
            self.target_index = (self.target_index+1)%len(self.vectors) 
        

         

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


    level.add_enemy(Enemy(e1_path, 0, SPEED_MEDIUM))
    level.add_enemy(Enemy(e2_path, 1, SPEED_MEDIUM))
    level.add_enemy(Enemy(e3_path, 0, SPEED_MEDIUM))
    level.add_enemy(Enemy(e4_path, 1, SPEED_MEDIUM))

    return level.enemies