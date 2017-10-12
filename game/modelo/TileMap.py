# coding=utf-8
__author__ = "Ignacio Oliveto"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ignacio Oliveto"
__email__ = "igoliveto@gmail.com"
__status__ = "Prototype"


class TileMap:

    MAP_WIDTH = 64
    MAP_HEIGHT = 64

    def __init__(self):
        self.tiles = [[0 for x in range(self.MAP_WIDTH)] for y in range(self.MAP_HEIGHT)]



