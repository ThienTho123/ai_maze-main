import pygame

from Algorithm.dfsMapGeneration import DFSMAPGen
from config.config import INIT_WIDTH, CELLSIZE, INIT_HEIGHT, FPS
from object.gameplay.Cell import Cell

size = INIT_WIDTH // CELLSIZE, INIT_HEIGHT // CELLSIZE
RES = INIT_WIDTH, INIT_HEIGHT

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


cols, rows = size
print("res, rows, cols", RES, INIT_WIDTH // CELLSIZE, INIT_HEIGHT // CELLSIZE, size)
grid_cells = [Cell(col, row, size) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]


gen_map = DFSMAPGen(grid_cells)

while True:
    sc.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw(sc) for cell in grid_cells]
    current_cell = gen_map.draw_maze(sc,current_cell)

    pygame.display.flip()
    clock.tick(FPS)