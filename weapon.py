import pygame
from config import *
from database import *


class Weapon_for_players(pygame.sprite.Sprite):
    def __init__(self, game, player, pos):
        self.game = game
        self.player = player
        self._layer = PLAYER_LAYER
        self.loop = 1

        self.groups = self.player.attack, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = pos[0]
        self.y = pos[1]
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect(center=player.rect.center)

    def direction(self):
        if self.player.view[0] == 0 and self.player.view[1] == -1:
            while self.loop <= 5:
                self.rect = self.image.get_rect(midbottom=self.player.rect.midtop)
                self.rect.x = self.x
                self.rect.y = self.y
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.player.view[0] == 0 and self.player.view[1] == 1:
            while self.loop <= 5:
                self.rect = self.image.get_rect(midtop=self.player.rect.midbottom)
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.player.view[0] == 1 and self.player.view[1] == 0:
            while self.loop <= 5:
                self.rect = self.image.get_rect(midleft=self.player.rect.midright)
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.player.view[0] == -1 and self.player.view[1] == 0:
            while self.loop <= 5:
                self.rect = self.image.get_rect(midright=self.player.rect.midleft)
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.player.view[0] == 1 and self.player.view[1] == -1:
            while self.loop <= 5:
                self.rect = self.player.rect.topright
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.player.view[0] == -1 and self.player.view[1] == -1:
            while self.loop <= 5:
                self.rect = self.player.rect.topleft
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.player.view[0] == -1 and self.player.view[1] == 1:
            while self.loop <= 5:
                self.rect = self.player.rect.bottomleft
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.player.view[0] == 1 and self.player.view[1] == 1:
            while self.loop <= 5:
                self.rect = self.player.rect.bottomright
                self.loop += 0.5
            self.loop = 1
            self.kill()

    def collide_with_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits:
            if type(enemy).__name__ == "robber":
                if enemy.current_hp - self.player.damage <= 0:
                    self.player.exp += 50
                    self.player.kill_for_session += 1
                    update_kills(1)
            if type(enemy).__name__ == "Robber_boss":
                if enemy.current_hp - self.player.damage <= 0:
                    self.player.exp += 200
                    self.player.kill_for_session += 1
                    update_kills(1)
            enemy.enemy_blinding = True
            enemy.blinding_time = pygame.time.get_ticks()
            enemy.current_hp -= self.player.characteristics['damage']

    def update(self):
        self.direction()
        self.collide_with_enemy()


class Weapon_for_enemyis(pygame.sprite.Sprite):
    def __init__(self, game, robber, pos):
        self.game = game
        self.robber = robber
        self._layer = ENEMY_LAYER
        self.loop = 1

        self.groups = self.robber.attack, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = pos[0]
        self.y = pos[1]
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=self.robber.rect.center)

    def direction(self):
        if self.robber.view[0] == 0 and self.robber.view[1] == -1:
            while self.loop <= 5:
                self.rect = self.image.get_rect(midbottom=self.robber.rect.midtop)
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.robber.view[0] == 0 and self.robber.view[1] == 1:
            while self.loop <= 5:
                self.rect = self.image.get_rect(midtop=self.robber.rect.midbottom)
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.robber.view[0] == 1 and self.robber.view[1] == 0:
            while self.loop <= 5:
                self.rect = self.image.get_rect(midleft=self.robber.rect.midright)
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.robber.view[0] == -1 and self.robber.view[1] == 0:
            while self.loop <= 5:
                self.rect = self.image.get_rect(midright=self.robber.rect.midleft)
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.robber.view[0] == 1 and self.robber.view[1] == -1:
            while self.loop <= 5:
                self.rect = self.robber.rect.topright
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.robber.view[0] == -1 and self.robber.view[1] == -1:
            while self.loop <= 5:
                self.rect = self.robber.rect.topleft
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.robber.view[0] == -1 and self.robber.view[1] == 1:
            while self.loop <= 5:
                self.rect = self.robber.rect.bottomleft
                self.loop += 0.5
            self.loop = 1
            self.kill()

        if self.robber.view[0] == 1 and self.robber.view[1] == 1:
            while self.loop <= 5:
                self.rect = self.robber.rect.bottomright
                self.loop += 0.5
            self.loop = 1
            self.kill()

    def collide_with_players(self):
        hits = pygame.sprite.spritecollide(self, self.game.players, False)
        for player in hits:
            player.current_hp -= self.robber.damage
            player.player_blinding = True
            player.blinding_time = pygame.time.get_ticks()

    def check_enemy(self):
        if self.robber.current_hp <= 0 and self.robber.cooldown_check == True:
            self.kill()

    def update(self):
        self.check_enemy()
        self.collide_with_players()
        self.direction()
