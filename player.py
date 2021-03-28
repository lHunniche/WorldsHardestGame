import pygame
from level import WALL

RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Player:
    def __init__(self, spawn):
        self.x = spawn[0]
        self.y = spawn[1]
        self.size = 36
        self.gap = 10
        self.speed = 3
        self.red_rect = pygame.Rect(self.x+self.gap/2, self.y+self.gap/2, self.size-self.gap, self.size-self.gap)
        self.black_rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.black_rect)
        pygame.draw.rect(screen, RED, self.red_rect)

    def move(self, keys, level):
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]
        move_up = keys[pygame.K_w]
        move_down = keys[pygame.K_s]

        x_motion = move_left * (self.speed * -1) + move_right * self.speed
        y_motion = move_up * (self.speed * -1) + move_down * self.speed

        # move X axis
        self.red_rect.move_ip(x_motion, 0)
        self.black_rect.move_ip(x_motion, 0)
        self.handle_x_axis_collision(level)

        # move Y axis
        self.red_rect.move_ip(0, y_motion)
        self.black_rect.move_ip(0, y_motion)
        self.handle_y_axis_collision(level)

        self.red_rect.left = self.black_rect.x+self.gap/2
        self.red_rect.top = self.black_rect.y+self.gap/2


    def handle_x_axis_collision(self, level):
        for column in level.tile_array:
            for tile in column:
                if tile is not None and tile.type == WALL:
                    if self.black_rect.colliderect(tile.rect):
                        if self.black_rect.left > tile.rect.left: # player is to the right
                            self.black_rect.left = tile.rect.right
                        if self.black_rect.right < tile.rect.right: #player is to the left
                            self.black_rect.right = tile.rect.left

    def handle_y_axis_collision(self, level):
        for column in level.tile_array:
            for tile in column:
                if tile is not None and tile.type == WALL:
                    if self.black_rect.colliderect(tile.rect):
                        if self.black_rect.top > tile.rect.top: # player is below
                            self.black_rect.top = tile.rect.bottom
                        if self.black_rect.bottom < tile.rect.bottom: # player is above
                            self.black_rect.bottom = tile.rect.top
