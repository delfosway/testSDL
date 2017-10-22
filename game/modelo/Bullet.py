# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

#

import pygame
import util.Util

class Bullet(pygame.sprite.Sprite):

    BULLET_SPRITE_WIDTH = 16
    BULLET_SPRITE_HEIGHT = 16

    BULLET_MAX_DISTANCE = 600

    def __init__(self, x, y, image, source, dmg, speed_x, speed_y, map):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.travelled_distance = 0
        self.source = source #Character
        self.dmg = dmg #Damage - int
        self.speed_x = speed_x #Speed on X
        self.speed_y = speed_y #Speed on Y
        self.current_map = map
        self.is_alive = True

    def collide_with_character(self, character):
        character.receive_damage(self.dmg)
        self.destroy()

    def is_alive(self):
        return self.is_alive

    def is_dead(self):
        return not self.is_alive

    def collide_with_wall(self):
        self.destroy()

    def collide_with_bullet(self):
        self.destroy()

    def destroy(self):
        self.kill()
        self.is_alive = False

    def draw(self, camera):
        camera.draw_drawable(self)

    def update(self):
        self.move(self.speed_x, self.speed_y)
        #self.move(0, self.speed_y)

    def move(self, x, y):

        if (x != 0 or y != 0):
            self.rect.x += x
            self.rect.y += y

            self.travelled_distance += util.Util.hypotenuse(x, y)

            if self.travelled_distance >= self.BULLET_MAX_DISTANCE:
                self.destroy()
            elif self.is_colliding_with_walls():
                self.collide_with_wall()
            elif self.is_colliding_with_bullets():
                self.collide_with_bullet()
            else:
                colliding_character = self.is_colliding_with_character()
                if colliding_character:
                    self.collide_with_character(colliding_character)

    def generate_rect(self):
        return pygame.Rect(self.rect.x, self.rect.y, self.BULLET_SPRITE_WIDTH, self.BULLET_SPRITE_HEIGHT)

    def is_colliding_with_walls(self):
        walls = self.current_map.walls
        rect = self.generate_rect()
        for wall in walls:
            if rect.colliderect(wall):
                channel = pygame.mixer.find_channel(3)
                if not channel.get_busy():
                    channel.queue(pygame.mixer.Sound("SFX/explosion.ogg"))
                else:
                    channel2 = pygame.mixer.find_channel(4)
                    channel2.queue(pygame.mixer.Sound("SFX/explosion.ogg"))
                #print("Bullet collided with Wall!")
                return True
        return False

    def is_colliding_with_bullets(self):
        bullets = self.current_map.bullets
        rect = self.generate_rect()
        for bullet in bullets:
            if bullet != self:
                if rect.colliderect(bullet):
                    #print ("Bullet collided with Bullet!")
                    return True
        return False

    def is_colliding_with_character(self):
        characters = self.current_map.characters
        rect = self.generate_rect()
        for character in characters:
            if rect.colliderect(character):
                if character != self.source:
                    channel = pygame.mixer.find_channel(5)
                    if not channel.get_busy():
                        channel.queue(pygame.mixer.Sound("SFX/explosion.ogg"))
                    else:
                        channel2 = pygame.mixer.find_channel(6)
                        channel2.queue(pygame.mixer.Sound("SFX/explosion.ogg"))
                    #print("Bullet collided with Character!")
                    return character
        return False