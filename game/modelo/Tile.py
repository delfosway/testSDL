# coding=utf-8
__author__ = "Ignacio Oliveto"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ignacio Oliveto"
__email__ = "igoliveto@gmail.com"
__status__ = "Prototype"

import pygame


class Tile (pygame.sprite.Sprite):

    TILE_WIDTH = 64  # Pixels
    TILE_HEIGHT = 64  # Pixels

    TILE_COLLIDER_WIDTH = 60
    TILE_COLLIDER_HEIGHT = 60

    def __init__(self, walkable, image, x, y, event):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = pygame.rect.Rect((0, 0) , (self.TILE_COLLIDER_WIDTH, self.TILE_COLLIDER_HEIGHT))
        self.x = 0
        self.y = 0
        self.set_position(x, y)
        self.walkable = walkable
        self.event = event

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x * self.TILE_WIDTH
        self.rect.y = y * self.TILE_HEIGHT
        #print("Tile [" + str(self.x) + "," + str(self.y) + "] Rect position : [" + str(
        #    self.rect.x) + "," + str(self.rect.y) + "]")

    def draw(self, camera):
        camera.draw_drawable(self)
        if self.event is not None:
            camera.draw_sprite(self.event.sprite, self.rect.x, self.rect.y)

    def set_event(self,event):
        self.event = event

    def is_walkable(self):
        return self.walkable

    def get_rect(self):
        return self.rect

    def copy(self):
        new_tile = Tile(self.walkable, self.image, self.x, self.y, self.event)
        return new_tile

class TileEvent:

    def __init__(self, tile, sprite , hp = 0, mp = 0, dmg_to_deal = 0, next_lvl = False):
        self.tile = tile
        self.sprite = sprite
        self.hp = hp
        self.mp = mp
        self.dmg_to_deal = dmg_to_deal
        self.next_lvl = next_lvl

    def apply(self, character, game_manager):
        if self.hp > 0:
            character.heal(self.hp)
        if self.mp > 0:
            character.add_mp(self.mp)
        if self.dmg_to_deal > 0:
            character.receive_damage(self.dmg_to_deal)
        if self.next_lvl:
            game_manager.go_to_next_lvl()