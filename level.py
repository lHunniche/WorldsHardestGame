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

WT = WALL_THICKNESS = 7
WB = WT//2
WBB = WB*2


class Tile:
    def __init__(self, rect, color, type):
        self.rect = rect
        self.color = color
        self.type = type
        self.wall_up = False
        self.wall_down = False
        self.wall_left = False
        self.wall_right = False

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
        self.enemies = None

    def set_enemies(self, enemies):
        self.enemies = enemies
        return self

    
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

        self.mark_where_walls_draw()

    

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


    def mark_where_walls_draw(self):
        for y_pos in range(self.tiles_height):
            for x_pos in range(self.tiles_width):
                tile = self.tile_array[y_pos][x_pos]
                if tile is not None and tile.type == WALL:
                    above = (y_pos-1, x_pos)
                    above = self.tile_array[above[0]][above[1]]
                    below = (y_pos+1, x_pos)
                    below = self.tile_array[below[0]][below[1]]
                    left = (y_pos, x_pos-1)
                    left = self.tile_array[left[0]][left[1]]
                    right = (y_pos, x_pos+1)
                    right = self.tile_array[right[0]][right[1]]

                    tile.wall_up = above is not None and above.type != WALL
                    tile.wall_down = below is not None and below.type != WALL
                    tile.wall_left = left is not None and left.type != WALL
                    tile.wall_right = right is not None and right.type != WALL


    def is_valid_layout(self):
        if len(self.layout) != 19:
            return False
        for row in self.layout:
            if len(row) != 26:
                return False
        return True


    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()

    def check_collision_with_player(self, player):
        '''
        small buffer added below... maybe reconsider implementation later?
        '''
        player_collide_rect = player.red_rect.copy()
        player_collide_rect.width = player.red_rect.width + 5
        player_collide_rect.height = player.red_rect.height + 5
        player_collide_rect.center = player.red_rect.center

        for enemy in self.enemies:
            if player_collide_rect.colliderect(enemy.rect):
                player.move_to_abs_pos(self.spawn[0], self.spawn[1])
                break



    def draw(self, screen):
        for column in self.tile_array:
            for tile in column:
                if tile is not None and tile.type == WALL:
                    rect = tile.rect
                    if tile.wall_up:
                        pygame.draw.line(screen, FLOOR_WALL, (rect.left-WBB, rect.top+WB), (rect.right+WBB, rect.top+WB), WT)
                    if tile.wall_down:
                        pygame.draw.line(screen, FLOOR_WALL, (rect.left-WBB, rect.bottom-WB), (rect.right+WBB, rect.bottom-WB), WT)
                    if tile.wall_left:
                        pygame.draw.line(screen, FLOOR_WALL, (rect.left+WB, rect.top-WBB), (rect.left+WB, rect.bottom+WBB), WT)
                    if tile.wall_right:
                        pygame.draw.line(screen, FLOOR_WALL, (rect.right-WB, rect.top-WBB), (rect.right-WB, rect.bottom+WBB), WT)
                        
        for column in self.tile_array:
            for tile in column:
                if tile is not None:
                    if tile.type != WALL:
                        pygame.draw.rect(screen, tile.color, tile.rect)

        for enemy in self.enemies:
            pygame.draw.circle(screen, enemy.outer_color, enemy.rect.center, enemy.outer_radius)
            pygame.draw.circle(screen, enemy.inner_color, enemy.rect.center, enemy.inner_radius)
            #pygame.draw.rect(screen, enemy.outer_color, enemy.rect)
                        

                



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



