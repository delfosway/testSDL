# coding=utf-8
__author__ = "Gonzalo Montaña"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Gonzalo Montaña"
__email__ = "gonza_257@gmail.com"
__status__ = "Prototype"

import modelo.Equipment
import pygame

class Character:

    BASE_AC_LVL_MULTIPLIER = 1
    BASE_DMG_LVL_MULTIPLIER = 2

    CHARACTER_SPRITE_WIDTH = 32
    CHARACTER_SPRITE_HEIGHT = 32

    def __init__(self, x, y, sprite, lvl, max_hp, max_mp, equipment = None):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.sprite = sprite
        self.is_dead = False
        self.lvl = lvl
        self.current_map = None
        if equipment == None:
            self.equipment = modelo.Equipment.Equipment(None)

    def spawn(self, map, x, y):
        self.current_map = map
        self.x = x
        self.y = y


    def base_ac(self):
        return self.lvl * self.BASE_AC_LVL_MULTIPLIER

    def base_dmg(self):
        return self.lvl * self.BASE_DMG_LVL_MULTIPLIER

    def total_ac(self):
        return self.equipment.total_ac() + self.base_ac()

    def receive_damage (self, damage_amount):
        hp_to_substract = damage_amount - self.total_ac()
        if hp_to_substract <= 0:
            hp_to_substract = 1

        self.substract_hp(hp_to_substract)


    def heal (self, heal_amount):
        self.add_hp(heal_amount)

    def add_hp(self, hp_to_add):
        self.hp += hp_to_add
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def subtract_hp(self, hp_to_substract):
        self.hp -= hp_to_substract
        if self.hp <= 0:
            self.is_dead = True

    def add_mp(self, mp_to_add):
        self.mp += mp_to_add
        if self.mp > self.max_mp:
            self.mp = self.max_mp

    def subtract_mp(self, mp_to_substract):
        self.mp -= mp_to_substract
        if self.mp <= 0:
            self.mp = 0

    def draw(self, camera):
        camera.draw_drawable(self)

    def move(self, x, y):
        if (x != 0 or y != 0):
            old_x = self.x
            old_y = self.y
            self.x += x
            self.y += y
            if self.is_colliding():
                print ("Colliding!")
                self.x = old_x
                self.y = old_y


    def is_colliding(self):
        walls = self.current_map.walls
        rect = pygame.Rect(self.x, self.y, self.CHARACTER_SPRITE_WIDTH, self.CHARACTER_SPRITE_HEIGHT)
        for wall in walls:
            if rect.colliderect(wall):
                return True
        return False

    def move_ai(self, px, py, ex, ey): #px py = player coordinates, ex ey = enemy coordinates
        self.px = px
        self.py = py
        self.ex = ex
        self.ey = ey


