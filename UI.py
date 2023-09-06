import math

import pygame
from config import *


class User_Interface:
    def __init__(self, player):
        self.player = player
        self.time_now = 0

        self.font = pygame.font.Font('fonts/EightBits.ttf', FONT_SIZE)
        self.last_characteristic = None
        self.upgrade_bool = True
        # bars
        self.exp_bar_back = pygame.Rect(15, 650, BAR_W + 150, BAR_H - 4)

        # upgrade menu
        self.health_image1 = pygame.transform.scale(
            pygame.image.load('images/skill_upgrade/health.jpg').convert_alpha(), (200, 250))
        self.speed_image = pygame.transform.scale(pygame.image.load('images/skill_upgrade/speed.png').convert_alpha(),
                                                  (200, 250))
        self.damage_image = pygame.transform.scale(
            pygame.image.load('images/skill_upgrade/damage.png').convert_alpha(), (200, 250))

        self.health_image_rect = self.health_image1.get_rect(topleft=((self.player.game.w - 600) / 4, 200))
        self.speed_image_rect = self.speed_image.get_rect(topleft=((self.player.game.w - 600) / 2 + 200, 200))
        self.damage_image_rect = self.damage_image.get_rect(topleft=((self.player.game.w - 600) * 3 / 4 + 400, 200))
        self.buttons_upgrade = pygame.sprite.Group()
        self.create_buttons_upgrade()

    def draw_bars_of_characteristics(self):
        # exp

        pygame.draw.rect(self.player.game.screen, 'yellow',
                         (self.player.game.w // 2 - 8, self.player.game.h // 2 - 25, self.player.exp // 2 / (
                                 self.player.characteristics['health'] / self.player.health_bar_length), 5))

        pygame.draw.rect(self.player.game.screen, (255, 255, 255),
                         (self.player.game.w // 2 - 8, self.player.game.h // 2 - 25,
                          self.player.characteristics['health'] / (
                                  self.player.characteristics['health'] / self.player.health_bar_length),
                          5), True)

    def draw_kill_for_session(self):
        self.player.game.screen.blit(self.font.render("KILL: " + str(self.player.kill_for_session), True, 'WHITE'),
                                     ((self.player.game.w - 62) // 2, 50))

    def draw_number_of_enemy(self):
        self.player.game.screen.blit(self.font.render("ENEMIES: " + str(len(self.player.game.enemies)), True, 'WHITE'),
                                     ((self.player.game.w - 104) // 2, 80))

    def draw_leveling_points(self):
        self.player.game.screen.blit(
            self.font.render("LEVELING POINTS: " + str(self.player.leveling_points), True, 'WHITE'),
            ((self.player.game.w - 176) // 2, 110))

    def create_buttons_upgrade(self):
        for i in range(3):
            self.buttons_upgrade.add(Button_and_name(((self.player.game.w - 600) / 4 * (i + 1) + i * 200,
                                                      self.health_image_rect.y + self.health_image_rect.height),
                                                     list(self.player.characteristics.keys())[i]))

    def check_click(self, mouse_pos):
        for button in self.buttons_upgrade:
            if button.rect.collidepoint(mouse_pos) and not button.click:
                self.upgrade_characteristic(button.characteristic_name)
                button.click_time = pygame.time.get_ticks()
                button.click = True
                break

    def timer_upgrade(self):
        pass

    def upgrade_characteristic(self, characteristic_name):
        if self.player.leveling_points > 0:
            self.player.leveling_points -= 1
            self.player.characteristics[characteristic_name] *= 1.20
            self.player.characteristics_level[characteristic_name] += 1

    def draw_upgrade_menu(self):
        for button in self.buttons_upgrade:
            pygame.draw.rect(self.player.game.screen, 'red', button.rect)
            if button.click:
                pygame.draw.rect(self.player.game.screen, 'gold', button.rect, 4)
            else:
                pygame.draw.rect(self.player.game.screen, '#45322E', button.rect, 4)
            self.player.game.screen.blit(button.image, button.rect)

            pygame.draw.rect(self.player.game.screen, (255, 255, 255), button.text_bg_rect)

            pygame.draw.rect(self.player.game.screen, '#45322E', button.text_bg_rect, 4)
            self.player.game.screen.blit(button.name_text, button.text_rect)

        # hp
        pygame.draw.rect(self.player.game.screen, (64, 64, 64), self.health_image_rect)
        pygame.draw.rect(self.player.game.screen, '#AE6524', self.health_image_rect, 4)
        self.player.game.screen.blit(self.health_image1, self.health_image_rect)

        self.player.game.screen.blit(self.font.render(str(self.player.characteristics_level['health']), True, 'BLACK'),
                                     ((self.player.game.w - 600) / 4 + 95, self.health_image_rect.y + self.health_image_rect.height + 45))
        # speed
        pygame.draw.rect(self.player.game.screen, (64, 64, 64), self.speed_image_rect)
        pygame.draw.rect(self.player.game.screen, '#AE6524', self.speed_image_rect, 4)
        self.player.game.screen.blit(self.speed_image, self.speed_image_rect)

        self.player.game.screen.blit(self.font.render(str(self.player.characteristics_level['speed']), True, 'BLACK'),
                                     ((self.player.game.w - 600) / 2 + 295, self.health_image_rect.y + self.health_image_rect.height + 45))

        #damage
        pygame.draw.rect(self.player.game.screen, (64, 64, 64), self.damage_image_rect)
        pygame.draw.rect(self.player.game.screen, '#AE6524', self.damage_image_rect, 4)
        self.player.game.screen.blit(self.damage_image, self.damage_image_rect)

        self.player.game.screen.blit(self.font.render(str(self.player.characteristics_level['damage']), True, 'BLACK'),
                                     ((self.player.game.w - 600) * 3 / 4 + 495, self.health_image_rect.y + self.health_image_rect.height + 45))

        self.buttons_upgrade.update()

    def draw_ui(self):
        self.draw_bars_of_characteristics()
        self.draw_kill_for_session()
        self.draw_number_of_enemy()
        self.draw_leveling_points()


class Button_and_name(pygame.sprite.Sprite):
    def __init__(self, pos, characteristic_name):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            'images/skill_upgrade/button_for_upgrade.png').convert_alpha(),
                                            (200, 150))
        self.rect = self.image.get_rect(topleft=pos)
        self.characteristic_name = characteristic_name
        self.text_bg_rect = pygame.Rect(self.rect.left, self.rect.y - 300, self.rect.width, 50)
        self.font = pygame.font.Font('fonts/EightBits.ttf', FONT_SIZE)
        self.name_text = self.font.render(self.characteristic_name, False, (255, 0, 0))
        self.text_rect = self.name_text.get_rect(center=(self.rect.centerx, self.rect.y - 280))
        self.click = False
        self.click_time = None

    def cooldown(self):
        cur_time = pygame.time.get_ticks()
        if self.click and cur_time - self.click_time >= 100:
            self.click = not self.click

    def update(self):
        self.cooldown()
