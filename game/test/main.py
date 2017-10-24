import pygame
from pygame.locals import *
from sys import exit

import modelo.Character
import negocio.ItemManager
import negocio.GameManager
import modelo.TileMap
import negocio.Camera
import util.DungeonGenerator
import util.Graphics
import util.Util
import util.Vector
import negocio.CharacterManager

game_manager = None

def game_init():
    global game_manager
    game_manager = negocio.GameManager.GameManager()

def create_test_grid():
    test_grid = [[0 for x in range(modelo.TileMap.TileMap.MAP_WIDTH)] for y in range(modelo.TileMap.TileMap.MAP_HEIGHT)]

    for x in range(modelo.TileMap.TileMap.MAP_WIDTH):
        for y in range(modelo.TileMap.TileMap.MAP_HEIGHT):
            if x == 0 or y == 0 or x == modelo.TileMap.TileMap.MAP_WIDTH - 1 or y == modelo.TileMap.TileMap.MAP_HEIGHT - 1:
                test_grid[x][y] = 1
            if x % 3 == 0 and y % 3 == 0:
                test_grid[x][y] = 1
    return test_grid

def main():
    pygame.init()
    game_init()
    game_manager.start()





if __name__ == '__main__':
    main()
