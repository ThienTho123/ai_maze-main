import heapq

import pygame
from config.logicConfig import Config

def ucs(maze, start, goal, sc, config=None):
    if config is None:
        config = Config()

    queue = [(0, start, [])]  # Initialize the queue with the start cell, its cost, and an empty path
    heapq.heapify(queue)

    while queue:
        current_cost, current_cell, path = heapq.heappop(queue)

        if current_cell == goal:
            [cell.draw_current_cell(sc) for cell in path]
            return path

        if not current_cell.visited:
            current_cell.visited = True

            neighbors = current_cell.find_neighbors(maze)

            for neighbor in neighbors:
                new_cost = current_cost + neighbor.cost

                new_path = path + [current_cell]
                heapq.heappush(queue, (new_cost, neighbor, new_path))

        [cell.draw(sc) for cell in maze]
        pygame.display.flip()
        pygame.time.Clock().tick(20)
        pygame.display.update()

    return None