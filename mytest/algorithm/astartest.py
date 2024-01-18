import os
import heapq

def heuristic(cell, end):
    # Sử dụng khoảng cách Manhattan làm hàm heuristic
    return abs(cell[0] - end[0]) + abs(cell[1] - end[1])

def solve_maze_a_star(maze):
    if not maze or not maze[0]:
        return []

    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)

    priority_queue = [(0, start)]
    visited = set()
    g_values = {start: 0}
    maze_copy = [row[:] for row in maze]

    step = 1

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        x, y = current

        maze_copy[x][y] = 2

        os.system("cls" if os.name == "nt" else "clear")

        print("Step {}:".format(step))
        for row in maze_copy:
            print(row)
        print("\n")

        if current == end:
            break

        step += 1

        next_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for move in next_moves:
            nx, ny = move
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                g_value = g_values[current] + 1
                if move not in g_values or g_value < g_values[move]:
                    g_values[move] = g_value
                    f_value = g_value + heuristic(move, end)
                    heapq.heappush(priority_queue, (f_value, move))
                    visited.add(move)

    return maze_copy

# Maze ví dụ
maze = [
    [0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0]
]

result = solve_maze_a_star(maze)
if result:
    print("Maze cuối cùng:")
    for row in result:
        print(row)
else:
    print("Không có đường đi từ điểm đầu đến điểm cuối trong maze.")
