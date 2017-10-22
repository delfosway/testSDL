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

    tuto = True
    tutorial(tuto, camera)

    menu = True
    main_menu(menu, camera)

    PLAYER_SPRITE = pygame.image.load("Graficos/archon.png").convert_alpha()

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

    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)

    bgmchannel = pygame.mixer.find_channel(0)
    bgmchannel.queue(pygame.mixer.Sound("SFX/bgmusic.ogg"))

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
                    channel = pygame.mixer.find_channel(1)
                    if not channel.get_busy():
                        channel.queue(pygame.mixer.Sound("SFX/shoot2.ogg"))
                    else:
                        channel2 = pygame.mixer.find_channel(2)
                        channel2.queue(pygame.mixer.Sound("SFX/shoot2.ogg"))
                    #print("Mouse Vector : " + util.Util.position_to_string(x,y) + " - Angle : " + util.Util.position_to_string(mouse_vector.x, mouse_vector.y))
                    player.shoot(mouse_vector.x * 10, mouse_vector.y * 10)
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    pause(paused, camera)

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

def main_menu(state, camera):
    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = False

        camera.fill_menu()
        menu_text = pygame.font.Font('arial.ttf', 50)
        text_surface, text_rect = text_draw("Welcome to the main menu", menu_text)
        text_rect = 80, 100
        camera.screen.blit(text_surface, text_rect)

        menu_text2 = pygame.font.Font('arial.ttf', 35)
        text_surface2, text_rect2 = text_draw("Press enter to start the game", menu_text2)
        text_rect2 = 160, 400
        camera.screen.blit(text_surface2, text_rect2)
        pygame.display.update()


def tutorial(state, camera):
    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = False

        camera.fill_menu()
        menu_text = pygame.font.Font('arial.ttf', 115)
        text_surface, text_rect = text_draw("How to play", menu_text)
        text_rect = 100, 25
        camera.screen.blit(text_surface, text_rect)

        menu_text2 = pygame.font.Font('arial.ttf', 30)
        text_surface2, text_rect2 = text_draw("Movement: w, a, s, d", menu_text2)
        text_rect2 = 220, 200
        camera.screen.blit(text_surface2, text_rect2)

        text_surface3, text_rect3 = text_draw("You aim with the mouse", menu_text2)
        text_rect3 = 220, 300
        camera.screen.blit(text_surface3, text_rect3)

        text_surface4, text_rect4 = text_draw("Shoot: [spacebar]", menu_text2)
        text_rect4 = 220, 400
        camera.screen.blit(text_surface4, text_rect4)

        text_surface5, text_rect5 = text_draw("Press enter to continue", menu_text2)
        text_rect5 = 200, 500
        camera.screen.blit(text_surface5, text_rect5)
        pygame.display.update()

def text_draw(text, font):
    text_surface = font.render(text, True, util.Graphics.BLACK)
    return text_surface, text_surface.get_rect()

def pause(paused, camera):
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        menu_text = pygame.font.Font('arial.ttf', 115)
        text_surface, text_rect = text_draw("Paused", menu_text)
        text_rect = 200, 150
        camera.screen.blit(text_surface, text_rect)

        pygame.display.update()

if __name__ == '__main__':
    main()
