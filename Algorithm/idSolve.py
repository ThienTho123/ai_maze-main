import pygame
from config.logicConfig import Config


def ids(maze, start, goal, sc, config=None):
    if config is None:
        config = Config()

    max_depth = 0
    draw_count = 0
    draw_frequency = 3  # Adjust this value for the frequency of updates

    while True:
        stack = [(start, [start])]
        while stack:
            current_cell, path = stack.pop()

            if current_cell.visited:
                continue

            current_cell.visited = True
            draw_count += 1

            if current_cell == goal:
                [cell.draw_current_cell(sc) for cell in path]
                return path

            if len(path) <= max_depth:
                neighbors = current_cell.find_neighbors(maze)
                unvisited_neighbors = [n for n in neighbors if not n.visited]

                for neighbor in unvisited_neighbors:
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_path))

            # if max_depth > 25:
            #     draw_frequency = 5
            # else:draw_frequency=1
            #
            # if draw_count % draw_frequency == 0:
            #     [cell.draw(sc) for cell in maze]
            #     pygame.display.flip()
            #
            #
            #     # Gradually increase the speed based on depth
            #
            #     speed = 20 +  max_depth**15
                pygame.time.Clock().tick(60)
                [cell.draw(sc) for cell in maze]
                pygame.display.flip()

        for cell in maze:
            cell.visited = False

        max_depth += 1

    return None