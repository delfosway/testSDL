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
import util.Vector
import util.Util


class Character (pygame.sprite.Sprite):

    BASE_AC_LVL_MULTIPLIER = 1
    BASE_DMG_LVL_MULTIPLIER = 5

    CHARACTER_SPRITE_WIDTH = 64
    CHARACTER_SPRITE_HEIGHT = 64

    CHARACTER_COLLIDER_WIDTH = 60
    CHARACTER_COLLIDER_HEIGHT = 60

    BULLET_SPEED = 10

    SHOOT_COOLDOWN = 60
    PLAYER_SHOOT_COOLDOWN = 15
    AI_SIGHT_DISTANCE = 300
    AI_SPEED = 4

    def __init__(self, image, lvl, base_max_hp, base_max_mp, bullet_sound, bullet_image, death_sound, equipment = None):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Test Character"
        self.image = image
        self.rect = pygame.rect.Rect((0, 0), (self.CHARACTER_COLLIDER_WIDTH, self.CHARACTER_COLLIDER_HEIGHT))
        self.rect.x = 0
        self.rect.y = 0

        self.speed_x = 0
        self.speed_y = 0
        #self.sprite = sprite

        self.current_gold  = 0
        self.total_gold = 0
        self.kills = 0
        self.base_max_hp = base_max_hp
        self.base_max_mp = base_max_mp
        self.max_hp = 0
        self.max_mp = 0
        self.hp = 0
        self.mp = 0
        self.lvl = 0
        self.set_lvl(lvl)
        self.kills = 0
        self.is_dead = False

        self.current_map = None
        self.bullet_sound = bullet_sound
        self.bullet_image = bullet_image
        self.death_sound = death_sound


        self.frames_since_last_shot = 0

        if equipment == None:
            self.equipment = modelo.Equipment.Equipment(None)

    def heal_to_max(self):
        self.hp = self.max_hp

    def add_gold(self, gold_amount):
        self.current_gold += gold_amount
        self.total_gold += gold_amount

    def subtract_gold(self, gold_amount):
        self.current_gold -= gold_amount

    def can_afford(self, price):
        return self.current_gold >= price

    def set_lvl(self, lvl):
        self.lvl = lvl
        self.max_hp = self.base_max_hp * self.lvl
        self.max_mp = self.base_max_mp * self.lvl
        self.hp = self.max_hp
        self.mp = self.max_mp

    def shoot(self, speed_x, speed_y):
        if self.is_player():
            if self.frames_since_last_shot < self.PLAYER_SHOOT_COOLDOWN:
                return
        else:
            if self.frames_since_last_shot < self.SHOOT_COOLDOWN:
                return
        self.frames_since_last_shot = 0
        self.play_shoot_sound(self.bullet_sound)
        self.current_map.spawn_bullet(modelo.Bullet.Bullet(self.rect.x, self.rect.y, self.bullet_image, self, 10,speed_x, speed_y, self.current_map, self.bullet_sound))

    def shoot_at(self, x, y):

        diff_vector = util.Vector.Vector(x - self.rect.x, y - self.rect.y)
        diff_vector.normalizar()
        self.shoot(diff_vector.x * self.BULLET_SPEED, diff_vector.y * self.BULLET_SPEED)

    #def shoot_at(self, x, y):
     #   diff_vector = util.Vector.Vector(x - player.rect.x, y - player.rect.y)
      #  mouse_vector.normalizar()
       # self.shoot(mouse_vector.x * 10, mouse_vector.y * 10)

    def play_shoot_sound(self, sound):
        channel = pygame.mixer.find_channel(1)
        if not channel.get_busy():
            channel.queue(sound)
        else:
            channel2 = pygame.mixer.find_channel(2)
            channel2.queue(sound)

    def play_death_sound(self):
        channel = pygame.mixer.find_channel(6)
        if not channel.get_busy():
            channel.queue(self.death_sound)
        else:
            channel2 = pygame.mixer.find_channel(7)
            channel2.queue(self.death_sound)

    def set_speed(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.update_frames()
        if not self.is_player():
            self.AI_play()

        self.move(self.speed_x, 0)
        self.move(0, self.speed_y)
        #print ("Updating Character...")

    def update_frames(self):
        self.frames_since_last_shot += 1

    def is_player(self):
        return self.current_map.game_manager.current_player == self

    def AI_play(self):
        player = self.current_map.game_manager.current_player
        if self.is_on_player_sight():
            self.shoot_at(player.rect.x, player.rect.y)
            self.set_speed_towards(player)

    def is_on_player_sight(self):
        player = self.current_map.game_manager.current_player
        return util.Util.distance(self.rect.x, self.rect.y, player.rect.x, player.rect.y) < self.AI_SIGHT_DISTANCE

    def set_speed_towards(self, target):
        diff_vector = util.Vector.Vector(target.rect.x - self.rect.x, target.rect.y - self.rect.y)
        diff_vector.normalizar()
        self.set_speed(diff_vector.x * self.AI_SPEED, diff_vector.y * self.AI_SPEED)

    def move(self, x, y):
        if (x != 0 or y != 0):
            old_x = self.rect.x
            old_y = self.rect.y
            self.rect.x += x
            self.rect.y += y
            if self.is_colliding_with_wall(): #colliding
                self.rect.x = old_x
                self.rect.y = old_y
            elif self.is_colliding_with_character():
                self.rect.x = old_x
                self.rect.y = old_y
            colliding_event = self.is_colliding_with_event()
            if colliding_event:
                colliding_event.apply(self)

    def is_colliding_with_wall(self):
        walls = self.current_map.walls
        rect = self.get_rect()
        for wall in walls:
            if rect.colliderect(wall.get_rect()):
                return True
        return False

    def is_colliding_with_event(self):
        events = self.current_map.events
        rect = self.get_rect()
        for event in events:
            if rect.colliderect(event.get_rect()):
                return event
        return False

    def is_colliding_with_character(self):
        characters = self.current_map.characters
        rect = self.get_rect()
        for character in characters:
            if rect.colliderect(character.rect):
                if character != self:
                    return True
        return False

    def spawn(self, map, map_x, map_y):
        self.current_map = map
        self.rect.x = map_x * modelo.Tile.Tile.TILE_WIDTH
        self.rect.y = map_y * modelo.Tile.Tile.TILE_HEIGHT

    def killed_character(self, killed_character):
        self.add_gold(killed_character.lvl)
        self.kills += 1

    def base_ac(self):
        return self.lvl * self.BASE_AC_LVL_MULTIPLIER

    def base_dmg(self):
        return self.lvl * self.BASE_DMG_LVL_MULTIPLIER

    def total_ac(self):
        return self.equipment.total_ac() + self.base_ac()

    def receive_damage (self, damage_amount, source):
        hp_to_substract = damage_amount - self.total_ac()
        if hp_to_substract <= 0:
            hp_to_substract = 1
        self.subtract_hp(hp_to_substract)
        if self.is_dead:
            source.killed_character(self)

    def heal (self, heal_amount):
        self.add_hp(heal_amount)

    def add_hp(self, hp_to_add):
        self.hp += hp_to_add
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def subtract_hp(self, hp_to_substract):
        self.hp -= hp_to_substract
        if self.hp <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.play_death_sound()

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
        self.draw_health_bar(camera)

    def draw_health_bar(self, camera):
        bar_length = int(max(min(self.hp / float(self.max_hp) * 64, 64), 0))
        rect = pygame.rect.Rect(self.rect.x, self.rect.y + 64, bar_length, 4)
        camera.draw_rect(rect)
        #print ("Rect Length : " + bar_length)

    def get_rect(self):
        return self.rect

    def copy(self):
        new_character = Character(self.image, self.lvl, self.max_hp, self.max_mp, self.bullet_sound, self.bullet_image, self.equipment.copy())
        new_character.kills = self.kills
        return new_character

    def fresh_copy(self):
        new_character = Character(self.image, self.lvl, self.max_hp, self.max_mp, self.bullet_sound, self.bullet_image, self.death_sound, None)
        new_character.kills = self.kills
        return new_character
