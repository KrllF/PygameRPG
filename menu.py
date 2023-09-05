import pygame


class Menu_button:
    def __init__(self, pos, width, height, fg, bg, text, fontsize, func):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.content = text
        self.font = pygame.font.Font('fonts/EightBits.ttf', fontsize)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
                return True
        return False



class Slider:
    def __init__(self, pos, size, initial_val, min, max):
        self.pos = pos
        self.size = size

        self.left_pos = self.pos[0] - (size[0] // 2)
        self.right_pos = self.pos[0] + (size[0] // 2)
        self.top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial_val = (self.right_pos - self.left_pos) * initial_val

        self.container_rect = pygame.Rect(self.left_pos, self.top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.left_pos + self.initial_val - 5, self.top_pos, 10,
                                       self.size[1])
    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]
    def render(self, game):
        pygame.draw.rect(game.screen, "darkgray", self.container_rect)
        pygame.draw.rect(game.screen, "red", self.button_rect)

    def get_value(self):
        val_range = self.right_pos - self.left_pos
        button_val = self.button_rect.centerx - self.left_pos

        return (button_val/val_range) * (self.max - self.min) + self.min

