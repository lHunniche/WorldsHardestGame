import pygame
from level import WALL

RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Player:
    def __init__(self, spawn):
        self.x = spawn[0]
        self.y = spawn[1]
        self.size = 40
        self.gap = 10
        self.speed = 3
        self.red_rect = pygame.Rect(self.x+self.gap/2, self.y+self.gap/2, self.size-self.gap, self.size-self.gap)
        self.black_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.red_rect.center = (self.x, self.y)
        self.black_rect.center = (self.x, self.y)
        self.alive = True
        self.death_frames = 45
        self.death_frame_counter = 0
        self.spawn_coordinates = None
        self.black_surface = pygame.Surface((self.black_rect.width, self.black_rect.height)) 
        self.red_surface = pygame.Surface((self.red_rect.width, self.red_rect.height)) 


    
    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, BLACK, self.black_rect)
            pygame.draw.rect(screen, RED, self.red_rect)
        else:
            if self.death_frame_counter != self.death_frames: # render dying player
               
                self.black_surface.set_alpha(255 - (self.death_frame_counter*5))
                self.red_surface.set_alpha(255 - (self.death_frame_counter*5))    
                self.black_surface.fill(BLACK)
                self.red_surface.fill(RED)
                screen.blit(self.black_surface, self.black_rect)
                screen.blit(self.red_surface, self.red_rect)
                self.death_frame_counter += 1
            else:
                self.death_frame_counter = 0
                self.alive = True
                self.move_to_abs_pos(self.spawn_coordinates[0], self.spawn_coordinates[1])

        
    def flag_as_hit(self, spawn_coordinates):
        self.alive = False
        self.spawn_coordinates = spawn_coordinates


    def move(self, keys, level):
        if not self.alive:
            return
        move_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        move_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        move_up = keys[pygame.K_w] or keys[pygame.K_UP]
        move_down = keys[pygame.K_s] or keys[pygame.K_DOWN]

        x_motion = move_left * (self.speed * -1) + move_right * self.speed
        y_motion = move_up * (self.speed * -1) + move_down * self.speed

        # move X axis
        self.red_rect.move_ip(x_motion, 0)
        self.black_rect.move_ip(x_motion, 0)
        #self.handle_x_axis_collision(level)

        # move Y axis
        self.red_rect.move_ip(0, y_motion)
        self.black_rect.move_ip(0, y_motion)
        #self.handle_y_axis_collision(level)

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


    def move_to_abs_pos(self, x, y):
        self.black_rect.centerx = x
        self.black_rect.centery = y
        self.red_rect.left = self.black_rect.x+self.gap/2
        self.red_rect.top = self.black_rect.y+self.gap/2

