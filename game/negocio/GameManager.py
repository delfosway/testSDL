# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

import negocio.ItemManager

class GameManager:
    def __init__(self):
        self.current_player = None
        self.current_lvl = 0
        self.current_gold = 0
        self.total_gold = 0
        self.item_manager = negocio.ItemManager.ItemManager()

    def set_current_player(self,character):
        self.current_player = character

    def add_gold(self, gold_amount):
        self.current_gold += gold_amount
        self.total_gold += gold_amount

    def subtract_gold(self, gold_amount):
        self.current_gold -= gold_amount

    def can_afford(self, price):
        return self.current_gold >= price

