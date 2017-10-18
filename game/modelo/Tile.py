# coding=utf-8
__author__ = "Ignacio Oliveto"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ignacio Oliveto"
__email__ = "igoliveto@gmail.com"
__status__ = "Prototype"

class Tile:
    def __init__(self, walkable, sprite, x, y, event):
        self.walkable = walkable
        self.sprite = sprite
        self.x = x
        self.y = y
        self.event = event

    def set_event(self,event):
        self.event = event

    def is_walkable(self):
        return self.walkable


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