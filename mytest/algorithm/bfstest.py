import os

def solve_maze_bfs(maze):
    if not maze or not maze[0]:
        return []

    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)

    stack = [start]
    visited = set()
    maze_copy = [row[:] for row in maze]  # Create a copy of the maze

    step = 1

    while stack:
        current = stack.pop()

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

        # Try moving up
        if x > 0 and maze[x - 1][y] == 0 and (x - 1, y) not in visited:
            stack.append((x - 1, y))
            visited.add((x - 1, y))

        # Try moving down
        if x < rows - 1 and maze[x + 1][y] == 0 and (x + 1, y) not in visited:
            stack.append((x + 1, y))
            visited.add((x + 1, y))

        # Try moving left
        if y > 0 and maze[x][y - 1] == 0 and (x, y - 1) not in visited:
            stack.append((x, y - 1))
            visited.add((x, y - 1))

        # Try moving right
        if y < cols - 1 and maze[x][y + 1] == 0 and (x, y + 1) not in visited:
            stack.append((x, y + 1))
            visited.add((x, y + 1))

    return maze_copy

# Example maze
maze = [
    [0, 0, 1, 1, 1],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0]
]

result = solve_maze_bfs(maze)
if result:
    print("Final Maze:")
    for row in result:
        print(row)
else:
    print("Không có đường đi từ điểm đầu đến điểm cuối trong maze.")
