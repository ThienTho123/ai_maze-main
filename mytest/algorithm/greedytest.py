import os
import heapq

def solve_maze_greedy(maze):
    if not maze or not maze[0]:
        return []

    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)

    priority_queue = [(0, start)]
    visited = set()
    maze_copy = [row[:] for row in maze]  # Create a copy of the maze

    step = 1

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        x, y = current

        # Mark the current cell as part of the path
        maze_copy[x][y] = 2

        # Clear the console (for better visualization)
        os.system("cls" if os.name == "nt" else "clear")

        # Print the step number
        print("Step {}:".format(step))

        # Print the maze at this step
        for row in maze_copy:
            print(row)
        print("\n")

        if current == end:
            break  # Stop if the end is reached

        step += 1

        # Calculate the next move based on Greedy heuristic (e.g., distance to the goal)
        next_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        next_moves = [(nx, ny) for nx, ny in next_moves if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited]
        next_moves = sorted(next_moves, key=lambda p: abs(p[0] - end[0]) + abs(p[1] - end[1]))

        for move in next_moves:
            heapq.heappush(priority_queue, (abs(move[0] - end[0]) + abs(move[1] - end[1]), move))
            visited.add(move)

    return maze_copy

# Example maze
maze = [
    [0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0]
]

result = solve_maze_greedy(maze)
if result:
    print("Final Maze:")
    for row in result:
        print(row)
else:
    print("Không có đường đi từ điểm đầu đến điểm cuối trong maze.")

