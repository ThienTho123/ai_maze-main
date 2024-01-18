import pygame
from random import choice

from config.config import STARTCOLOR, VISITEDCOLOR, BORDERCOLOR, CELLCOLOR
from config.logicConfig import Config


class Cell:
    def __init__(self, x, y, map_size=None, config=None):
        if config is None:
            config = Config()
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.size = map_size
        self.visited = False
        self.thickness = 4
        self.cel_size = config.cellsize
        self.cost = 10

    def draw_current_cell(self, sc, color=None):
        if color is None:
            color = STARTCOLOR
        x, y = self.x * self.cel_size, self.y * self.cel_size
        pygame.draw.rect(sc, pygame.Color(color), (x + 2, y + 2, self.cel_size - 2, self.cel_size - 2))

    def draw(self, sc):
        x, y = self.x * self.cel_size, self.y * self.cel_size
        if self.visited:
            pygame.draw.rect(sc, pygame.Color(VISITEDCOLOR), (x + 2, y + 2, self.cel_size - 2, self.cel_size - 2))
        if not self.visited:
            pygame.draw.rect(sc, pygame.Color(CELLCOLOR), (x + 2, y + 2, self.cel_size - 2, self.cel_size - 2))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color(BORDERCOLOR), (x, y), (x + self.cel_size, y), self.thickness)
        else:
            pygame.draw.line(sc, pygame.Color(VISITEDCOLOR), (x, y), (x + self.cel_size, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color(BORDERCOLOR), (x + self.cel_size, y),
                             (x + self.cel_size, y + self.cel_size),
                             self.thickness)
        else:
            pygame.draw.line(sc, pygame.Color(VISITEDCOLOR), (x + self.cel_size, y),
                             (x + self.cel_size, y + self.cel_size),
                             self.thickness)

        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color(BORDERCOLOR), (x + self.cel_size, y + self.cel_size),
                             (x, y + self.cel_size),
                             self.thickness)
        else:
            pygame.draw.line(sc, pygame.Color(VISITEDCOLOR), (x + self.cel_size, y + self.cel_size),
                             (x, y + self.cel_size),
                             self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color(BORDERCOLOR), (x, y + self.cel_size), (x, y), self.thickness)
        else:
            pygame.draw.line(sc, pygame.Color(VISITEDCOLOR), (x, y + self.cel_size), (x, y), self.thickness)

    def possible_move(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = {}
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if not self.walls['top'] and top:
            neighbors['top'] = top
        if not self.walls['right'] and right:
            neighbors['right'] = right
        if not self.walls['bottom'] and bottom:
            neighbors['bottom'] = bottom
        if not self.walls['left'] and left:
            neighbors['left'] = left
        return neighbors

    def check_cell(self, x, y):
        cols, rows = self.size
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return neighbors

    def find_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if left and not left.visited and not self.walls['left']:
            neighbors.append(left)
        if right and not right.visited and not self.walls['right']:
            neighbors.append(right)
        if top and not top.visited and not self.walls['top']:
            neighbors.append(top)
        if bottom and not bottom.visited and not self.walls['bottom']:
            neighbors.append(bottom)

        return neighbors

    def click(self, pos_cell, wall_remove=False, grid_cells=None):
        self.grid_cells = grid_cells
        x, y, px_cell, py_cell = pos_cell
        # print(str(self.x) + ' ' + str(self.x + self.cel_size) + ' ' + str(self.y) + ' ' + str(self.y + self.cel_size))
        # print(str(mouse_x), mouse_y)
        # is_click = self.x <= mouse_x/self.cel_size <= self.x + self.cel_size and self.y <= mouse_y/self.cel_size <= self.y + self.cel_size
        is_click = self.x == x and self.y == y
        if is_click:
            print('clicked', self.x, self.y)
            # top = left = right = bottom = False
            top = self.check_cell(self.x, self.y - 1)
            right = self.check_cell(self.x + 1, self.y)
            bottom = self.check_cell(self.x, self.y + 1)
            left = self.check_cell(self.x - 1, self.y)
            change = []
            if wall_remove and is_click:
                if 0 < px_cell < 0.2 and left:
                    print('click left')
                    self.walls['left'] = not self.walls['left']
                    change.append((x, y))
                    # if left:
                    left.walls['right'] = not left.walls['right']
                    change.append((x-1, y))
                if 0.8 < px_cell < 1 and right:
                    print('click right')
                    self.walls['right'] = not self.walls['right']
                    change.append((x, y))
                    # if right:
                    right.walls['left'] = not right.walls['left']
                    change.append((x+1, y))
                if 0 < py_cell < 0.2 and top:
                    print('click top')
                    self.walls['top'] = not self.walls['top']
                    change.append((x, y))
                    # if top:
                    top.walls['bottom'] = not top.walls['bottom']
                    change.append((x, y-1))
                if 0.8 < py_cell < 1 and bottom:
                    print('click bottom')
                    self.walls['bottom'] = not self.walls['bottom']
                    change.append((x, y))
                    # if bottom:
                    bottom.walls['top'] = not bottom.walls['top']
                    change.append((x, y+1))
                return True, change
        return is_click, []

    def __lt__(self, other):
        return self.x + self.y * self.size[0] > other.x + other.y * other.size[0]
