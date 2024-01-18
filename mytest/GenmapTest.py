import pygame

from config.config import INIT_WIDTH, CELLSIZE, INIT_HEIGHT, FPS
from object.gameplay.Cell import Cell

size = INIT_WIDTH // CELLSIZE, INIT_HEIGHT // CELLSIZE


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


def generate_maze():
    rows, cols = size
    grid_cells = [Cell(col, row, size) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()
    return grid_cells


if __name__ == "__main__":
    RES = INIT_WIDTH, INIT_HEIGHT
    pygame.init()
    sc = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    cols, rows = size
    print("res, rows, cols", RES, INIT_WIDTH // CELLSIZE, INIT_HEIGHT // CELLSIZE, size)
    grid_cells = [Cell(col, row, size) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    colors, color = [], 40

    while True:
        sc.fill(pygame.Color('darkslategray'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        [cell.draw(sc) for cell in grid_cells]
        current_cell.visited = True
        current_cell.draw_current_cell(sc)
        [pygame.draw.rect(sc, colors[i], (cell.x * CELLSIZE + 5, cell.y * CELLSIZE + 5, CELLSIZE - 10, CELLSIZE - 10),
                          border_radius=12) for i, cell in enumerate(stack)]
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            colors.append((min(color, 255), 10, 100))
            color += 1
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()

        pygame.display.flip()
        clock.tick(FPS)
