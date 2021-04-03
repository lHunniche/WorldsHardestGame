import pygame
import numpy as np
from soundfx import SoundFX


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
        self.enemies = []
        self.coins = []

    
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
            print("Height is {} - should be 19".format(len(self.layout)))
            return False
        for row in self.layout:
            if len(row) != 26:
                print("Width is {} - should be 26".format(len(row)))
                return False
        return True


    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()

    def check_collision_with_player(self, player):
        if not player.alive:
            return
        for enemy in self.enemies:
            if player.red_rect.colliderect(enemy.rect):
                player.flag_as_hit(self.spawn)
                SoundFX.player_hit.play()
                break

    def check_collision_with_coin(self, player):
        if not player.alive:
            return
        before = len(self.coins)
        self.coins[:] = [coin for coin in self.coins if not player.black_rect.colliderect(coin.rect)]
        after = len(self.coins)
        if before != after:
            SoundFX.point.play()



    def draw_level(self, screen):
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

        for coin in self.coins:
            pygame.draw.circle(screen, coin.outer_color, coin.rect.center, coin.outer_radius)
            pygame.draw.circle(screen, coin.inner_color, coin.rect.center, coin.inner_radius)


    def player_reached_goal(self, player):
        if len(self.coins) != 0:
            return
        for column in self.tile_array:
            for tile in column:
                if tile is not None and tile.type == END:
                    if player.black_rect.colliderect(tile.rect):
                        return True
        return False
                        

                


class LevelGen:

    @classmethod
    def load_levels(cls):
        from os import listdir
        levels = []
        for file in listdir("levels"):
            levels.append(LevelGen.load_level("levels/" + file))
        return levels


    @classmethod
    def load_level(cls, file):
        level_file = open(file, "r")
        lines = level_file.readlines()
        lines[:] = [line.rstrip('\n') for line in lines]
        level_layout = []
        

        # LOADING LAYOUT
        for i in range(0, 19): # the indices of the level layout
            row = list(lines[i])
            row[:] = [int(x) for x in row]
            level_layout.append(row)

        level = Level(level_layout)

        
        # LOADING SPAWN
        spawn_x = int(lines[20].split("=")[1].strip())
        spawn_y = int(lines[21].split("=")[1].strip())
        level.spawn = (spawn_x, spawn_y)


        # LOADING ENEMIES
        load_enemies = False
        enemies = []
        for line in lines:
            if line == "ENEMIES_START":
                load_enemies = True
                continue
            if line == "ENEMIES_STOP":
                break
            if load_enemies:
                enemy = (LevelGen.extract_enemy(line))
                if enemy is not None:
                    enemies.append(enemy)
        level.enemies = enemies


        # LOADING COINS
        load_coins = False
        coins = []
        for line in lines:
            if line == "COINS_START":
                load_coins = True
                continue
            if line == "COINS_STOP":
                break
            if load_coins:
                coins.append(LevelGen.extract_coin(line))
        level.coins = coins


        return level

    @classmethod
    def extract_enemy(cls, line):
        from enemy import Enemy
        if len(line) == 0:
            return None
        if (list(line)[0] == "#"):
            return None
        elements = [l.strip() for l in line.split(":")]
        paths = elements[:-1]
        speed = int(elements[-1])

        enemy_paths = []
        for path in paths:
            x = int(path.split(",")[0])
            y = int(path.split(",")[1])
            enemy_paths.append((x,y))
        return Enemy(enemy_paths, speed)

    
    @classmethod
    def extract_coin(cls, line):
        from coin import Coin
        x = int(line.split(",")[0])
        y = int(line.split(",")[1])
        return Coin(x, y)