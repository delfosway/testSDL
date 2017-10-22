# coding=utf-8
__author__ = "Gonzalo Montaña"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Gonzalo Montaña"
__email__ = "gonza_257@gmail.com"
__status__ = "Prototype"

import modelo.Equipment
import modelo.Tile
import modelo.Bullet
import pygame




class Character (pygame.sprite.Sprite):

    BASE_AC_LVL_MULTIPLIER = 1
    BASE_DMG_LVL_MULTIPLIER = 2

    CHARACTER_SPRITE_WIDTH = 64
    CHARACTER_SPRITE_HEIGHT = 64

    CHARACTER_COLLIDER_WIDTH = 60
    CHARACTER_COLLIDER_HEIGHT = 60

    def __init__(self, image, lvl, max_hp, max_mp, equipment = None):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Test Character"
        self.image = image
        self.rect = pygame.rect.Rect((0, 0), (self.CHARACTER_COLLIDER_WIDTH, self.CHARACTER_COLLIDER_HEIGHT))
        self.rect.x = 0
        self.rect.y = 0

        self.speed_x = 0
        self.speed_y = 0
        #self.sprite = sprite



        self.max_hp = max_hp
        self.max_mp = max_mp

        self.is_dead = False
        self.lvl = lvl
        self.current_map = None
        if equipment == None:
            self.equipment = modelo.Equipment.Equipment(None)

    def shoot(self, speed_x, speed_y):
        self.current_map.spawn_bullet(modelo.Bullet.Bullet(self.rect.x, self.rect.y, pygame.image.load("Graficos/fireball red.png").convert_alpha(), self, 10,speed_x, speed_y, self.current_map))

    def set_speed(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.move(self.speed_x, 0)
        self.move(0, self.speed_y)
        #print ("Updating Character...")

    def move(self, x, y):
        if (x != 0 or y != 0):
            old_x = self.rect.x
            old_y = self.rect.y
            self.rect.x += x
            self.rect.y += y
            if self.is_colliding_with_wall(): #colliding
                self.rect.x = old_x
                self.rect.y = old_y
            #elif self.is_colliding_with_character():
            #    self.rect.x = old_x
            #    self.rect.y = old_y

    def is_colliding_with_wall(self):
        walls = self.current_map.walls
        rect = self.get_rect()
        for wall in walls:
            if rect.colliderect(wall.get_rect()):
                return True
        return False

    def is_colliding_with_character(self):
        characters = self.current_map.characters
        rect = self.get_rect()
        for character in characters:
            if rect.colliderect(character.rect):
                return True
        return False

    def spawn(self, map, map_x, map_y):
        self.current_map = map
        self.rect.x = map_x * modelo.Tile.Tile.TILE_WIDTH
        self.rect.y = map_y * modelo.Tile.Tile.TILE_HEIGHT

    def base_ac(self):
        return self.lvl * self.BASE_AC_LVL_MULTIPLIER

    def base_dmg(self):
        return self.lvl * self.BASE_DMG_LVL_MULTIPLIER

    def total_ac(self):
        return self.equipment.total_ac() + self.base_ac()

    def receive_damage (self, damage_amount):
        hp_to_substract = damage_amount - self.total_ac()
        if hp_to_substract <= 0:
            hp_to_substract = 1
        self.subtract_hp(hp_to_substract)


    def heal (self, heal_amount):
        self.add_hp(heal_amount)

    def add_hp(self, hp_to_add):
        self.hp += hp_to_add
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def subtract_hp(self, hp_to_substract):
        self.hp -= hp_to_substract
        if self.hp <= 0:
            self.is_dead = True

    def add_mp(self, mp_to_add):
        self.mp += mp_to_add
        if self.mp > self.max_mp:
            self.mp = self.max_mp

    def subtract_mp(self, mp_to_substract):
        self.mp -= mp_to_substract
        if self.mp <= 0:
            self.mp = 0

    def draw(self, camera):
        camera.draw_drawable(self)

    def get_rect(self):
        return self.rect

    def move_ai(self, px, py, ex, ey): #px py = player coordinates, ex ey = enemy coordinates
        self.px = px
        self.py = py
        self.ex = ex
        self.ey = ey


