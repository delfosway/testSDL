# coding=utf-8
__author__ = "Ignacio Oliveto"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ignacio Oliveto"
__email__ = "igoliveto@gmail.com"
__status__ = "Prototype"

import modelo.Tile
import pygame
from  random import  randint
import copy

class TileMap:

    FLOOR_TILE_SPRITE_STRING = "Graficos/wood.png"
    WALL_TILE_SPRITE_STRING = "Graficos/wall.png"

    MAP_WIDTH = 64 #Tiles
    MAP_HEIGHT = 64 #Tiles

    floor_tile = None
    wall_tile = None

    TILE_FLOOR = 0
    TILE_WALL = 1


    def __init__(self):
        self.tiles = [[None for x in range(self.MAP_WIDTH)] for y in range(self.MAP_HEIGHT)]
        self.walls = []
        self.characters = []
        self.bullets = []
        self.load_default_tiles()

    def update(self):



        # Primero actualizamos los Characters:
        for character in self.characters:
            character.update()

        # Luego actualizamos los Bullets

        #Primero chequeamos los que esten "muertos" y los sacamos de la lista.

        #self.bullets[:]  = [bul for bul in self.bullets if bul.is_alive()]

        for bullet in self.bullets[:]:
            if bullet.is_dead():
                self.bullets.remove(bullet)
            else:
                bullet.update()



    def draw(self, camera):
        #Primero dibujamos los tiles.

                #print ("Dibujando Tile : [" + str(x) + "," + str(y) + "]")
        #camera.draw_drawable(tile)
        camera.draw_map(self)

        #Luego dibujamos los Characters
        for character in self.characters:
            camera.draw_drawable(character)

        #Y por ultimo los Bullets.
        for bullet in self.bullets:
            camera.draw_drawable(bullet)

    def get_map_graphic_width(self):
        return self.MAP_WIDTH * modelo.Tile.Tile.TILE_WIDTH , self.MAP_HEIGHT * modelo.Tile.Tile.TILE_HEIGHT

    def get_random_walkable_tile(self):
        try_count = 0
        while try_count < 2000:
            found_tile = self.tiles[randint(0, self.MAP_WIDTH - 1)][randint(0, self.MAP_HEIGHT - 1)]
            if found_tile is not None:
                if found_tile.is_walkable():
                    print ("Walkable Tile Found : [" + str(found_tile.x) + "," + str(found_tile.y) + "]")
                    return found_tile
            try_count += 1
        raise NameError("Couldn't find a Walkable Tile!")


    def spawn_character_at_random_walkable(self, character):
        walkable_tile = self.get_random_walkable_tile()
        self.spawn_character_at_tile(character, walkable_tile)

    def spawn_character_at_tile(self, character, tile):
        self.spawn_character_at_pos(character, tile.x, tile.y)

    def spawn_character_at_pos(self, character, x, y):
        self.characters.append(character)
        character.spawn(self, x, y)

    def spawn_bullet(self, bullet):
        self.bullets.append(bullet)

    def load_from_grid(self, grid):
        self.print_grid(grid)
        if self.is_grid_size_valid(grid):
            self.walls = []
            for x in range(self.MAP_WIDTH):
                for y in range (self.MAP_HEIGHT):
                    #print("TILEMAP : Setting Tile : [" + str(x) + "," + str(y) + "]")
                    tile_to_set = self.tile_from_grid_value(grid[x][y]).copy()
                    #tile_to_set.x = x
                    #tile_to_set.y = y
                    self.set_tile(x, y, tile_to_set)
        else:
            raise NameError("Grid out of Boundaries.")

    def set_tile(self, x, y, tile):
        if self.is_index_out_of_bounds(x, y):
            raise NameError("X or Y is out of map boundaries! X = " + str(x) + ", Y = " + str(y))
        else:
            tile.set_position(x, y)
            self.tiles[x][y] = tile
            if not tile.is_walkable():
                self.walls.append(tile)

    def is_index_out_of_bounds(self, x, y):
        return x < 0 or x >= self.MAP_WIDTH or y < 0 or y >= self.MAP_HEIGHT

    #TESTING
    def print_grid(self, grid):
        print ("Grid Size : [" + str(str(len(grid)) + "," + str(len(grid[0])) + "]"))
        for x in range(32):
            for y in range(32):
                print(str(grid[x][y]) + " ", end="")
            print ("\n")

    def tile_from_grid_value(self, value):
        if value == self.TILE_FLOOR:
            return self.floor_tile
        elif value == self.TILE_WALL:
            return self.wall_tile
        else:
            raise NameError ("Grid value " + str(value) + " is Invalid!")

    def is_grid_size_valid(self, grid):
        if len(grid) != self.MAP_WIDTH:
            return False
        else:
            if len(grid[0]) != self.MAP_HEIGHT:
                return False

        return True


    def load_default_tiles(self):
        self.load_floor_tile()
        self.load_wall_tile()


    def load_floor_tile(self):
        if self.floor_tile is None:
            self.floor_tile = modelo.Tile.Tile(True, pygame.image.load(self.FLOOR_TILE_SPRITE_STRING).convert_alpha(), 0, 0, None)

    def load_wall_tile(self):
        if self.wall_tile is None:
            self.wall_tile = modelo.Tile.Tile(False, pygame.image.load(self.WALL_TILE_SPRITE_STRING).convert_alpha(), 0, 0, None)

