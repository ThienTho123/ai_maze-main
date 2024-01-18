from collections import deque

import pygame

from config.logicConfig import Config


def bfs(maze, start, goal, sc, config=None):
    if config is None:
        config = Config()
    print('hear')
    queue = deque([(start, [])])  # Initialize the queue with the start cell and an empty path

    while queue:
        current_cell, path = queue.popleft()  # Dequeue the current cell and its path

        if current_cell == goal:
            [cell.draw_current_cell(sc) for cell in path]
            # We found the goal, return the path
            return path

        if not current_cell.visited:
            current_cell.visited = True

            # Get neighboring cells
            neighbors = current_cell.find_neighbors(maze)

            for neighbor in neighbors:
                new_path = path + [current_cell]
                queue.append((neighbor, new_path))

        [cell.draw(sc) for cell in maze]
        pygame.display.flip()
        pygame.time.Clock().tick(20)
        pygame.display.update()

    # If no path is found, return None to indicate that there's no solution
    return None


