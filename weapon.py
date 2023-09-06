import pygame
from config import *
from database import *
from random import randint


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

        self.image_up = pygame.image.load("images/sword_for_player/sword_up.png")
        self.image_down = pygame.image.load("images/sword_for_player/sword_down.png")
        self.image_left = pygame.image.load("images/sword_for_player/sword_left.png")
        self.image_right = pygame.image.load("images/sword_for_player/sword_right.png")
        self.image = self.image_down
        self.rect = self.image.get_rect(center=player.rect.center)

        self.enemies_hit = set()

        self.animation_frames = {
            (0, -1): self.image_up,
            (1, -1): self.image_up,
            (-1, 1): self.image_down,
            (0, 1): self.image_down,
            (1, 0): self.image_right,
            (1, 1): self.image_right,
            (-1, -1): self.image_left,
            (-1, 0): self.image_left
        }
        self.animation_delay = 10
        self.animation_timer = self.animation_delay
        self.animation_frames_completed = False
        self.damage_bool = False

    def direction(self):
        direction = (self.player.view[0], self.player.view[1])
        if direction in self.animation_frames:
            self.image = self.animation_frames[direction]

    def update_sword_position(self):
        if self.player.view == [0, -1]:
            self.rect.midbottom = self.player.rect.midtop
        elif self.player.view == [0, 1]:
            self.rect.midtop = self.player.rect.midbottom
        elif self.player.view == [1, 0]:
            self.rect.midleft = self.player.rect.midright
        elif self.player.view == [-1, 0]:
            self.rect.midright = self.player.rect.midleft


    def collide_with_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for i, enemy in enumerate(hits):
            if enemy not in self.enemies_hit:
                if type(enemy).__name__ == "robber":
                    if enemy.current_hp - self.player.characteristics['damage'] <= 0:
                        enemy.current_hp -= self.player.characteristics['damage']
                        self.player.exp += randint(80, 100) + self.player.kill_for_session * 25
                        self.player.kill_for_session += 1
                        for enemy in self.game.enemies:
                            if type(enemy).__name__ == "robber":
                                enemy.characteristics['damage'] *= 1.10
                                enemy.characteristics['health'] *= 1.10
                                enemy.characteristics['speed'] *= 1.05
                            else:
                                enemy.characteristics['damage'] *= 1.05
                                enemy.characteristics['health'] *= 1.05
                                enemy.characteristics['speed'] *= 1.01
                    else:
                        enemy.current_hp -= self.player.characteristics['damage']

                if type(enemy).__name__ == "Robber_boss":
                    if enemy.current_hp - self.player.characteristics['damage'] <= 0:
                        enemy.current_hp -= self.player.characteristics['damage']
                        self.player.exp += 300 + self.player.kill_for_session * 25
                        self.player.kill_for_session += 1
                        for enemy in self.game.enemies:
                            if type(enemy).__name__ == "robber":
                                enemy.characteristics['damage'] *= 1.10
                                enemy.characteristics['health'] *= 1.10
                                enemy.characteristics['speed'] *= 1.05
                            else:
                                enemy.characteristics['damage'] *= 1.05
                                enemy.characteristics['health'] *= 1.05
                                enemy.characteristics['speed'] *= 1.01
                    else:
                        enemy.current_hp -= self.player.characteristics['damage']

                enemy.enemy_blinding = True
                enemy.blinding_time = pygame.time.get_ticks()
            self.enemies_hit.add(enemy)

    def update(self):
        self.direction()
        self.update_sword_position()

        self.animation_timer -= 1
        if self.animation_timer <= 0:
            self.animation_timer = self.animation_delay
            self.animation_frames_completed = True

        self.collide_with_enemy()

        if self.animation_frames_completed and self.animation_timer == 0:
            self.animation_frames_completed = True
        elif self.animation_frames_completed:
            self.kill()


# I could inherit, but I wanted to

class Weapon_for_enemyis(Weapon_for_players):
    def __init__(self, game, robber, pos):
        self.game = game
        self.robber = robber
        self._layer = PLAYER_LAYER
        self.loop = 1

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = pos[0]
        self.y = pos[1]

        self.image_up = pygame.image.load("images/sword_for_robber/sword_up_robber.png")
        self.image_down = pygame.image.load("images/sword_for_robber/sword_down_robber.png")
        self.image_left = pygame.image.load("images/sword_for_robber/sword_left_robber.png")
        self.image_right = pygame.image.load("images/sword_for_robber/sword_right_robber.png")
        self.image = self.image_down
        self.rect = self.image.get_rect(center=self.robber.rect.center)

        self.players_hit = set()

        self.animation_frames = {
            (0, -1): self.image_up,
            (1, -1): self.image_up,
            (-1, 1): self.image_down,
            (0, 1): self.image_down,
            (1, 0): self.image_right,
            (1, 1): self.image_right,
            (-1, -1): self.image_left,
            (-1, 0): self.image_left
        }
        self.animation_delay = 10
        self.animation_timer = self.animation_delay
        self.animation_frames_completed = False
        self.damage_bool = False

    def direction(self):
        direction = (self.robber.view[0], self.robber.view[1])
        if direction in self.animation_frames:
            self.image = self.animation_frames[direction]

    def update_sword_position(self):
        if self.robber.view == [0, -1]:
            self.rect.midbottom = self.robber.rect.midtop
        elif self.robber.view == [0, 1]:
            self.rect.midtop = self.robber.rect.midbottom
        elif self.robber.view == [1, 0]:
            self.rect.midleft = self.robber.rect.midright
        elif self.robber.view == [-1, 0]:
            self.rect.midright = self.robber.rect.midleft

    def collide_with_players(self):
        hits = pygame.sprite.spritecollide(self, self.game.players, False)
        for i, player in enumerate(hits):
            if player not in self.players_hit:
                if player.current_hp - self.robber.characteristics['damage'] <= 0:
                    player.player_death()
                player.enemy_blinding = True
                player.blinding_time = pygame.time.get_ticks()
                player.current_hp -= self.robber.characteristics['damage']
                self.players_hit.add(player)

    def update(self):
        self.direction()
        self.update_sword_position()

        self.animation_timer -= 1
        if self.animation_timer <= 0:
            self.animation_timer = self.animation_delay
            self.animation_frames_completed = True

        self.collide_with_players()

        if self.animation_frames_completed and self.animation_timer == 0:
            self.animation_frames_completed = True
        elif self.animation_frames_completed:
            self.kill()

class Weapon_for_enemyis_boss(Weapon_for_enemyis):
    def __init__(self, game, robber, pos):
        self.game = game
        self.robber = robber
        self._layer = PLAYER_LAYER
        self.loop = 1

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = pos[0]
        self.y = pos[1]

        self.image_up = pygame.image.load("images/sword_for_robber_boss/sword_up_robber_boss.png")
        self.image_down = pygame.image.load("images/sword_for_robber_boss/sword_down_robber_boss.png")
        self.image_left = pygame.image.load("images/sword_for_robber_boss/sword_left_robber_boss.png")
        self.image_right = pygame.image.load("images/sword_for_robber_boss/sword_right_robber_boss.png")
        self.image = self.image_down
        self.rect = self.image.get_rect(center=self.robber.rect.center)

        self.players_hit = set()

        self.animation_frames = {
            (0, -1): self.image_up,
            (1, -1): self.image_up,
            (-1, 1): self.image_down,
            (0, 1): self.image_down,
            (1, 0): self.image_right,
            (1, 1): self.image_right,
            (-1, -1): self.image_left,
            (-1, 0): self.image_left
        }
        self.animation_delay = 10
        self.animation_timer = self.animation_delay
        self.animation_frames_completed = False
        self.damage_bool = False