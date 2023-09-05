import pygame
from config import *
from database import *


class Weapon_for_players(pygame.sprite.Sprite):
    def __init__(self, game, player, pos):
        self.sword_up_images = [pygame.image.load("images/sword_up.png")]
        self.sword_down_images = [pygame.image.load("images/sword_down.png")]
        self.sword_left_images = [pygame.image.load("images/sword_left.png")]
        self.sword_right_images = [pygame.image.load("images/sword_right.png")]

        self.game = game
        self.player = player
        self._layer = PLAYER_LAYER
        self.loop = 1

        self.groups = self.player.attack, self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = pos[0]
        self.y = pos[1]

        self.image_up = pygame.image.load("images/sword_up.png")
        self.image_down = pygame.image.load("images/sword_down.png")
        self.image_left = pygame.image.load("images/sword_left.png")
        self.image_right = pygame.image.load("images/sword_right.png")
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
        if self.player.view == [0, -1]:  # Вверх
            self.rect.midbottom = self.player.rect.midtop
        elif self.player.view == [0, 1]:  # Вниз
            self.rect.midtop = self.player.rect.midbottom
        elif self.player.view == [1, 0]:  # Вправо
            self.rect.midleft = self.player.rect.midright
        elif self.player.view == [-1, 0]:  # Влево
            self.rect.midright = self.player.rect.midleft

    def collide_with_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for i, enemy in enumerate(hits):
            if enemy not in self.enemies_hit:
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
        self.sword_up_images = [pygame.image.load("images/sword_up.png")]
        self.sword_down_images = [pygame.image.load("images/sword_down.png")]
        self.sword_left_images = [pygame.image.load("images/sword_left.png")]
        self.sword_right_images = [pygame.image.load("images/sword_right.png")]

        self.game = game
        self.robber = robber
        self._layer = PLAYER_LAYER
        self.loop = 1

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = pos[0]
        self.y = pos[1]

        self.image_up = pygame.image.load("images/sword_up.png")
        self.image_down = pygame.image.load("images/sword_down.png")
        self.image_left = pygame.image.load("images/sword_left.png")
        self.image_right = pygame.image.load("images/sword_right.png")
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
                if player.current_hp - self.robber.damage <= 0:
                    player.player_death()
                player.enemy_blinding = True
                player.blinding_time = pygame.time.get_ticks()
                player.current_hp -= self.robber.damage
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
