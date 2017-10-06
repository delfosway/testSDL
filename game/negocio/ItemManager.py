# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto",
               "Matthew Wakefield"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

import modelo.Item


class ItemManager:

    def __init__(self):
        self.create_items()

    def create_items(self):

        self.items = []

        weapon_names = ["Espada de Hierro", "Espada de Acero", "Espada de Plata",
                        "Espada de Diamante", "Espada de Mitril", "Espada de Adamantita",
                        "Espada de Ebano", "Espada Bendita", "Cuchilla Profana", "Vincere ad Infinitum"]

        armor_names = ["Coraza de Hierro", "Coraza de Acero", "Coraza de Plata",
                       "Coraza de Diamante", "Coraza de Mitril", "Coraza de Adamantita",
                       "Coraza de Ebano", "Coraza Sagrada", "Armadura Demoniaca", "Praesidio ad Infinitum"]

        helmet_names = ["Casco de Hierro", "Casco de Acero", "Casco de Plata",
                        "Casco de Diamante", "Casco de Mitril", "Casco de Adamantita",
                        "Casco de Ebano", "Celada Angelical", "Yelmo Impio", "Dominus ad Infinitum"]

        self.items.extend([[], [], []])

        for n in range(0, modelo.Item.MAX_ITEM_LVL + 1):
            self.items[modelo.Equipment.WEAPON].append(
                modelo.Item.Item(weapon_names[n], n, 100 * (n * n), (n * n) + 3, 0, modelo.Equipment.WEAPON, None))
        for n in range(0, modelo.Item.MAX_ITEM_LVL + 1):
            self.items[modelo.Equipment.ARMOR].append(
                modelo.Item.Item(armor_names[n], n, 100 * (n * n), 0, n, modelo.Equipment.ARMOR, None))
        for n in range(0, modelo.Item.MAX_ITEM_LVL + 1):
            self.items[modelo.Equipment.HELMET].append(
                modelo.Item.Item(helmet_names[n], n, 100 * (n * n), 0, n, modelo.Equipment.HELMET, None))

    def get_item(self, type, lvl):
        if (lvl < 0 or lvl > modelo.Item.MAX_ITEM_LVL) or (type < 0 or type >= modelo.Equipment.EQUIPMENT_TYPE_COUNT):
            return None
        return self.items[type][lvl]

    def list_all_items(self):
        for i in range(0, modelo.Equipment.EQUIPMENT_TYPE_COUNT):
            for n in range(0, modelo.Item.MAX_ITEM_LVL + 1):
                print self.get_item(i, n).to_string()