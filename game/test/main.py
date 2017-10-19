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

game_manager = None
item_manager = None

FPS = 60

clock = pygame.time.Clock()

def game_init():
    global game_manager
    game_manager = negocio.GameManager.GameManager()

def create_test_grid():
    test_grid = [[0 for x in range(modelo.TileMap.TileMap.MAP_WIDTH)] for y in range(modelo.TileMap.TileMap.MAP_HEIGHT)]

    for x in range(modelo.TileMap.TileMap.MAP_WIDTH):
        for y in range(modelo.TileMap.TileMap.MAP_HEIGHT):
            if (x == 0 or y == 0 or x == modelo.TileMap.TileMap.MAP_WIDTH - 1 or y == modelo.TileMap.TileMap.MAP_HEIGHT - 1):
                test_grid[x][y] = 1
            if (x % 3 == 0 and y % 3 == 0):
                test_grid[x][y] = 1
    return test_grid

def main():
    pygame.init()
    game_init()
    camera = negocio.Camera.Camera(800,600)

    PLAYER_SPRITE = pygame.image.load("Graficos/Bicho.png").convert_alpha()

    characters = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    game_manager.item_manager.list_all_items()

    #test_grid = create_test_grid()
    test_grid = util.DungeonGenerator.crearHabitaciones(modelo.TileMap.TileMap.MAP_WIDTH, modelo.TileMap.TileMap.MAP_HEIGHT)
    tileMap = modelo.TileMap.TileMap()
    tileMap.load_from_grid(test_grid)


    player = modelo.Character.Character(PLAYER_SPRITE, 1, 300, 300)
    
    tileMap.spawn_character_at_random_walkable(player)
    #player.spawn(tileMap, 330, 330)

    run_speed_multiplier = 1.5
    speed = 3

    camera.attach_to_drawable(player)
    running = True
    while running:
        clock.tick(FPS)



        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    x, y = camera.get_mouse_map_position()
                    #print("Mouse Position : " + util.Util.position_to_string(x, y))
                    mouse_vector = util.Vector.Vector(x - player.rect.x, y - player.rect.y)
                    mouse_vector.normalizar()
                    #print("Mouse Vector : " + util.Util.position_to_string(x,y) + " - Angle : " + util.Util.position_to_string(mouse_vector.x, mouse_vector.y))
                    player.shoot(mouse_vector.x * 10, mouse_vector.y * 10)

        movement_x = 0
        movement_y = 0

        #Calculo desplazamiento a partir de las teclas presionadas.
        pressed = pygame.key.get_pressed()
        if pressed[K_w]:
            movement_y += -speed
        if pressed[K_s]:
            movement_y += speed
        if pressed[K_a]:
            movement_x += -speed
        if pressed[K_d]:
            movement_x += speed


        #Incremento la velocidad si esta corriendo:
        if pressed[K_LSHIFT]:
            movement_x = movement_x * run_speed_multiplier
            movement_y = movement_y * run_speed_multiplier

        player.set_speed(movement_x, movement_y)
        #print ("player Position : " + util.Util.position_to_string(player.rect.x, player.rect.y))
        #UPDATE :
        tileMap.update()
        camera.update()
        #DRAW:
        camera.fill_background()
        tileMap.draw(camera)
        #camera.draw_drawable(player)
        pygame.display.flip()

        #Chequeamos si el player sigue vivo.
        #En caso contrario, salimos del Main Loop.
        if player.is_dead:
            running = False

if __name__ == '__main__':
    main()
