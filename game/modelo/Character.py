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

class Character:

    BASE_AC_LVL_MULTIPLIER = 1
    BASE_DMG_LVL_MULTIPLIER = 2

    def __init__(self, x, y, sprite, lvl, max_hp, max_mp, equipment = None):
        self.x = x #map address
        self.y = y
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.sprite = sprite
        self.is_dead = False
        self.lvl = lvl
        if equipment == None:
            self.equipment = modelo.Equipment.Equipment(None)

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


