import pygame
from game import BLACK

ENEMY_BLUE = (0, 69, 232)

class Enemy:
    def __init__(self, path, speed):
        self.outer_radius = 13
        self.inner_radius = 7
        self.speed = speed

        self.rect = pygame.Rect(0,0,self.outer_radius*2, self.outer_radius*2)
        self.inner_color = ENEMY_BLUE
        self.outer_color = BLACK
        self.path = path
        self.rect.centerx = self.path[0][0]
        self.rect.centery = self.path[0][1]
        self.target_index = 1 % len(path)
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
        #print(direction_vector)

        # check if we should switch target vector
        if target_vector.distance_to(self.rect.center) < self.speed:
            self.rect.centerx = self.vectors[self.target_index].x
            self.rect.centery = self.vectors[self.target_index].y
            self.target_index = (self.target_index+1) % len(self.vectors)
