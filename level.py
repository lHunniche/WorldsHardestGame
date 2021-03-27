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


class Tile:
    def __init__(self, rect, color, type):
        self.rect = rect
        self.color = color
        self.type = type

    def __repr__(self):
        return str(self.type)


class Level:
    def __init__(self, layout):
        self.layout = layout # 26 x 19 array
        self.tiles_height = 19
        self.tiles_width = 26
        self.left = 50
        self.top = 50
        self.tile_size = 50
        self.tile_array = []
        self.spawn = (0, 0)

        self.make_rect_array()
    
    def make_rect_array(self):
        if not self.is_valid_layout():
            print("Invalid layout")
        self.tile_array = [None] * self.tiles_height
        for counter in range(self.tiles_height):
            self.tile_array[counter] = [None] * self.tiles_width

        self.generate_walls()

        for y_pos in range(self.tiles_height):
            for x_pos in range(self.tiles_width):
                if self.layout[y_pos][x_pos] is not NOTHING:
                    self.tile_array[y_pos][x_pos] = self.create_tile(self.layout[y_pos][x_pos], y_pos, x_pos)

        


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


    def generate_walls(self):
        for y_pos in range(self.tiles_height):
            for x_pos in range(self.tiles_width):
                if self.layout[y_pos][x_pos] != NOTHING and self.layout[y_pos][x_pos] != WALL:
                    neighbors = [(y_pos-1, x_pos), (y_pos+1, x_pos), (y_pos, x_pos-1), (y_pos, x_pos+1)]
                    for indices in neighbors:
                        if indices[0] < 0 or indices[1] < 0 or indices[0] >= self.tiles_height or indices[1] >= self.tiles_width: # only look within boundaries
                            continue
                        if self.layout[indices[0]][indices[1]] == NOTHING: # find tile that is None
                            self.layout[indices[0]][indices[1]] = WALL # make it a wall


    def draw(self, screen):
        #print(np.matrix(self.tile_array))
        for column in self.tile_array:
            for tile in column:
                if tile is not None:
                    pygame.draw.rect(screen, tile.color, tile.rect)



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



