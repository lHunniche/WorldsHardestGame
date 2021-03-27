import pygame
import numpy as np


_ = NOTHING = 0
W = WALL = 1
S = START = 2
E = END = 3
F = FLOOR = 4
P = SPAWN = 5

FLOOR_BLUE = (216, 207, 252)
FLOOR_WHITE = (255, 255, 255)
FLOOR_START = (149, 245, 132)
FLOOR_END = (149, 245, 132)
FLOOR_WALL = (0, 0, 0)
TILE_SIZE = 50
WB = WALL_BUFFER = 2

WALL_THICKNESS = 6


class Tile:
    def __init__(self, rect, color, type):
        self.rect = rect
        self.color = color
        self.type = type
        self.wall_up = False
        self.wall_down = False
        self.wall_left = False
        self.wall_right = False
        self.has_walls = False

    def __repr__(self):
        return str(self.type)







class Level:
    def __init__(self, layout):
        self.layout = layout # 26 x 19 array
        self.tiles_height = 19
        self.tiles_width = 26
        self.left = 50
        self.top = 50
        self.tile_size = TILE_SIZE
        self.tile_array = []
        self.spawn = (0, 0)

        self.make_rect_array()
    
    def make_rect_array(self):
        if not self.is_valid_layout():
            print("Invalid layout")
        self.tile_array = [None] * self.tiles_height
        for counter in range(self.tiles_height):
            self.tile_array[counter] = [None] * self.tiles_width


        for y_pos in range(self.tiles_height):
            for x_pos in range(self.tiles_width):
                if self.layout[y_pos][x_pos] is not NOTHING:
                    self.tile_array[y_pos][x_pos] = self.create_tile(self.layout[y_pos][x_pos], y_pos, x_pos)

        self.flag_walls()
        


    def create_tile(self, tile_type, y_pos, x_pos):
        # Rect(left, top, width, height)
        left = self.left + self.tile_size * x_pos
        top = self.top + self.tile_size * y_pos
        width = self.tile_size
        height = self.tile_size
        
        if tile_type == WALL:
            rect = pygame.Rect(left, top, width, height)
            color = FLOOR_WALL
            return Tile(rect, color, tile_type)


        elif tile_type == FLOOR:
            floor_rect = pygame.Rect(left, top, width, height)
            color = None
            if y_pos % 2 == 0: #if we are on even row, make even column white, odd column blue
                if x_pos % 2 == 0:
                    color = FLOOR_WHITE
                else:
                    color = FLOOR_BLUE
            else: #if we are on uneven row, make even column blue, odd column white
                if x_pos % 2 == 0:
                    color = FLOOR_BLUE
                else:
                    color = FLOOR_WHITE
            return Tile(floor_rect, color, tile_type)


        elif tile_type == START or tile_type == SPAWN:
            rect = pygame.Rect(left, top, width, height)
            color = FLOOR_START
            if tile_type == SPAWN:
                self.spawn = (left, top)
            return Tile(rect, color, tile_type)


        elif tile_type == END:
            rect = pygame.Rect(left, top, width, height)
            color = FLOOR_END
            return Tile(rect, color, tile_type)
    

    def is_valid_layout(self):
        if len(self.layout) != 19:
            return False
        for row in self.layout:
            if len(row) != 26:
                return False
        return True


    def flag_walls(self):
        for y_pos in range(self.tiles_height):
            for x_pos in range(self.tiles_width):
                if self.tile_array[y_pos][x_pos] is not None: #and self.tile_array[y_pos][x_pos] != WALL:
                    up = (y_pos-1, x_pos)
                    down = (y_pos+1, x_pos)
                    left = (y_pos, x_pos-1)
                    right = (y_pos, x_pos+1)
                    current_tile = self.tile_array[y_pos][x_pos]
                    if self.tile_array[left[0]][left[1]] is None:
                        current_tile.has_walls = True
                        current_tile.wall_left = True
                    if self.tile_array[right[0]][right[1]] is None:
                        current_tile.has_walls = True
                        current_tile.wall_right = True
                    if self.tile_array[up[0]][up[1]] is None:
                        current_tile.has_walls = True
                        current_tile.wall_up = True
                    if self.tile_array[down[0]][down[1]] is None:
                        current_tile.has_walls = True
                        current_tile.wall_down = True



    def draw(self, screen):
        for column in self.tile_array:
            for tile in column:
                if tile is not None:
                    pygame.draw.rect(screen, tile.color, tile.rect)
        for column in self.tile_array:
            for tile in column:
                if tile is not None:
                    x = tile.rect.x 
                    y = tile.rect.y
                    tl = tile.rect.topleft
                    tr = tile.rect.topright
                    bl = tile.rect.bottomleft
                    br = tile.rect.bottomright
                    if tile.wall_up:
                        pygame.draw.line(screen, FLOOR_WALL, tl, tr, WALL_THICKNESS)
                    if tile.wall_down:
                        pygame.draw.line(screen, FLOOR_WALL, bl, br, WALL_THICKNESS)
                    if tile.wall_left:
                        pygame.draw.line(screen, FLOOR_WALL, tl, bl, WALL_THICKNESS)
                    if tile.wall_right:
                        pygame.draw.line(screen, FLOOR_WALL, tr, br, WALL_THICKNESS)

                    



class LevelGen:

    @classmethod
    def level_1(cls):
        return [
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, S, S, S, S, _, _, _, _, _, _,     _, _, _, _, F, F, E, E, E, E, _, _, _],
            [_, _, _, S, P, S, S, _, F, F, F, F, F,     F, F, F, F, F, _, E, E, E, E, _, _, _],
            [_, _, _, S, S, S, S, _, F, F, F, F, F,     F, F, F, F, F, _, E, E, E, E, _, _, _],

            [_, _, _, S, S, S, S, _, F, F, F, F, F,     F, F, F, F, F, _, E, E, E, E, _, _, _],
            [_, _, _, S, S, S, S, _, F, F, F, F, F,     F, F, F, F, F, _, E, E, E, E, _, _, _],
            [_, _, _, S, S, S, S, F, F, _, _, _, _,     _, _, _, _, _, _, E, E, E, E, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _, _, _, _, _,     _, _, _, _, _, _, _, _, _, _, _, _, _],
        ]

    @classmethod
    def all_floor(cls):
        return [
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
            [F, F, F, F, F, F, F, F, F, F, F, F, F,     F, F, F, F, F, F, F, F, F, F, F, F, F],
        ]



