import pygame


class Button:
    def __init__(self, x, y, width, height, text, colour, text_colour, font=None, size=None, center=False):
        self.colour, self.text_colour = colour, text_colour
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.center_pos_x = self.x + self.width/2
        if center:
            self.x -= (self.width / 2)
            self.center_pos_x = self.x
        self.text = text
        if size is None: size = 30
        if font is None:
            self.font = pygame.font.SysFont("Consolas", size)


    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, True, self.text_colour)
        self.font_size = self.font.size(self.text)
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))


    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
