# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

import modelo.Equipment

MAX_ITEM_LVL = 9

class Item:
    def __init__(self, name, lvl, price, dmg, ac, item_type, sprite):
        self.name = name
        self.sprite = sprite
        self.item_type = item_type
        self.price = price
        self.lvl = lvl
        self.dmg = dmg
        self.ac = ac

    @staticmethod
    def item_type_to_string(item_type):
        if item_type >= modelo.Equipment.EQUIPMENT_TYPE_COUNT or item_type < 0:
            return "ITEM_TYPE_ERROR (" + item_type + ")"
        else:
            return modelo.Equipment.item_type_strings[item_type]

    def to_string(self):
        return self.name + " - " + self.item_type_to_string(self.item_type) \
               + " - Lvl : " + str(self.lvl) + " - DMG : " + str(self.dmg) + " - AC : " + str(self.ac) \
               + " - Price : " + str(self.price)

