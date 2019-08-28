import heapq
import sys
from os.path import splitext


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class Grid:
    def __init__(self, width, height, start, finish, walls):
        self.start = start
        self.finish = finish
        self.width = width
        self.height = height
        self.walls = walls

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


def parse_maze(maze_name, is_logged = True):
    start = ()
    finish = ()
    start_found = False
    finish_found = False
    walls = []

    try:
        with open(maze_name, 'r') as maze_file:
            maze_data = [line.strip(' "\n') for line in maze_file.readlines()]
            if not maze_data:
                raise IOError
    except IOError:
        if is_logged:
            print('Не удалось прочитать файл лабиринта! Введите путь до файла или создайте лабиринт в файле "maze.txt".')
        sys.exit(1)

    max_line_length = max([len(line) for line in maze_data])

    for i in range(len(maze_data)):
        if maze_data[i].find('S') != -1:
            if start_found:
                if is_logged:
                    print('У лабиринта не может быть больше одного старта! Оставьте один символ "S" в файле с лабиринтом.')
                sys.exit(1)
            else:
                start = (i, maze_data[i].find('S'))
                start_found = True
        if maze_data[i].find('F') != -1:
            if finish_found:
                if is_logged:
                    print('У лабиринта не может быть больше одного финиша! Оставьте один символ "F" в файле с лабиринтом.')
                sys.exit(1)
            else:
                finish = (i, maze_data[i].find('F'))
                finish_found = True
        for j in range(len(maze_data[i])):
            if maze_data[i][j] == 'x':
                walls.append((i, j))
        if len(maze_data[i]) < max_line_length:
            for k in range(len(maze_data[i]), max_line_length):
                walls.append((i, k))

    if not start_found:
        if is_logged:
            print('У лабиринта отсутствует старт! Добавьте его в файл с помощью символа "S".')
        sys.exit(1)
    if not finish_found:
        if is_logged:
            print('У лабиринта отсутствует финиш! Добавьте его в файл с помощью символа "F".')
        sys.exit(1)

    return Grid(len(maze_data), max_line_length, start, finish, walls)


def search_path(graph, is_logged = True):
    queue = PriorityQueue()
    queue.put(graph.start, 0)
    previous_nodes = {graph.start: None}
    costs = {graph.start: 0}

    while not queue.empty():
        current = queue.get()
        if current == graph.finish:
            break
        for next_node in graph.neighbors(current):
            new_cost = costs[current] + 1
            if next_node not in costs or new_cost < costs[next_node]:
                costs[next_node] = new_cost
                priority = new_cost + heuristic(graph.finish, next_node)
                queue.put(next_node, priority)
                previous_nodes[next_node] = current

    return restore_path(previous_nodes, graph.start, graph.finish, is_logged)


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def restore_path(previous_nodes, start, finish, is_logged = True):
    if not(finish in previous_nodes):
        if is_logged:
            print('Хомяку не удалось найти путь в лабиринте :(')
        sys.exit(1)
    else:
        current = previous_nodes[finish]
        path = []
        while current != start:
            path.append(current)
            current = previous_nodes[current]
        return path


def draw_path(maze_name, path, is_logged = True):
    try:
        with open(maze_name, 'r') as maze_file:
            maze_lines = maze_file.readlines()
        for node in path:
            maze_lines[node[0]] = list(maze_lines[node[0]])
            maze_lines[node[0]][node[1] + 1] = '*'
            maze_lines[node[0]] = "".join(maze_lines[node[0]])
        solved_maze_name = '{}_solved.txt'.format(splitext(maze_name)[0])
        with open(solved_maze_name, 'w') as solved_maze_file:
            solved_maze_file.writelines(maze_lines)
        if is_logged:
            print('Хомяк нашёл путь в лабиринте и записал его в файл {}'.format(solved_maze_name))
    except IOError:
        if is_logged:
            print('Не удалось записать решение лабиринта в файл.')
        sys.exit(1)


if __name__ == '__main__':
    maze_name = sys.argv[1] if len(sys.argv) > 1 else 'maze.txt'
    maze = parse_maze(maze_name)
    path = search_path(maze)
    draw_path(maze_name, path)
