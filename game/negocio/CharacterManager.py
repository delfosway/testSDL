# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

import modelo.Character
import modelo.Bullet
import pygame
from random import randint


class CharacterManager:



    def __init__(self):

        self.PLAYER_SPRITE = None
        self.character_images = []
        self.bullet_images = []

        self.enemy_shoot_sound = None
        self.player_shoot_sound = None
        self.death_sound = None
        self.characters = []
        self.player_character = None

        self.load_images()
        self.load_sounds()
        self.create_characters()

    def load_images(self):
        self.PLAYER_SPRITE = pygame.image.load("Graficos/archon.png").convert_alpha()
        self.character_images.append(pygame.image.load("Graficos/enemy1.png").convert_alpha())
        self.character_images.append(pygame.image.load("Graficos/enemy2.png").convert_alpha())
        self.character_images.append(pygame.image.load("Graficos/enemy3.png").convert_alpha())
        self.character_images.append(pygame.image.load("Graficos/enemy4.png").convert_alpha())
        self.character_images.append(pygame.image.load("Graficos/enemy5.png").convert_alpha())
        self.character_images.append(pygame.image.load("Graficos/enemy6.png").convert_alpha())
        self.bullet_images.append(pygame.image.load("Graficos/fireball red.png").convert_alpha())
        self.bullet_images.append(pygame.image.load("Graficos/fireball black.png").convert_alpha())
        self.bullet_images.append(pygame.image.load("Graficos/fireball green.png").convert_alpha())
        self.bullet_images.append(pygame.image.load("Graficos/fireball blue.png").convert_alpha())
        self.bullet_images.append(pygame.image.load("Graficos/fireball purple.png").convert_alpha())


    def load_sounds(self):
        self.player_shoot_sound = pygame.mixer.Sound("SFX/shoot2.ogg")
        self.enemy_shoot_sound = pygame.mixer.Sound("SFX/shoot3.wav")
        self.death_sound = pygame.mixer.Sound("SFX/death1.ogg")

    def create_characters(self):
        self.characters = []

        player = modelo.Character.Character(self.PLAYER_SPRITE, 1, 50, 0, self.player_shoot_sound, self.bullet_images[0], self.death_sound)
        self.player = player

        enemy1 = modelo.Character.Character(self.character_images[0], 1, 10, 100, self.enemy_shoot_sound,
                                            self.bullet_images[1], self.death_sound)
        enemy2 = modelo.Character.Character(self.character_images[1], 1, 15, 100, self.enemy_shoot_sound,
                                            self.bullet_images[2], self.death_sound)
        enemy3 = modelo.Character.Character(self.character_images[2], 1, 20, 100, self.enemy_shoot_sound,
                                            self.bullet_images[3], self.death_sound)
        enemy4 = modelo.Character.Character(self.character_images[3], 1, 25, 100, self.enemy_shoot_sound,
                                            self.bullet_images[4], self.death_sound)
        enemy5 = modelo.Character.Character(self.character_images[4], 1, 30, 100, self.enemy_shoot_sound,
                                            self.bullet_images[4], self.death_sound)
        enemy6 = modelo.Character.Character(self.character_images[5], 1, 35, 100, self.enemy_shoot_sound,
                                            self.bullet_images[3], self.death_sound)
        self.characters.append(enemy1)
        self.characters.append(enemy2)
        self.characters.append(enemy3)
        self.characters.append(enemy4)
        self.characters.append(enemy5)
        self.characters.append(enemy6)

    def get_player(self):
        return self.player.fresh_copy()

    def get_character(self, index):
        return self.characters[index].fresh_copy()

    def get_random_enemy(self, floor_lvl):
        char = self.get_character(randint(0, len(self.characters) - 1))
        char.set_lvl(floor_lvl)
        return char
