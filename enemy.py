import pygame
import math
import random

from config import *
from weapon import Weapon_for_enemyis


class robber(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.game = game
        self._layer = ENEMY_LAYER

        self.loop = 1
        self.cooldown_check = False
        #hp
        self.maximum_hp = robber_hp
        self.current_hp = robber_hp
        self.health_bar_length = 32
        self.health_ratio = self.maximum_hp / self.health_bar_length


        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = pos[0] * TILESIZE
        self.y = pos[1] * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.enemy_spritesheet.get_sprite((0, 0), self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.enemy_blinding = False
        self.blinding_time = -10000

        self.attack = pygame.sprite.LayeredUpdates()
        self.can_attack = False
        self.damage = 20
        self.attack_time = 0

        self.direction = [0, 0]
        self.view = [0, 0]
        self.direction_vector = [0, 0]

        self.speed = random.uniform(1, 2)

    def robber_animation(self):
        down_animations = [self.game.enemy_spritesheet.get_sprite((3, 2), self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite((35, 2), self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite((68, 2), self.width, self.height)]

        up_animations = [self.game.enemy_spritesheet.get_sprite((3, 34), self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite((35, 34), self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite((68, 34), self.width, self.height)]

        left_animations = [self.game.enemy_spritesheet.get_sprite((3, 98), self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite((35, 98), self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite((68, 98), self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite((3, 66), self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite((35, 66), self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite((68, 66), self.width, self.height)]

        if self.view[0] == 0 and self.view[1] == 0:
            self.image = self.game.enemy_spritesheet.get_sprite((3, 2), self.width, self.height)

        if self.view[0] == 0 and self.view[1] == 1:
            self.image = down_animations[0]
            while self.loop < 3:
                self.image = down_animations[math.floor(self.loop)]
                self.loop += 0.1
            self.loop = 1

        if self.view[0] == 0 and self.view[1] == -1:
            self.image = up_animations[0]
            while self.loop < 3:
                self.image = up_animations[math.floor(self.loop)]
                self.loop += 0.1
            self.loop = 1

        if self.view[0] == 1 and self.view[1] == 0:
            self.image = right_animations[0]
            while self.loop < 3:
                self.image = right_animations[math.floor(self.loop)]
                self.loop += 0.1
            self.loop = 1

        if self.view[0] == -1 and self.view[1] == 0:
            self.image = left_animations[0]
            while self.loop < 3:
                self.image = left_animations[math.floor(self.loop)]
                self.loop += 0.1
            self.loop = 1

        if self.view[0] == 0 and self.view[1] == 1 and (
                self.direction_vector[0] == 0 and self.direction_vector[1] == 0):
            self.image = self.game.enemy_spritesheet.get_sprite((3, 2), self.width, self.height)

        if self.view[0] == 0 and self.view[1] == -1 and (
                self.direction_vector[0] == 0 and self.direction_vector[1] == 0):
            self.image = up_animations[0]

        if self.view[0] == 1 and self.view[1] == 0 and (
                self.direction_vector[0] == 0 and self.direction_vector[1] == 0):
            self.image = right_animations[0]

        if self.view[0] == -1 and self.view[1] == 0 and (
                self.direction_vector[0] == 0 and self.direction_vector[1] == 0):
            self.image = left_animations[0]

    def field_of_vision(self, player):
        distance = math.sqrt(
            (player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.rect.centery) ** 2)
        if distance < 4 * TILESIZE:
            return True
        else:
            return False

    def attack_checker(self):
        if pygame.time.get_ticks() - self.attack_time > enemy_weapon_cooldown:
            self.can_attack = True
            return True
        else:
            self.can_attack = False
            return False

    def robber_movements(self):
        if pygame.time.get_ticks() - self.blinding_time > 1500:
            self.blinding_time = False
            self.cooldown_check = False
            for player in self.game.players:
                dist = math.sqrt(
                    (player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.rect.centery) ** 2)
                if self.field_of_vision(player):
                    self.direction_vector = [player.rect.centerx - self.rect.centerx,
                                             player.rect.centery - self.rect.centery]
                else:
                    self.direction_vector = [0, 0]

                length = math.sqrt(self.direction_vector[0] ** 2 + self.direction_vector[1] ** 2)
                if length != 0:
                    self.direction_vector[0] /= length
                    self.direction_vector[1] /= length
                    self.view[0] = round(self.direction_vector[0])
                    self.view[1] = round(self.direction_vector[1])
                    self.direction_vector[0] = round(self.direction_vector[0], 1)
                    self.direction_vector[1] = round(self.direction_vector[1], 1)
                if dist > TILESIZE:
                    self.rect.centerx += self.direction_vector[0] * self.speed
                    self.rect.centery += self.direction_vector[1] * self.speed
                else:
                    if self.attack_checker():
                        self.attack_time = pygame.time.get_ticks()
                        Weapon_for_enemyis(self.game, self, (self.x, self.y))

        else:
            self.view = [0, 0]
            self.cooldown_check = True
            self.direction_vector = [0, 0]

    def robber_collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for collided_sprite in hits:
            if collided_sprite == self:
                hits.remove(collided_sprite)

        if not hits:
            self.oldX = self.rect.centerx
            self.oldY = self.rect.centery
        if hits:
            self.rect.centerx = self.oldX
            self.rect.centery = self.oldY

    def robber_death(self):
        if self.current_hp <= 0:
            self.kill()

    def health_bar(self):
        pygame.draw.rect(self.game.screen, (255, 51, 153),
                         (self.rect.topleft[0], self.rect.topleft[1] - 5, self.current_hp / self.health_ratio, 5))
        pygame.draw.rect(self.game.screen, (255, 255, 255),
                         (self.rect.topleft[0], self.rect.topleft[1] - 5, self.maximum_hp / self.health_ratio, 5), True)

    def update(self):
        self.health_bar()

        self.robber_death()
        self.robber_movements()
        self.robber_animation()
