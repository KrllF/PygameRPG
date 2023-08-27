import sys
import pygame

from menu import *
from config import *
from collision import BLOCK
from player import *
from collision import Spritesheet
from collision import Ground
from enemy import *

pygame.display.set_caption('GAME WITH RPG ELEMENTS')


class SGAME:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet("imagestest/character.png")
        self.terrain_spritesheet = Spritesheet("imagestest/terrain.png")
        self.enemy_spritesheet = Spritesheet("imagestest/enemy.png")

        self.font = pygame.font.SysFont('ariel', 32)

    def create_map(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, (j, i))
                if column == "B":
                    BLOCK(self, (j, i))
                if column == "R":
                    robber(self, (j, i))
                if column == "P":
                    Player(self, (j, i))

    def new_game(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()

        self.create_map()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

    def update(self):
        self.all_sprites.update()
        pygame.display.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)

    def main(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def menu(self):
        local_game = Menu_button((415, 50), 250, 100, BLACK, WHITE, 'Local play', 32, 2)
        about_game = Menu_button((415, 200), 250, 100, BLACK, WHITE, 'About game', 32, 2)
        setting = Menu_button((415, 350), 250, 100, BLACK, WHITE, 'Setting', 32, 2)
        exit_game = Menu_button((415, 500), 250, 100, BLACK, WHITE, 'Exit', 32, 2)
        back = Menu_button((415, 500), 250, 100, BLACK, WHITE, 'Back', 32, 2)
        intro = True
        about_game_bool = False
        setting_bool = False
        while intro:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()

            if about_game_bool or setting_bool:
                if back.is_pressed(mouse_pos, events):
                    about_game_bool = False
                    setting_bool = False
            else:
                if local_game.is_pressed(mouse_pos, events):
                    intro = False

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
            elif setting_bool:
                self.screen.blit(back.image, back.rect)
            else:
                self.screen.blit(local_game.image, local_game.rect)
                self.screen.blit(about_game.image, about_game.rect)
                self.screen.blit(setting.image, setting.rect)
                self.screen.blit(exit_game.image, exit_game.rect)

            self.clock.tick(FPS)
            pygame.display.update()


game = SGAME()
game.menu()
game.new_game()

while game.running:
    game.main()
    game.game_over()

pygame.quit()
sys.exit()
