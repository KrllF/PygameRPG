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
        self.font = pygame.font.SysFont('arial', fontsize)

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

