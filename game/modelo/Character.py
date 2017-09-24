import pygame
from pygame.locals import *
from sys import exit
import math

class Character:
    def __init__(self, x, y, sprite):
        self.x = x #map address
        self.y = y
        self.sprite = sprite

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def move(self, x, y):
        self.x += x
        self.y += y

    def move_ai(self, px, py, ex, ey): #px py = player coordinates, ex ey = enemy coordinates
        self.px = px
        self.py = py
        self.ex = ex
        self.ey = ey


