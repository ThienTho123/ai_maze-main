def solve_maze(maze):
    if not maze or not maze[0]:
        return []

    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)

    stack = [start]
    visited = set()

    while stack:
        current = stack[-1]

        if current == end:
            break  # Dừng nếu tìm thấy đường đi

        x, y = current

        # Thử đi lên
        if x > 0 and maze[x - 1][y] == 0 and (x - 1, y) not in visited:
            stack.append((x - 1, y))
            visited.add((x - 1, y))
            continue

        # Thử đi xuống
        if x < rows - 1 and maze[x + 1][y] == 0 and (x + 1, y) not in visited:
            stack.append((x + 1, y))
            visited.add((x + 1, y))
            continue

        # Thử đi sang trái
        if y > 0 and maze[x][y - 1] == 0 and (x, y - 1) not in visited:
            stack.append((x, y - 1))
            visited.add((x, y - 1))
            continue

        # Thử đi sang phải
        if y < cols - 1 and maze[x][y + 1] == 0 and (x, y + 1) not in visited:
            stack.append((x, y + 1))
            visited.add((x, y + 1))
            continue

        # Nếu không thể di chuyển, loại bỏ vị trí hiện tại khỏi stack
        stack.pop()

    # Tạo một maze kết quả với đường đi được đánh dấu bằng giá trị 2
    result_maze = [row[:] for row in maze]
    for step in stack:
        x, y = step
        result_maze[x][y] = 2

    return result_maze

# Ví dụ một maze
maze = [
    [0, 1, 0, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0]
]

result = solve_maze(maze)
if result:
    print("Maze kết quả:")
    for row in result:
        print(row)
else:
    print("Không có đường đi từ điểm đầu đến điểm cuối trong maze.")
