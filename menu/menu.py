import sys

import pygame

from config.config import WHITE, BLACK
from object.draw.UIElement import UIElement
from object.draw.button import Button


# def main_menu(screen, click=False, callback={}):
def main_menu(screen, config, click=False, callbacks=None, name=None):
    # draw_text('main menu', font, (255, 255, 255), screen, 20, 20)
    x = config.width / 2

    if callbacks is None:
        callbacks = []
    if name is None:
        name = ['']
    UIElement(x, 20, 'main menu').draw_center_x(screen, font=pygame.font.Font('assets/font/emulogic.ttf'))

    mx, my = pygame.mouse.get_pos()
    y = 100
    i = 0

    for callback in callbacks:
        button = Button(x, y, 200, 50, name[i], WHITE, BLACK, size=20, center=True)
        y += 100
        if click:
            if button.click(mx,my):
                callback()
        i += 1
        button.draw(screen)

    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        return click

