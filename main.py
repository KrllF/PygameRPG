import sys
import pygame

from menu import *
from config import *
from collision import BLOCK
from player import *
from collision import Spritesheet
from collision import Ground
from enemy import *
from database import *

pygame.display.set_caption('GAME WITH RPG ELEMENTS')

# data_base
add_player(1)


class SGAME:
    def __init__(self):
        pygame.init()
        self.game_over_bool = False
        self.FPS = FPS
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet("imagestest/character.png")
        self.terrain_spritesheet = Spritesheet("imagestest/terrain.png")
        self.enemy_spritesheet = Spritesheet("imagestest/enemy.png")

        self.font = pygame.font.Font('fonts/EightBits.ttf', 32)
        self.font1 = pygame.font.Font('fonts/EightBits.ttf', 64)

        # map

        self.floor_surface = pygame.image.load('images/map_bg.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def create_map(self):
        for index, layer in enumerate(layers_of_map):
            for row_index, row in enumerate(layer):
                for col_index, col in enumerate(row):
                    pos = (col_index, row_index)
                    if col != '-1':
                        if index == 0:
                            # map border
                            BLOCK(self, pos, 'block')
                        elif index == 1:
                            # trees
                            BLOCK(self, pos, 'tree')

                        elif index == 2:
                            robber(self, pos)
                            pass
                        if index == 3:
                            # bosses
                            pass

    def new_game(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.unvisible = pygame.sprite.LayeredUpdates()

        self.create_map()

        self.player = Player(self, (20, 10))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

    def update(self):
        self.all_sprites.update()
        pygame.display.update()

    def camera(self):
        offset = pygame.math.Vector2(self.player.rect.centerx - SIZE[0] // 2, self.player.rect.centery - SIZE[1] // 2)
        floor_offset_rect = self.floor_rect.topleft - offset
        self.screen.blit(self.floor_surface, floor_offset_rect)

        for sprite in sorted(
                self.all_sprites,
                key=lambda sprite: sprite.rect.centery):
            offset_of_sprite = sprite.rect.topleft - offset
            if type(sprite).__name__ == "robber":
                sprite.health_bar(offset)

            self.screen.blit(sprite.image, offset_of_sprite)

    def draw(self):
        self.screen.fill(BLACK)
        # для карты временно

        self.camera()
        self.clock.tick(self.FPS)

    def check_main(self):
        if self.players.empty():
            self.running = False

    def main(self):
        while self.running:
            self.events()
            self.draw()
            self.update()
            if self.game_over_bool:
                self.running = False
        self.running = False

    def game_over(self):
        restart_buttom = Menu_button((415, 300), 250, 100, BLACK, WHITE, 'Restart', 32, 2)
        menu_buttom = Menu_button((490, 500), 100, 50, BLACK, WHITE, 'Menu', 32, 2)
        game_over_bool = True
        for sprite in self.all_sprites:
            sprite.kill()
        while game_over_bool:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if restart_buttom.is_pressed(mouse_pos, events):
                game_over_bool = False
                self.__init__()
                self.new_game()
                while self.running:
                    self.main()
                    self.game_over()

            if menu_buttom.is_pressed(mouse_pos, events):
                game_over_bool = False
                self.__init__()
                self.menu()

            self.screen.fill(BLACK)
            self.screen.blit(restart_buttom.image, restart_buttom.rect)
            self.screen.blit(menu_buttom.image, menu_buttom.rect)

            self.clock.tick(60)
            pygame.display.update()

    def menu(self):
        local_game = Menu_button((415, 50), 250, 100, BLACK, WHITE, 'Local play', 32, 2)
        about_game = Menu_button((415, 200), 250, 100, BLACK, WHITE, 'About game', 32, 2)
        setting = Menu_button((415, 350), 250, 100, BLACK, WHITE, 'Setting', 32, 2)
        exit_game = Menu_button((415, 500), 250, 100, BLACK, WHITE, 'Exit', 32, 2)
        back = Menu_button((415, 500), 250, 100, BLACK, WHITE, 'Back', 32, 2)
        statistics_game = Menu_button((800, 50), 200, 100, BLACK, WHITE, 'Statistics', 32, 2)
        reset_kills_game = Menu_button((800, 130), 100, 50, BLACK, WHITE, 'Reset kills', 32, 2)
        reset_play_time_game = Menu_button((800, 230), 100, 50, BLACK, WHITE, 'Reset time', 32, 2)
        reset_number_of_attempts_game = Menu_button((800, 330), 100, 50, BLACK, WHITE, 'Reset time', 32, 2)
        sliderFPS = Slider((SIZE[0] // 2, SIZE[1] // 2 - 100), (200, 50), 0.5, 30, 120)

        intro = True
        about_game_bool = False
        setting_bool = False
        statistics_bool = False

        while intro:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()

            if reset_kills_game.is_pressed(mouse_pos, events):
                reset_kills(1)
            if reset_play_time_game.is_pressed(mouse_pos, events):
                reset_play_time(1)
            if reset_number_of_attempts_game.is_pressed(mouse_pos, events):
                reset_number_of_attempts(1)

            if about_game_bool or setting_bool or statistics_bool:
                if back.is_pressed(mouse_pos, events):
                    about_game_bool = False
                    setting_bool = False
                    statistics_bool = False

            else:
                if local_game.is_pressed(mouse_pos, events):
                    intro = False
                    self.new_game()

                    while self.running:
                        self.main()
                        self.game_over()

                if statistics_game.is_pressed(mouse_pos, events):
                    statistics_bool = True

                if about_game.is_pressed(mouse_pos, events):
                    about_game_bool = True

                if setting.is_pressed(mouse_pos, events):
                    setting_bool = True

                if exit_game.is_pressed(mouse_pos, events):
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK)

            if about_game_bool:
                self.screen.blit(back.image, back.rect)
                self.screen.blit(self.font.render(ABOUT_GAME, True, 'WHITE'), (10, 10))
                self.screen.blit(self.font.render(ABOUT_GAME1, True, 'WHITE'), (10, 30))
                self.screen.blit(self.font.render(ABOUT_GAME2, True, 'WHITE'), (10, 50))

            elif setting_bool:
                mouse_pos = pygame.mouse.get_pos()
                mouse_press = pygame.mouse.get_pressed()
                if sliderFPS.container_rect.collidepoint(mouse_pos) and mouse_press[0]:
                    sliderFPS.move_slider(mouse_pos)

                self.screen.blit(self.font1.render("SETTING", True, 'WHITE'), (470, 50))
                sliderFPS.render(self)
                self.FPS = sliderFPS.get_value()
                self.screen.blit(self.font.render("FPS:", True, 'WHITE'), (300, SIZE[1]//2-115))
                self.screen.blit(self.font.render(str(int(sliderFPS.get_value())), True, 'WHITE'), (SIZE[0]//2-8, SIZE[1]//2-60))

                self.screen.blit(back.image, back.rect)
            elif statistics_bool:
                self.screen.blit(back.image, back.rect)
                self.screen.blit(reset_kills_game.image, reset_kills_game.rect)
                self.screen.blit(reset_play_time_game.image, reset_play_time_game.rect)
                self.screen.blit(reset_number_of_attempts_game.image, reset_number_of_attempts_game.rect)
                self.screen.blit(self.font1.render("STATISTICS", True, 'WHITE'), (440, 50))

                self.screen.blit(self.font.render("KILLS:", True, 'WHITE'), (100, 150))
                self.screen.blit(self.font.render(str(get_kills(1)), True, 'WHITE'), (170, 150))

                self.screen.blit(self.font.render("PLAY TIME:", True, 'WHITE'), (100, 250))
                self.screen.blit(self.font.render(str(get_play_time(1)) + ' sec', True, 'WHITE'), (230, 250))

                self.screen.blit(self.font.render("NUMBER OF ATTEMPTS:", True, 'WHITE'), (100, 350))
                self.screen.blit(self.font.render(str(get_number_of_attempts(1)), True, 'WHITE'), (320, 350))


            else:
                self.screen.blit(local_game.image, local_game.rect)
                self.screen.blit(about_game.image, about_game.rect)
                self.screen.blit(setting.image, setting.rect)
                self.screen.blit(statistics_game.image, statistics_game.rect)
                self.screen.blit(exit_game.image, exit_game.rect)

            self.clock.tick(self.FPS)
            pygame.display.update()


game = SGAME()
game.menu()

pygame.quit()
sys.exit()
