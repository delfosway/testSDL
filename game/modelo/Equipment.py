# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

import modelo.Item

EQUIPMENT_TYPE_COUNT = 3

WEAPON, ARMOR, HELMET = range(EQUIPMENT_TYPE_COUNT)
item_type_strings = ["Weapon", "Armor", "Helmet"]


class Equipment:

    def __init__(self, character):
        self.character = character
        self.items = [None, None, None]

    def equip(self,item):
        self.items[item.item_type] = item

    def total_ac(self):
        total_ac = 0
        for item in self.items:
            if item is not None:
                total_ac += item.ac
        return total_ac

    def total_dmg(self):
        total_dmg = 0
        for item in self.items:
            if item is not None:
                total_dmg += item.dmg
        return total_dmg

    def set_armor(self, item):
        self.items[ARMOR] = item

    def set_helmet(self, item):
        self.items[HELMET] = item

    def set_weapon(self, item):
        self.items[WEAPON] = item

    def to_string (self):
        result = "Equipo : \n"
        for item in self.items:
            if item is not None:
                result += "    " + item.to_string() + "\n"
        return result





