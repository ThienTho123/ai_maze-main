import copy
import time

import pygame
from Algorithm.BFSsolve import bfs
from Algorithm.DFSsovle import dfs
from Algorithm.astarSolve import a_star
from Algorithm.dfsMapGeneration import DFSMAPGen
from Algorithm.greedySolve import greedy
from Algorithm.hillClimbSolve import hill_climbing
from Algorithm.idSolve import ids
from Algorithm.uscSolve import ucs
from config.config import WHITE, BLACK, BLUE
from object.draw.UIElement import UIElement
from object.draw.button import Button
from object.gameplay.Cell import Cell


class game:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.clock = pygame.time.Clock()
        self.running = False
        # self.previous_choice = ""
        self.start_autoplay = False
        self.path = []
        self.start_game = False
        self.start_reset = False
        self.algorithm = 'player'
        self.start_timer = False
        self.elapsed_time = 0
        # # self.high_score = float(self.get_high_scores()[0])
        self.size = int(self.config.width // self.config.cellsize), int(self.config.height // self.config.cellsize)
        self.config.cellsize = self.config.cellsize_ratio(0.75)
        self.grid_cells = self.create()
        self.current_cell = self.grid_cells[0]
        self.complete_cell = self.grid_cells[-1]
        self.colors, self.color = [], 40
        self.map = DFSMAPGen(self.grid_cells, self.config)
        # cols, rows = self.size
        self.start_grid = copy.deepcopy(self.grid_cells)
        self.start_replay = False
        self.make_map = False
        self.mouser_down = False
        self.algorithms = ['DFS', 'Greedy', 'BFS', 'Astar', 'UCS', 'Hill', 'IDS', 'player']
        self.time_of_algorithm = [0, 0, 0, 0, 0, 0, 0, 0]
        self.visited = [0, 0, 0, 0, 0, 0, 0, 0]
        self.move_step = [0, 0, 0, 0, 0, 0, 0, 0]
        self.is_completed = False
        self.changed = []

    # def get_high_scores(self):
    #     with open("high_score.txt", "r") as file:
    #         scores = file.read().splitlines()
    #     return scores

    # def save_score(self):
    #     with open("high_score.txt", "w") as file:
    #         file.write(str("%.3f\n" % self.high_score))
    #
    # def time(self):
    #     pass
    def initsetup(self):
        self.path = []
        self.start_game = False
        self.start_autoplay = False
        self.start_replay = False
        self.start_timer = False
        self.make_map = False
        self.current_cell = self.grid_cells[0]
        self.complete_cell = self.grid_cells[-1]
        self.map = DFSMAPGen(self.grid_cells, self.config)
        self.directions = {'a': 'left', 'd': 'right', 'w': 'top', 's': 'bottom'}
        self.keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
        self.is_completed = False
        self.mouser_down = False
        self.reset_map = False
        self.changed = []

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        pygame.display.set_caption('MAZE - game')
        self.time_of_algorithm = [0, 0, 0, 0, 0, 0, 0, 0]
        self.visited = [0, 0, 0, 0, 0, 0, 0, 0]
        self.move_step = [0, 0, 0, 0, 0, 0, 0, 0]
        self.elapsed_time = 0
        self.algorithm = 'player'
        self.initsetup()
        self.buttons_list = []
        self.draw_x, self.draw_y = self.size[0] * self.config.cellsize, self.size[1] * self.config.cellsize + 30
        self.right_menu_center_x = (self.config.width - self.draw_x) / 2 + self.draw_x
        self.buttons_list.append(
            Button(self.right_menu_center_x, self.draw_y * 0.4, 100, 25, "create map", WHITE, BLACK, size=15,
                   center=True))
        self.buttons_list.append(
            Button(self.right_menu_center_x, self.draw_y * 0.5, 100, 25, "Reset", WHITE, BLACK, size=15, center=True))
        self.buttons_list.append(
            Button(self.right_menu_center_x, self.draw_y * 0.6, 100, 25, "Replay", WHITE, BLACK, size=15, center=True))
        self.buttons_list.append(
            Button(self.right_menu_center_x, self.draw_y * 0.7, 100, 25, "Play", WHITE, BLACK, size=15, center=True))
        self.algorithm_button_list = [Button(100 + 100 * i, self.draw_y, 75, 25, algorithm, WHITE, BLACK, size=20) for
                                      i, algorithm in enumerate(self.algorithms)]
        # self.algorithm_button_list.append(Button(50, self.draw_y, 75, 25, "DFS", WHITE, BLACK, size=20))
        # self.algorithm_button_list.append(Button(150, self.draw_y, 75, 25, "Greedy", WHITE, BLACK, size=20))
        # self.algorithm_button_list.append(Button(250, self.draw_y, 75, 25, "BFS", WHITE, BLACK, size=20))
        # self.algorithm_button_list.append(Button(350, self.draw_y, 75, 25, "Astar", WHITE, BLACK, size=20))
        # self.algorithm_button_list.append(Button(450, self.draw_y, 75, 25, "UCS", WHITE, BLACK, size=20))
        # self.algorithm_button_list.append(Button(550, self.draw_y, 75, 25, "Hill", WHITE, BLACK, size=20))
        # self.algorithm_button_list.append(Button(650, self.draw_y, 75, 25, "IDS", WHITE, BLACK, size=20))

        self.path = []
        self.draw()
        self.create_map()

    def create(self):
        print('create')
        return [Cell(col, row, map_size=self.size, config=self.config) for row in range(self.size[1]) for col in
                range(self.size[0])]

    def create_map(self):
        isBreak = False
        while not isBreak:
            [cell.draw(self.screen) for cell in self.grid_cells]
            self.current_cell, isBreak = self.map.draw_maze(self.screen, self.current_cell, isBreak)
            # self.clock.tick(self.config.fps)
            pygame.display.update()
        self.start_grid = copy.deepcopy(self.grid_cells)

    def reset_visited(self):
        for cell in self.grid_cells:
            cell.visited = False

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(self.config.fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        if self.start_game:
            if self.current_cell == self.complete_cell:
                self.start_game = False
                self.is_completed = True
            #         if self.high_score > 0:
            #             self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
            #         else:
            #             self.high_score = self.elapsed_time
            #         self.save_score()
            #
            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer
        #
        # if self.start_shuffle:
        #     self.shuffle()
        #     self.draw_tiles()
        #     self.shuffle_time += 1
        #     if self.shuffle_time > 120:
        #         self.start_shuffle = False
        #         self.start_game = True
        #         self.start_timer = True

        if self.start_autoplay:
            self.reset_visited()
            self.draw()
            if self.autoplay():
                self.start_autoplay = False
        if self.start_reset:
            if self.reset():
                self.start_reset = False
        if self.start_replay:
            if self.replay():
                self.start_replay = False
        if self.make_map:
            self.make_map_handler()


    def draw(self):
        self.all_sprites.draw(self.screen)
        self.screen.fill(pygame.Color(self.config.maincolor))
        self.draw_grid()
        self.current_cell.draw_current_cell(self.screen)
        self.complete_cell.draw_current_cell(self.screen, BLUE)

        # UI text
        UIElement(self.right_menu_center_x, self.draw_y * 0.08, 'MAZE').draw_center_x(self.screen)
        UIElement(self.right_menu_center_x, self.draw_y * 0.2, "%.3f" % self.elapsed_time).draw_center_x(self.screen)

        # button right menu
        for button in self.buttons_list:
            button.draw(self.screen)

        # algorithm UI
        UIElement(5, self.draw_y + 5, "Algorithm:").draw(
            self.screen, fontsize=15)
        UIElement(5, self.draw_y + 35, "Time solve:").draw(
            self.screen, fontsize=15)
        UIElement(5, self.draw_y + 60, "Visited:").draw(
            self.screen, fontsize=15)
        UIElement(5, self.draw_y + 85, "Move Step:").draw(
            self.screen, fontsize=15)

        # button
        for i, button in enumerate(self.algorithm_button_list):
            button.draw(self.screen)

            # Time solver
            UIElement(button.center_pos_x, self.draw_y + 35, "%.3f" % self.time_of_algorithm[i]).draw_center_x(
                self.screen, fontsize=15)

            # Visited
            UIElement(button.center_pos_x, self.draw_y + 60, "%.3f" % self.visited[i]).draw_center_x(
                self.screen, fontsize=15)

            # Move Step
            UIElement(button.center_pos_x, self.draw_y + 85, "%.3f" % self.move_step[i]).draw_center_x(
                self.screen, fontsize=15)

        if self.current_cell == self.complete_cell:
            if len(self.path) > 0:
                for i in self.path:
                    self.colors.append((min(self.color, 255), 10, 100))
                    self.color += 1
                [pygame.draw.rect(self.screen, self.colors[i],
                                  (cell.x * self.config.cellsize + 5, cell.y * self.config.cellsize + 5,
                                   self.config.cellsize - 10, self.config.cellsize - 10),
                                  border_radius=8) for i, cell in enumerate(self.path)]
        # if self.algorithm == 'BFS':
        #     self.time_of_algorithm[2] = self.elapsed_time
        # if self.algorithm == 'Greedy':
        #     self.time_of_algorithm[1] = self.elapsed_time
        # if self.algorithm == 'DFS':
        #     self.time_of_algorithm[0] = self.elapsed_time
        # if self.algorithm == 'Astar':
        #     self.time_of_algorithm[3] = self.elapsed_time
        # if self.algorithm == 'UCS':
        #     self.time_of_algorithm[4] = self.elapsed_time
        # if self.algorithm == 'Hill':
        #     self.time_of_algorithm[5] = self.elapsed_time
        # if self.algorithm == 'IDS':
        #     self.time_of_algorithm[6] = self.elapsed_time
        self.time_of_algorithm[self.algorithms.index(self.algorithm)] = self.elapsed_time

        pygame.display.update()

    def draw_grid(self):
        [cell.draw(self.screen) for cell in self.grid_cells]
        # pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keyup = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                pressed_key = pygame.key.get_pressed()
                for key, key_value in self.keys.items():
                    if pressed_key[key_value] and keyup and not self.is_completed:
                        if not self.start_game:
                            self.algorithm = 'player'
                            self.start_game = True
                            self.start_timer = True
                            self.move_step[-1] = self.visited[-1] = 1
                        keyup = False
                        if self.directions[key] in self.current_cell.possible_move(self.grid_cells):
                            self.visited[-1] += 1
                            self.move_step[-1] = self.visited[-1]
                            self.current_cell = self.current_cell.possible_move(self.grid_cells)[self.directions[key]]
            if event.type == pygame.KEYUP:
                keyup = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.mouser_down = True

                for button in self.buttons_list + self.algorithm_button_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text in self.algorithms:
                            self.algorithm = button.text
                            self.start_autoplay = True
                            self.start_game = True
                            self.start_timer = True
                        # if button.text == "BFS":
                        #     self.algorithm = 'BFS'
                        #     self.start_autoplay = True
                        #     self.start_game = True
                        #     self.start_timer = True
                        # if button.text == "Greedy":
                        #     self.algorithm = 'Greedy'
                        #     self.start_autoplay = True
                        #     self.start_game = True
                        #     self.start_timer = True
                        # if button.text == "DFS":
                        #     self.algorithm = 'DFS'
                        #     self.start_autoplay = True
                        #     self.start_game = True
                        #     self.start_timer = True
                        # if button.text == "Astar":
                        #     self.algorithm = 'Astar'
                        #     self.start_autoplay = True
                        #     self.start_game = True
                        #     self.start_timer = True
                        # if button.text == "UCS":
                        #     self.algorithm = 'UCS'
                        #     self.start_autoplay = True
                        #     self.start_game = True
                        #     self.start_timer = True
                        # if button.text == "Hill":
                        #     self.algorithm = 'Hill'
                        #     self.start_autoplay = True
                        #     self.start_game = True
                        #     self.start_timer = True
                        # if button.text == "IDS":
                        #     self.algorithm = 'IDS'
                        #     self.start_autoplay = True
                        #     self.start_game = True
                        #     self.start_timer = True

                        if button.text == "create map":
                            self.make_map = True
                            self.reset_map = True
                        if button.text == "save":
                            self.make_map = False
                            self.start_grid = copy.deepcopy(self.grid_cells)
                            self.start_replay = True
                            self.buttons_list.pop()
                        if button.text == "Reset":
                            self.start_reset = True
                        if button.text == "Replay":
                            self.start_replay = True
                        if button.text == "Play":
                            self.start_game = True
                            self.start_timer = True

                #                 if button.text == "BFS":
                #                     self.autoplay(0)
                #                     self.start_autoplay = True
                #                 if button.text == "DFS":
                #                     self.autoplay(1)
                #                     self.start_autoplay = True
                #                 if button.text == "UCS":
                #                     self.autoplay(2)
                #                     self.start_autoplay = True
                #                 if button.text == "Astar":
                #                     self.autoplay(3)
                #                     self.start_autoplay = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouser_down = False
                self.changed = []

            # if self.change_delay <= 10:
            #     self.change_delay += 1
            # else:
            #     self.change_delay = 0
            if self.make_map and self.mouser_down:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print('make')
                find_cell = lambda mouse_x, mouse_y: (
                    mouse_x // self.config.cellsize, mouse_y // self.config.cellsize,
                    mouse_x / self.config.cellsize - mouse_x // self.config.cellsize,
                    mouse_y / self.config.cellsize - mouse_y // self.config.cellsize)
                print(find_cell(mouse_x, mouse_y)[0:2])
                for cell in self.grid_cells:
                    if find_cell(mouse_x, mouse_y)[0:2] not in self.changed:
                        isclick, self.changed = cell.click(find_cell(mouse_x, mouse_y), wall_remove=True,
                                                           grid_cells=self.grid_cells)

    def autoplay(self):
        self.start_autoplay = False
        # 'DFS', 'Greedy', 'BFS', 'Astar', 'UCS', 'Hill', 'IDS'
        funcs = [dfs, greedy, bfs, a_star, ucs, hill_climbing, ids]

        def callback(func_i, maze, start, goal, sc, config=None):
            self.path = funcs[func_i](maze, start, goal, sc, config=None)
            if self.path is None:
                self.path = []
            else:
                if self.path[-1] != self.complete_cell:
                    self.path.append(self.complete_cell)
            self.visited[func_i] = self.visited_counter()
            self.move_step[func_i] = len(self.path)

        callback(self.algorithms.index(self.algorithm), self.grid_cells, self.current_cell, self.complete_cell,
                 self.screen, self.config)

        # if self.algorithm == 'BFS':
        #     self.path = bfs(self.grid_cells, self.current_cell, self.complete_cell, self.screen, self.config)
        # if self.algorithm == 'Greedy':
        #     self.path = greedy(self.grid_cells, self.current_cell, self.complete_cell, self.screen, self.config)
        # if self.algorithm == 'DFS':
        #     self.path = dfs(self.grid_cells, self.current_cell, self.complete_cell, self.screen, self.config)
        # if self.algorithm == 'Astar':
        #     self.path = a_star(self.grid_cells, self.current_cell, self.complete_cell, self.screen, self.config)
        # if self.algorithm == 'UCS':
        #     self.path = ucs(self.grid_cells, self.current_cell, self.complete_cell, self.screen, self.config)
        # if self.algorithm == 'Hill':
        #     self.path = hill_climbing(self.grid_cells, self.current_cell, self.complete_cell, self.screen, self.config)
        # if self.algorithm == 'IDS':
        #     self.path = ids(self.grid_cells, self.current_cell, self.complete_cell, self.screen, self.config)

        self.current_cell = self.complete_cell

    def reset(self):
        self.start_reset = False
        self.grid_cells = self.create()
        self.draw()
        self.new()

    def replay(self):
        self.start_replay = False
        self.grid_cells = self.start_grid
        self.set_visited()
        self.draw()
        self.initsetup()

    def main(self):
        self.screen.fill(pygame.Color(self.config.maincolor))
        self.running = True
        while self.running:
            # UIElement(cols * self.config.cellsize + 60, rows * self.config.cellsize * 0.08,'MAZE').draw(self.screen)

            self.new()
            self.run()
            self.clock.tick(self.config.fps)
            pygame.display.update()

    def visited_counter(self):
        counter = 1
        for cell in self.grid_cells:
            if cell.visited:
                counter += 1
        return counter

    def set_visited(self):
        for cell in self.grid_cells:
            cell.visited = True

    def make_map_handler(self):
        if self.reset_map:
            self.buttons_list.append(
                Button(self.right_menu_center_x, self.draw_y * 0.85, 100, 25, "save", WHITE, BLACK, size=15,
                       center=True))
            self.grid_cells = self.create()
            self.reset_map = False
