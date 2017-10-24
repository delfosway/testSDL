# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

import negocio.ItemManager
import negocio.CharacterManager
import pygame
import modelo.Character
import negocio.ItemManager
import modelo.TileMap
import negocio.Camera
import util.DungeonGenerator
import util.Graphics
import util.Util
import util.Vector
from pygame import *

class GameManager:
    FPS = 60

    def __init__(self):
        self.camera = negocio.Camera.Camera(800, 600)
        self.item_manager = negocio.ItemManager.ItemManager()
        self.character_manager = negocio.CharacterManager.CharacterManager()
        self.current_player = None
        self.current_lvl = 0
        self.current_map = None
        self.clock = pygame.time.Clock()

    def set_current_player(self,character):
        self.current_player = character

    def start(self):

        #Creamos la Camara
        self.camera = negocio.Camera.Camera(800, 600)
        #Creamos al Player (Heroe) y lo asignamos como Player Actual
        player = self.character_manager.get_player()
        self.set_current_player(player)
        #Attachamos la camara al Player.
        self.camera.attach_to_drawable(player)
        #Mostramos Tutorial
        tuto = True
        self.tutorial(tuto)
        #Mostramos Menu Principal
        menu = True
        self.main_menu(menu)
        #Iniciamos el juego con el primer nivel.
        self.start_lvl(1)
        self.main_loop()
        self.end_game()

    def start_lvl(self, lvl):
        #Asignamos el nivel actual.
        self.current_lvl = lvl
        #Creamos un nuevo Tilemap.
        self.current_map = modelo.TileMap.TileMap(lvl, self)

        #Generamos un nuevo mapa aleatorio y construimos el tilemap
        #a partir de el.
        self.current_map.load_from_grid(
            util.DungeonGenerator.crearHabitaciones(
                self.current_map.MAP_WIDTH, self.current_map.MAP_HEIGHT))
        #Spawneamos al heroe
        self.current_map.spawn_character_at_random_walkable(self.current_player)
        #Spawneamos los enemigos
        self.current_map.spawn_random_enemies(100)
        self.current_map.generate_random_tile_events(50)

    def start_next_lvl(self):
        self.start_lvl(self.current_lvl + 1)

    def main_loop(self):
        player = self.current_player

        run_speed_multiplier = 1.5
        speed = 3

        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)

        bgmchannel = pygame.mixer.find_channel(0)
        bgmchannel.queue(pygame.mixer.Sound("SFX/bgmusic.ogg"))

        running = True
        while running:
            self.clock.tick(self.FPS)

            # Chequeamos si el player sigue vivo.
            # En caso contrario, salimos del Main Loop.
            if player.is_dead:
                self.update_and_draw()
                self.wait_seconds(1)
                running = False
            if player.kills >= 5:
                self.start_next_lvl()
                player.kills = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                        self.pause(paused)
            if pygame.mouse.get_pressed()[0]:
                try:
                    x, y = self.camera.get_mouse_map_position()
                    player.shoot_at(x, y)
                except AttributeError:
                    pass

            movement_x = 0
            movement_y = 0

            # Calculo desplazamiento a partir de las teclas presionadas.
            pressed = pygame.key.get_pressed()
            if pressed[K_w]:
                movement_y += -speed
            if pressed[K_s]:
                movement_y += speed
            if pressed[K_a]:
                movement_x += -speed
            if pressed[K_d]:
                movement_x += speed

            # Incremento la velocidad si esta corriendo:
            if pressed[K_LSHIFT]:
                movement_x = movement_x * run_speed_multiplier
                movement_y = movement_y * run_speed_multiplier
            player.set_speed(movement_x, movement_y)

            # UPDATE AND DRAW:
            self.update_and_draw()

    def wait_seconds(self, seconds):
        wait_frames = self.FPS * seconds
        while wait_frames > 0:
            self.clock.tick(self.FPS)
            wait_frames -= 1

    def update_and_draw(self):
        self.update()
        self.draw()

    def update(self):
        # UPDATE
        self.current_map.update()
        self.camera.update()

    def draw(self):
        # DRAW
        self.camera.fill_background()
        self.current_map.draw(self.camera)
        self.camera.draw_text("Gold  : " + str(self.current_player.current_gold), 0, 0)
        self.camera.draw_text("Score : " + str(self.current_player.current_gold), 0, 30)
        pygame.display.flip()

    def end_game(self):
        self.endgame_menu()

    def endgame_menu(self):
        state = True
        while state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        state = False

            self.camera.fill_menu()
            self.camera.draw_text("You have died horribly...", 200, 150, util.Graphics.BLACK)
            self.camera.draw_text("Your final score is : " + str(self.current_player.total_gold), 200, 250, util.Graphics.BLACK)
            self.camera.draw_text("Press enter to quit the game", 170, 350, util.Graphics.BLACK)
            pygame.display.update()

    def main_menu(self, state):
        while state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        state = False

            self.camera.fill_menu()
            self.camera.draw_text("Welcome to the main menu", 200, 150, util.Graphics.BLACK)
            self.camera.draw_text("Press enter to start the game", 170, 350, util.Graphics.BLACK)

            pygame.display.update()

    def shop_menu(self, state):
        while state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        state = False

            self.camera.fill_menu()
            self.camera.draw_text("Welcome to the main menu", 200, 150, util.Graphics.BLACK)
            # menu_text = pygame.font.Font('arial.ttf', 50)
            # text_surface, text_rect = text_draw("Welcome to the main menu", menu_text)
            # text_rect = 80, 100
            # camera.screen.blit(text_surface, text_rect)
            self.camera.draw_text("Press enter to start the game", 160, 350, util.Graphics.BLACK)

            # menu_text2 = pygame.font.Font('arial.ttf', 35)
            # text_surface2, text_rect2 = text_draw("Press enter to start the game", menu_text2)
            # text_rect2 = 160, 400
            # camera.screen.blit(text_surface2, text_rect2)
            pygame.display.update()

    def tutorial(self, state):
        while state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        state = False

            text_x = 250

            self.camera.fill_menu()

            self.camera.draw_text("HOW TO PLAY", 300, 100, util.Graphics.BLACK, 115)

            self.camera.draw_text("MOVE WITH W, A, S, D", text_x, 250, util.Graphics.BLACK, 30)

            self.camera.draw_text("AIM WITH YOUR MOUSE", text_x, 300, util.Graphics.BLACK, 30)

            self.camera.draw_text("SHOOT WITH [MOUSE1]", text_x, 400, util.Graphics.BLACK, 30)

            self.camera.draw_text("PRESS ENTER TO CONTINUE", text_x - 20, 500, util.Graphics.BLACK, 30)



            pygame.display.update()

    def text_draw(self, text, font):
        text_surface = font.render(text, True, util.Graphics.BLACK)
        return text_surface, text_surface.get_rect()

    def pause(self, paused):
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

            menu_text = pygame.font.Font('arial.ttf', 115)
            text_surface, text_rect = self.text_draw("Paused", menu_text)
            text_rect = 200, 150

            self.camera.screen.blit(text_surface, text_rect)

            pygame.display.update()

