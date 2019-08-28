import heapq
import sys
from os.path import splitext
import argparse


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


def read_maze(maze_name):
    try:
        with open(maze_name, 'r') as maze_file:
            source_maze_data = maze_file.readlines()
            maze_data = [line.strip(' "\n') for line in source_maze_data]
            if not maze_data:
                raise IOError

            return source_maze_data, maze_data
    except IOError:
        raise Exception('Не удалось прочитать файл лабиринта! Введите путь до файла или создайте лабиринт в файле "maze.txt".')


def parse_maze(maze_data):
    start = ()
    finish = ()
    start_found = False
    finish_found = False
    walls = []

    max_line_length = max([len(line) for line in maze_data])

    for i in range(len(maze_data)):
        start_position = maze_data[i].find('S')
        if start_position != -1:
            if start_found:
                raise Exception('У лабиринта не может быть больше одного старта! Оставьте один символ "S" в файле с лабиринтом.')
            else:
                start = (i, start_position)
                start_found = True
        finish_position = maze_data[i].find('F')
        if finish_position != -1:
            if finish_found:
                raise Exception('У лабиринта не может быть больше одного финиша! Оставьте один символ "F" в файле с лабиринтом.')
            else:
                finish = (i, finish_position)
                finish_found = True
        for j in range(len(maze_data[i])):
            if maze_data[i][j] == 'x':
                walls.append((i, j))
        if len(maze_data[i]) < max_line_length:  # Будем считать, что в отсутствующих клетках стоят стены
            for k in range(len(maze_data[i]), max_line_length):
                walls.append((i, k))

    if not start_found:
        raise Exception('У лабиринта отсутствует старт! Добавьте его в файл с помощью символа "S".')
    if not finish_found:
        raise Exception('У лабиринта отсутствует финиш! Добавьте его в файл с помощью символа "F".')

    return Grid(len(maze_data), max_line_length, start, finish, walls)


def calc_heuristic_dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def restore_path(previous_nodes, start, finish):
    if not (finish in previous_nodes):
        raise Exception('Хомяку не удалось найти путь в лабиринте :(')
    else:
        current = previous_nodes[finish]
        path = []
        while current != start:
            path.append(current)
            current = previous_nodes[current]
        return path


def search_path(graph):
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
                priority = new_cost + calc_heuristic_dist(graph.finish, next_node)
                queue.put(next_node, priority)
                previous_nodes[next_node] = current

    return restore_path(previous_nodes, graph.start, graph.finish)


def draw_path(maze_lines, solved_maze_name, path, verbose=False):
    try:
        for node in path:
            maze_lines[node[0]] = list(maze_lines[node[0]])
            maze_lines[node[0]][node[1] + 1] = '*'
            maze_lines[node[0]] = "".join(maze_lines[node[0]])
        with open(solved_maze_name, 'w') as solved_maze_file:
            solved_maze_file.writelines(maze_lines)
        if verbose:
            print('Хомяк нашёл путь в лабиринте и записал его в файл {}'.format(solved_maze_name))
    except IOError:
        raise Exception('Не удалось записать решение лабиринта в файл.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-in_maze', type=str, default='maze.txt', help='Входной файл для лабиринта')
    parser.add_argument('-out_maze', type=str, help='Выходной файл для решённого лабиринта')
    parser.add_argument('-v', action="store_true", help='Включает подробный режим (программа пишет о успешном завершении или возникшей ошибке)')
    args = parser.parse_args()

    maze_name = args.in_maze
    solved_maze_name = args.out_maze if args.out_maze else '{}_solved.txt'.format(splitext(maze_name)[0])

    try:
        lines, maze_data = read_maze(maze_name)
        maze = parse_maze(maze_data)
        path = search_path(maze)
        draw_path(lines, solved_maze_name, path, args.v)
    except Exception as ex:
        print(ex)
        sys.exit(1)
