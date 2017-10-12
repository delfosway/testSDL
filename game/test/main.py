import pygame
from pygame.locals import *
from sys import exit

import modelo.Character
import negocio.ItemManager
import negocio.GameManager

game_manager = None

def game_init():
    game_manager = negocio.GameManager.GameManager()

def main():
    pygame.init()
    game_init()

    item_manager = negocio.ItemManager.ItemManager()
    equip = modelo.Equipment.Equipment(None)
    equip.equip(item_manager.get_item(modelo.Equipment.ARMOR, 1))
    equip.equip(item_manager.get_item(modelo.Equipment.HELMET, 1))
    equip.equip(item_manager.get_item(modelo.Equipment.WEAPON, 1))
    ##print (equip.to_string())
    item_manager.list_all_items()

    screen = pygame.display.set_mode((800, 600), 0, 32)
    gris = (100, 100, 100)

    PLAYER_SPRITE = pygame.image.load("pythonright.png").convert_alpha()

    player = modelo.Character.Character(1, 1, PLAYER_SPRITE, 1, 100, 100)
    run_speed_multiplier = 1.25
    speed = 0.25

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
        player.move(movement_x,movement_y)
        screen.fill(gris)
        player.draw(screen)
        #screen.fill(gris)
        pygame.display.flip()

if __name__ == '__main__':
    main()
