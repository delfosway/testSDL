import pygame
from pygame.locals import *
from sys import exit

import modelo.Character

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600), 0, 32)
    gris = (100, 100, 100)

    PLAYER_SPRITE = pygame.image.load("pythonright.png").convert_alpha()

    player = modelo.Character.Character(1, 1, PLAYER_SPRITE)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        movement_x = 0
        movement_y = 0
        speed = 0.04
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
            movement_y += -speed * 1.75
        if pressed[K_s] and pressed[K_LSHIFT]:
            movement_y += speed * 1.75
        if pressed[K_a] and pressed[K_LSHIFT]:
            movement_x += -speed * 1.75
        if pressed[K_d] and pressed[K_LSHIFT]:
            movement_x += speed * 1.75

        modelo.Character.Character.move(player, movement_x, movement_y)

        screen.fill(gris)
        modelo.Character.Character.draw(player, screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
