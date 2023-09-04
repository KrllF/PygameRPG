import math
import pygame

from config import *
from weapon import Weapon_for_players
from UI import User_Interface
from database import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.oldX = None
        self.oldY = None
        self.loop = 1
        self.game = game
        self._layer = PLAYER_LAYER

        self.player_blinding = False
        self.blinding_time = -10000

        # hp
        self.health = start_hp_player
        self.current_hp = start_hp_player
        self.health_bar_length = 32

        self.attack = pygame.sprite.LayeredUpdates()
        self.can_attack = True
        self.attack_time = 0

        self.groups = self.game.all_sprites, self.game.players
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = pos[0] * TILESIZE
        self.y = pos[1] * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.character_spritesheet.get_sprite((0, 0), self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.direction = [0, 0]
        self.view = [0, 0]

        # player characteristics
        self.level = 0
        self.leveling_points = 0
        self.exp = start_exp_player
        self.speed = start_speed_player
        self.exp = start_exp_player
        self.stamina = 1001
        self.damage = start_damage_player

        self.health_level = 1
        self.speed_level = 1
        self.damage_level = 1

        self.characteristics = {'health': self.health, 'speed': self.speed, 'damage': self.damage,
                                'exp': self.exp}
        self.characteristics_level = {'health': self.health_level, 'speed': self.speed_level,
                                      'damage': self.damage_level}

        self.upgrade_menu_open = False
        self.ui = User_Interface(self)

        self.kill_for_session = 0
        self.life_time = 0

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()

        if pygame.time.get_ticks() - self.blinding_time > blindtime:
            self.player_blinding = False
            if keys[pygame.K_w]:
                self.direction[1] = -1
                self.view[0] = 0
                self.view[1] = -1
            elif keys[pygame.K_s]:
                self.direction[1] = 1
                self.view[0] = 0
                self.view[1] = 1
            else:
                self.direction[1] = 0

            if keys[pygame.K_d]:
                self.direction[0] = 1
                self.view[0] = 1
                self.view[1] = 0
            elif keys[pygame.K_a]:
                self.direction[0] = -1
                self.view[0] = -1
                self.view[1] = 0
            else:
                self.direction[0] = 0

            if keys[pygame.K_j]:
                self.upgrade_menu_open = True
                self.ui.draw_upgrade_menu()
                if mouse_pressed[0]:
                    self.ui.check_click(pygame.mouse.get_pos())

            if keys[pygame.K_SPACE]:
                if self.attack_checker():
                    self.attack_time = pygame.time.get_ticks()
                    Weapon_for_players(self.game, self, (self.x, self.y))
                    self.can_attack = False
        else:
            self.direction = [0, 0]

    def player_animation(self):
        down_animations = [self.game.character_spritesheet.get_sprite((3, 2), self.width, self.height),
                           self.game.character_spritesheet.get_sprite((35, 2), self.width, self.height),
                           self.game.character_spritesheet.get_sprite((68, 2), self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite((3, 34), self.width, self.height),
                         self.game.character_spritesheet.get_sprite((35, 34), self.width, self.height),
                         self.game.character_spritesheet.get_sprite((68, 34), self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite((3, 98), self.width, self.height),
                           self.game.character_spritesheet.get_sprite((35, 98), self.width, self.height),
                           self.game.character_spritesheet.get_sprite((68, 98), self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite((3, 66), self.width, self.height),
                            self.game.character_spritesheet.get_sprite((35, 66), self.width, self.height),
                            self.game.character_spritesheet.get_sprite((68, 66), self.width, self.height)]

        if self.view[0] == 0 and self.view[1] == 0:
            self.image = self.game.character_spritesheet.get_sprite((3, 2), self.width, self.height)

        if self.view[0] == 0 and self.view[1] == 1 and (self.direction[0] != 0 or self.direction[1] != 0):
            self.image = down_animations[0]
            while self.loop < 3:
                self.image = down_animations[math.floor(self.loop)]
                self.loop += 0.1
            self.loop = 1

        if self.view[0] == 0 and self.view[1] == -1 and (self.direction[0] != 0 or self.direction[1] != 0):
            self.image = up_animations[0]
            while self.loop < 3:
                self.image = up_animations[math.floor(self.loop)]
                self.loop += 0.1
            self.loop = 1

        if self.view[0] == 1 and self.view[1] == 0 and (self.direction[0] != 0 or self.direction[1] != 0):
            self.image = right_animations[0]
            while self.loop < 3:
                self.image = right_animations[math.floor(self.loop)]
                self.loop += 0.1
            self.loop = 1

        if self.view[0] == -1 and self.view[1] == 0 and (self.direction[0] != 0 or self.direction[1] != 0):
            self.image = left_animations[0]
            while self.loop < 3:
                self.image = left_animations[math.floor(self.loop)]
                self.loop += 0.1
            self.loop = 1

        if self.view[0] == 0 and self.view[1] == 1 and (self.direction[0] == 0 and self.direction[1] == 0):
            self.image = self.game.character_spritesheet.get_sprite((3, 2), self.width, self.height)

        if self.view[0] == 0 and self.view[1] == -1 and (self.direction[0] == 0 and self.direction[1] == 0):
            self.image = up_animations[0]

        if self.view[0] == 1 and self.view[1] == 0 and (self.direction[0] == 0 and self.direction[1] == 0):
            self.image = right_animations[0]

        if self.view[0] == -1 and self.view[1] == 0 and (self.direction[0] == 0 and self.direction[1] == 0):
            self.image = left_animations[0]

    def attack_checker(self):
        if pygame.time.get_ticks() - self.attack_time > player_weapon_cooldown:
            self.can_attack = True
            return True
        else:
            self.can_attack = False
            return False

    def player_collide_with_blocks(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if not hits:
            self.oldX = self.rect.centerx
            self.oldY = self.rect.centery
            self.rect.centerx += self.direction[0] * self.speed
            self.rect.centery += self.direction[1] * self.speed
            if pygame.sprite.spritecollide(self, self.game.blocks, False):
                self.rect.centerx = self.oldX
                self.rect.centery = self.oldY

    def player_collide_with_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if not hits:
            self.oldX = self.rect.centerx
            self.oldY = self.rect.centery
        if hits:
            self.rect.centerx = self.oldX
            self.rect.centery = self.oldY

    def player_death(self):
        if self.current_hp <= 0:
            self.life_time = pygame.time.get_ticks() // 1000
            update_play_time(1, self.life_time)
            self.game.game_over_bool = True
            self.kill()

    def update_level(self):
        if self.exp >= 200:
            self.exp -= 200
            self.leveling_points += 1
            self.level += 1

    def health_bar(self):
        pygame.draw.rect(self.game.screen, (255, 0, 0),
                         (self.rect.topleft[0], self.rect.topleft[1] - 5,
                          self.current_hp / (self.characteristics['health'] / self.health_bar_length), 5))
        pygame.draw.rect(self.game.screen, (255, 255, 255),
                         (self.rect.topleft[0], self.rect.topleft[1] - 5,
                          self.characteristics['health'] / (self.characteristics['health'] / self.health_bar_length),
                          5), True)

    def regeneration(self):
        if self.current_hp < self.characteristics['health']:
            self.current_hp += 0.001 * self.characteristics['health']
        if self.current_hp > self.characteristics['health']:
            self.current_hp = self.characteristics['health']

    def draw_level(self):
        level_text = self.game.font.render(str(self.level), False, 1)
        self.game.screen.blit(level_text, (self.rect.topleft[0] - 13, self.rect.topleft[1] - 23))

    def update(self):
        self.draw_level()
        self.regeneration()
        self.update_level()
        self.ui.draw_ui()
        self.health_bar()
        self.player_death()
        self.input()
        self.player_collide_with_blocks()
        self.player_animation()
