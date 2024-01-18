import pygame
import pygame_gui

from config.logicConfig import Config
from menu.game import game
from menu.menu import main_menu
from menu.option import option

config = Config()
config.config_load()

RES = config.width, config.height

pygame.init()
sc = pygame.display.set_mode(RES)
manager = pygame_gui.UIManager(RES)
clock = pygame.time.Clock()

click = False

main = game(sc, config).main

options = option(sc, config, manager, main).main


while True:
    time_delta = clock.tick(config.fps) / 1000.0
    sc.fill(pygame.Color(config.maincolor))
    click = main_menu(sc, config, click=click, callbacks=[main, options], name=['game', 'option'])
    manager.draw_ui(sc)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        manager.process_events(event)

    manager.update(time_delta)
    pygame.display.update()
    clock.tick(config.fps)
