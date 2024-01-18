import pygame

from config.config import WHITE


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text
        self.size = 30

    def draw(self, screen, fontsize=None, font=None, color=WHITE):
        if fontsize is None:
            fontsize = self.size
        if font is None:
            font = pygame.font.SysFont("Consolas", fontsize)

        text = font.render(self.text, True, color)
        screen.blit(text, (self.x, self.y))

    def draw_center_x(self, screen, fontsize=None, font=None, color=WHITE):
        if fontsize is None:
            fontsize = self.size
        if font is None:
            font = pygame.font.SysFont("Consolas", fontsize)

        text = font.render(self.text, True, color)

        font_size = font.size(self.text)
        draw_x = self.x - font_size[0] / 2
        draw_y = self.y
        screen.blit(text, (draw_x, draw_y))
