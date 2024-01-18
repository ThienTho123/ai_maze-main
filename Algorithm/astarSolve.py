import pygame
from config.logicConfig import Config


def a_star(maze, start, goal, sc, config=None):
    if config is None:
        config = Config()

    open_set = [start]
    came_from = {}
    g_score = {cell: float('inf') for cell in maze}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in maze}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = min(open_set, key=lambda cell: f_score[cell])

        if current == goal:
            path = reconstruct_path(came_from, current)
            [cell.draw_current_cell(sc) for cell in path]
            return path

        open_set.remove(current)

        if not current.visited:  # Check the 'visited' attribute of the cell
            current.visited = True

            for neighbor in current.find_neighbors(maze):
                tentative_g_score = g_score[current] + 1  # Assuming each step has a cost of 1

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

                    if neighbor not in open_set:
                        open_set.append(neighbor)

        [cell.draw(sc) for cell in maze]
        pygame.display.flip()
        pygame.time.Clock().tick(20)
        pygame.display.update()

    return None


def heuristic(cell, goal):
    # Define your heuristic function here, e.g., Manhattan distance
    return ((cell.x - goal.x) ** 2 + (cell.y - goal.y) ** 2) ** 0.5


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path