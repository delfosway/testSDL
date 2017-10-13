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



class TileMap:

    FLOOR_TILE_SPRITE_STRING = "floor.jpg"
    WALL_TILE_SPRITE_STRING = "wall.png"

    MAP_WIDTH = 64 #Tiles
    MAP_HEIGHT = 64 #Tiles

    TILE_WIDTH = 32 #Pixels
    TILE_HEIGHT = 32 #Pixels

    floor_tile = None
    wall_tile = None



    def __init__(self):
        self.tiles = [[None for x in range(self.MAP_WIDTH)] for y in range(self.MAP_HEIGHT)]
        self.load_default_tiles()

    def load_from_grid(self, grid):

        if self.is_grid_size_valid(grid):
            for x in range(self.MAP_WIDTH):
                for y in range (self.MAP_HEIGHT):
                    tile_to_set = self.tile_from_grid_value(grid[x][y])
                    #tile_to_set.x = x
                    #tile_to_set.y = y
                    self.set_tile(x, y, tile_to_set)
        else:
            raise NameError("Grid out of Boundaries.")

    def draw(self, camera):
        for x in range(self.MAP_WIDTH):
            for y in range(self.MAP_HEIGHT):
                tile = self.tiles[x][y]
                camera.draw_sprite(tile.sprite, x * self.TILE_WIDTH, y * self.TILE_HEIGHT)

    def tile_from_grid_value(self, value):
        if value == 0:
            return self.floor_tile
        elif value == 1:
            return self.wall_tile
        else:
            raise NameError ("Grid value " + str(value) + " is Invalid!")

    def set_tile(self, x, y, tile):
        if x < 0 or x >= self.MAP_WIDTH or y < 0 or y >= self.MAP_HEIGHT:
            raise NameError("X or Y is out of map boundaries! X = " + str(x) + ", Y = " + str(y))
        else:
            tile.x = x
            tile.y = y
            self.tiles[x][y] = tile

    def is_grid_size_valid(self, grid):
        if len(grid) > self.MAP_WIDTH:
            return False
        else:
            if len(grid[0]) > self.MAP_HEIGHT:
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

