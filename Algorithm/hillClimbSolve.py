import pygame
from config.logicConfig import Config

def evaluate(cell, goal):
    return ((cell.x - goal.x) ** 2 + (cell.y - goal.y) ** 2) ** 0.5

def hill_climbing(maze, start, goal, sc, config=None):
    if config is None:
        config = Config()
    print('hear')

    current_cell = start
    path = [current_cell]
    visited_cells = set()  # Danh sách các ô đã đi qua
    found_path = False

    while current_cell != goal:
        current_cell.visited = True
        neighbors = current_cell.find_neighbors(maze)

        best_neighbor = None
        best_score = float('inf')

        for neighbor in neighbors:
            if neighbor not in visited_cells:  # Đảm bảo không quay lại ô đã đi qua
                score = evaluate(neighbor, goal)
                if score < best_score:
                    best_score = score
                    best_neighbor = neighbor

        if best_neighbor is None:
            # Không tìm thấy đường đi, quay lại bước trước đó
            if len(path) > 1:  # Nếu có ít nhất 2 ô trong đường đi
                visited_cells.add(current_cell)  # Thêm ô hiện tại vào danh sách đã đi qua
                path.pop()  # Bỏ ô hiện tại
                current_cell = path[-1]  # Đặt ô hiện tại là ô trước đó
            else:
                # Nếu không còn ô nào để quay lại, thoát vòng lặp vô hạn
                break
        else:
            # Tìm thấy ô tiếp theo, thêm vào đường đi
            path.append(best_neighbor)
            visited_cells.add(current_cell)
            current_cell = best_neighbor

        [cell.draw_current_cell(sc) for cell in path]
        [cell.draw(sc) for cell in maze]
        pygame.display.flip()
        pygame.time.Clock().tick(20)
        pygame.display.update()

        if current_cell == goal:
            found_path = True
            break

    if found_path:
        return path  # Trả về đường đi nếu tìm thấy
    else:
        return None  # Trả về None nếu không tìm thấy đường đi
