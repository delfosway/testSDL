import pygame
from pygame.locals import *
from sys import exit

import modelo.Character
import negocio.ItemManager
import negocio.GameManager
import modelo.TileMap
import negocio.Camera

game_manager = None
item_manager = None

def game_init():
    global game_manager
    game_manager = negocio.GameManager.GameManager()

def main():
    pygame.init()
    game_init()
    camera = negocio.Camera.Camera(800,600)

    PLAYER_SPRITE = pygame.image.load("pythonright.png").convert_alpha()

    #equip = modelo.Equipment.Equipment(None)
    #equip.equip(item_manager.get_item(modelo.Equipment.ARMOR, 1))
    #equip.equip(item_manager.get_item(modelo.Equipment.HELMET, 1))
    #equip.equip(item_manager.get_item(modelo.Equipment.WEAPON, 1))
    ##print (equip.to_string())
    game_manager.item_manager.list_all_items()

    test_grid = [[0 for x in range(modelo.TileMap.TileMap.MAP_WIDTH)] for y in range(modelo.TileMap.TileMap.MAP_HEIGHT)]

    for x in range(modelo.TileMap.TileMap.MAP_WIDTH):
        for y in range(modelo.TileMap.TileMap.MAP_HEIGHT):
            if (x == 0 or y == 0 or x == modelo.TileMap.TileMap.MAP_WIDTH -1 or y == modelo.TileMap.TileMap.MAP_HEIGHT - 1):
                test_grid[x][y] = 1
            if (x % 3 == 0 and y % 3 == 0):
                test_grid[x][y] = 1


    tileMap = modelo.TileMap.TileMap()
    tileMap.load_from_grid(test_grid)

    player = modelo.Character.Character(1, 1, PLAYER_SPRITE, 1, 100, 100)
    run_speed_multiplier = 1.25
    speed = 1

    camera.attach_to_drawable(player)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        movement_x = 0
        movement_y = 0

        #Walks
        pressed = pygame.key.get_pressed()
        if pressed[K_w]:
            movement_y += -speed
        if pressed[K_s]:
            movement_y += speed
        if pressed[K_a]:
            movement_x += -speed
        if pressed[K_d]:
            movement_x += speed

        #Runs
        if pressed[K_w] and pressed[K_LSHIFT]:
            movement_y += -speed * run_speed_multiplier
        if pressed[K_s] and pressed[K_LSHIFT]:
            movement_y += speed * run_speed_multiplier
        if pressed[K_a] and pressed[K_LSHIFT]:
            movement_x += -speed * run_speed_multiplier
        if pressed[K_d] and pressed[K_LSHIFT]:
            movement_x += speed * run_speed_multiplier

        #modelo.Character.Character.move(player, movement_x, movement_y)
        player.move(movement_x, movement_y)


        camera.update()
        camera.fill_background()
        tileMap.draw(camera)
        camera.draw_drawable(player)
        #tileMap.draw(camera)
        #player.draw(camera)



        #screen.fill(gris)
        pygame.display.flip()

if __name__ == '__main__':
    main()
