# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

import pygame
import math

class Camera:

    gray = (0, 0, 0)

    def __init__(self, camera_width, camera_height):
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.screen = pygame.display.set_mode((camera_width, camera_height), 0, 32)
        self.offset_x = 0
        self.offset_y = 0
        self.attached_drawable = None
        self.player_pos_x=0
        self.player_pos_y=0

    def attach_to_drawable(self, drawable):
        self.attached_drawable = drawable
        self.update()

    def update(self):
        if self.attached_drawable is not None:
           self.offset_x = self.attached_drawable.x
           self.offset_y = self.attached_drawable.y

    def fill_background(self):
        self.screen.fill(self.gray)

    def total_x_offset(self):
        return self.offset_x - (self.camera_width / 2)

    def total_y_offset(self):
        return self.offset_y - (self.camera_height / 2)

    def draw_sprite(self,sprite, x, y):
        #print ("Draw pos : [" + str(x) + "," + str(y) + "] - Camera Offset : [" + str(self.offset_x) + "," + str(self.offset_y) + "]")
        #self.screen.blit(sprite, (x - self.offset_x, y - self.offset_y))
        if (self.dist_player_sprite(x,y)<300):
            self.screen.blit(sprite, (x - self.total_x_offset(), y - self.total_y_offset()))

    def draw_drawable (self, drawable):
        self.draw_sprite(drawable.sprite, drawable.x, drawable.y)

    def draw_fog(self,x,y):
        self.player_pos_x =x
        self.player_pos_y =y

    def dist_player_sprite(self,x,y):
      distancia = math.sqrt(math.pow((x-self.player_pos_x),2)+math.pow((y-self.player_pos_y),2))

      return distancia