import sys
import pygame

from config import *
from collision import BLOCK
from player import *
from collision import Spritesheet
from collision import Ground
from enemy import *


class SGAME:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet("imagestest/character.png")
        self.terrain_spritesheet = Spritesheet("imagestest/terrain.png")
        self.enemy_spritesheet = Spritesheet("imagestest/enemy.png")

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
        pass


game = SGAME()
game.menu()
game.new_game()

while game.running:
    game.main()
    game.game_over()

pygame.quit()
sys.exit()
