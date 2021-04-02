import pygame
from game import BLACK

ENEMY_BLUE = (0, 69, 232)

class Enemy:
    def __init__(self, path, spawn_index, speed):
        self.outer_radius = 15
        self.inner_radius = 9
        self.speed = speed

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
            self.target_index = (self.target_index+1) % len(self.vectors) 
        

         

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

    SPEED = 6


    level.add_enemy(Enemy(e1_path, 0, SPEED))
    level.add_enemy(Enemy(e2_path, 1, SPEED))
    level.add_enemy(Enemy(e3_path, 0, SPEED))
    level.add_enemy(Enemy(e4_path, 1, SPEED))

    return level.enemies


def level_two():
    level = EnemyLevel()

    e1_path = [(425, 425), (425, 675)]
    e2_path = [(475, 425), (475, 675)]
    e3_path = [(525, 425), (525, 675)]
    e4_path = [(575, 425), (575, 675)]
    e5_path = [(625, 425), (625, 675)]
    e6_path = [(675, 425), (675, 675)]
    e7_path = [(725, 425), (725, 675)]
    e8_path = [(775, 425), (775, 675)]
    e9_path = [(825, 425), (825, 675)]
    e10_path = [(875, 425), (875, 675)]
    e11_path = [(925, 425), (925, 675)]
    e12_path = [(975, 425), (975, 675)]


    SPEED = 4

    level.add_enemy(Enemy(e1_path, 0, SPEED))
    level.add_enemy(Enemy(e2_path, 1, SPEED))
    level.add_enemy(Enemy(e3_path, 0, SPEED))
    level.add_enemy(Enemy(e4_path, 1, SPEED))
    level.add_enemy(Enemy(e5_path, 0, SPEED))
    level.add_enemy(Enemy(e6_path, 1, SPEED))
    level.add_enemy(Enemy(e7_path, 0, SPEED))
    level.add_enemy(Enemy(e8_path, 1, SPEED))
    level.add_enemy(Enemy(e9_path, 0, SPEED))
    level.add_enemy(Enemy(e10_path, 1, SPEED))
    level.add_enemy(Enemy(e11_path, 0, SPEED))
    level.add_enemy(Enemy(e12_path, 1, SPEED))

    return level.enemies