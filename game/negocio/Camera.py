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
import util.Util
import util.Graphics
import modelo.Tile

class Camera:

    LIGHT_RADIUS = 300

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

        self.pixelart_font = pygame.font.Font('pixelart.ttf', 30)
        self.arial_font = pygame.font.Font('arial.ttf', 30)

    def attach_to_drawable(self, drawable):
        self.attached_drawable = drawable
        self.update()

    def update(self):
        if self.attached_drawable is not None:
            self.offset_x = self.attached_drawable.rect.x
            self.offset_y = self.attached_drawable.rect.y

    def fill_background(self):
        self.screen.fill(util.Graphics.BLACK)

    def fill_menu(self):
        self.screen.fill(util.Graphics.WHITE)

    def total_x_offset(self):
        return self.offset_x - (self.camera_width / 2)

    def total_y_offset(self):
        return self.offset_y - (self.camera_height / 2)

    def get_mouse_map_position(self):
        x, y = pygame.mouse.get_pos()
        x += self.total_x_offset()
        y += self.total_y_offset()
        return x, y

    def draw_sprite(self, sprite, x, y):
        # if self.dist_player_sprite(x, y) < self.LIGHT_RADIUS: #FOG
        # print("Dibujando " + util.Util.position_to_string(x, y))
        self.screen.blit(sprite, (x - self.total_x_offset(), y - self.total_y_offset()))

    def draw_fixed_sprite(self, sprite, x, y):
        self.screen.blit(sprite, x, y)

    def draw_drawable (self, drawable):
        if self.is_on_light_radius(drawable):
            self.draw_sprite(drawable.image, drawable.rect.x, drawable.rect.y)

    def draw_fixed_drawable(self, drawable):
        self.draw_fixed_sprite(drawable.image, drawable.rect.x, drawable.rect.y)

    def draw_text(self, text, x, y, color = util.Graphics.WHITE, size = 30):
        menu_text2 = self.pixelart_font
        text_surface2, text_rect2 = self.prepare_text(text, menu_text2, color)
        text_rect2 = x, y
        #print ("Text to Draw : " + text)
        self.screen.blit(text_surface2, text_rect2)

    def draw_map(self, map):
        player_map_x, player_map_y = self.get_attached_drawable_tile(map)
        tile_radius = (self.LIGHT_RADIUS // map.tiles[0][0].TILE_WIDTH) + 2
        for x in range(player_map_x - tile_radius, player_map_x + tile_radius):
            for y in range(player_map_y - tile_radius, player_map_y + tile_radius):
                if not map.is_index_out_of_bounds(x, y):
                    if self.is_on_light_radius(map.tiles[x][y]):
                        self.draw_drawable(map.tiles[x][y])

    def draw_rect(self, rect):
        if self.is_rect_on_light_radius(rect):
            rect.x -= self.total_x_offset()
            rect.y -= self.total_y_offset()
            pygame.draw.rect(self.screen, util.Graphics.GREEN, rect, 0)

    def prepare_text(self, text, font, color):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def get_attached_drawable_tile(self, map):
        return self.attached_drawable.rect.x // map.MAP_WIDTH, self.attached_drawable.rect.y // map.MAP_HEIGHT

    def is_rect_on_light_radius(self, rect):
        return self.dist_player_sprite(rect.x, rect.y) < self.LIGHT_RADIUS

    def is_on_light_radius(self, drawable):
        return self.dist_player_sprite(drawable.rect.x, drawable.rect.y) < self.LIGHT_RADIUS

    def dist_player_sprite(self, x, y):
        distancia = math.sqrt(math.pow((x - self.attached_drawable.rect.x), 2) + math.pow((y - self.attached_drawable.rect.y), 2))
        return distancia