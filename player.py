import pygame

RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 28
        self.speed = 3
        self.red_rect = pygame.Rect(self.x+4, self.y+4, self.size-8, self.size-8)
        self.black_rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.black_rect)
        pygame.draw.rect(screen, RED, self.red_rect)

    def move(self, keys):
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]
        move_up = keys[pygame.K_w]
        move_down = keys[pygame.K_s]

        x_motion = move_left * (self.speed * -1) + move_right * self.speed
        y_motion = move_up * (self.speed * -1) + move_down * self.speed

        self.red_rect.move_ip(x_motion, y_motion)
        self.black_rect.move_ip(x_motion, y_motion)