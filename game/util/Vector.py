# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

import math

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalizar(self):
        mag = self.magnitud()
        if mag != 0:
            self.x = self.x / mag
            self.y = self.y / mag
        else:
            self.x = 0
            self.y = 0

    def magnitud(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

