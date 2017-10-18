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
import negocio.ItemManager

class Shop:

    def __init__(self):
        self.itemsOnSale = None

    def set_items_on_sale(self,lvl):
        self.itemsOnSale = [1,2]