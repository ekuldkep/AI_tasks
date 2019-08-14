from queue import Queue, PriorityQueue
import time
import math


class Constants:
    lava_map1 = [
        "      **               **      ",
        "     ***     D        ***      ",
        "     ***                       ",
        "                      *****    ",
        "           ****      ********  ",
        "           ***          *******",
        " **                      ******",
        "*****             ****     *** ",
        "*****              **          ",
        "***                            ",
        "              **         ******",
        "**            ***       *******",
        "***                      ***** ",
        "                               ",
        "                s              ",
    ]

    lava_map1 = [
        "     **********************    ",
        "   *******   D    **********   ",
        "   *******                     ",
        " ****************    **********",
        "***********          ********  ",
        "            *******************",
        " ********    ******************",
        "********                   ****",
        "*****       ************       ",
        "***               *********    ",
        "*      ******      ************",
        "*****************       *******",
        "***      ****            ***** ",
        "                               ",
        "                s              ",
    ]

    s = "s"
    D = "D"
    lava = "*"
    free_path = " "
    path = "."


def return_map_small():
    with open("cave300x300") as f:
        return [l.strip() for l in f.readlines() if len(l) > 1]


def return_map_middle():
    with open("cave600x600") as f:
        return [l.strip() for l in f.readlines() if len(l) > 1]


def return_map_big():
    with open("cave900x900") as f:
        return [l.strip() for l in f.readlines() if len(l) > 1]


def astar(world_map, heuristic):
    start_time = time.time()
    x_lenght = len(world_map[0])
    y_length = len(world_map)
    size = (x_lenght, y_length)

    start = get_coordinates_of(world_map, Constants.s)
    diamond = get_coordinates_of(world_map, Constants.D)

    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    lava = []

    while not frontier.empty():
        _, current = frontier.get()

        for next in get_neighbours(current, size):
            new_cost = cost_so_far[current] + 1
            if (next not in cost_so_far or new_cost < cost_so_far[next]) and not is_there_lava(world_map, next):
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, diamond)
                frontier.put((priority, next))
                came_from[next] = current

        if current == diamond:
            path = reconstruct_path(came_from, diamond, start)
            break
    end = time.time()
    print_map_with_path(path, world_map, start, diamond, size)
    # print(end, len(path))
    return end - start_time, len(path)


def greedy(world_map, heuristic):
    start_time = time.time()
    x_lenght = len(world_map[0])
    y_length = len(world_map)
    size = (x_lenght, y_length)

    start = get_coordinates_of(world_map, Constants.s)
    diamond = get_coordinates_of(world_map, Constants.D)

    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    lava = []

    while not frontier.empty():
        _, current = frontier.get()

        for next in get_neighbours(current, size):
            if next not in came_from and not is_there_lava(world_map, next):
                priority = heuristic(next, diamond)
                frontier.put((priority, next))
                came_from[next] = current

        if current == diamond:
            path = reconstruct_path(came_from, diamond, start)
            break
    end = time.time()
    print_map_with_path(path, world_map, start, diamond, size)
    # print(end, len(path))
    return end - start_time, len(path)


def reconstruct_path(came_from, diamond, start):
    path = []
    new = diamond

    while new != start:
        pointer = came_from[new]
        new = pointer
        path.append(pointer)
    # print(list(filter(lambda p: p[1] == 14, path)))
    return path


def get_coordinates_of(world_map, place_to_find):
    for y_index, row in enumerate(world_map):
        if place_to_find in row:
            x_index = world_map[y_index].find(place_to_find)

            return x_index, y_index


def get_neighbours(current, size):

    neighbours = [
        (current[0], current[1] - 1),
        (current[0] - 1, current[1]),
        (current[0], current[1] + 1),
        (current[0] + 1, current[1])
    ]

    return [neighbour for neighbour in neighbours if is_coordinate_on_map(neighbour, size)]


def get_neighbours_diagonal(current, size):

    neighbours = [
        (current[0], current[1] - 1),
        (current[0] - 1, current[1] + 1),
        (current[0] - 1, current[1]),
        (current[0] - 1, current[1] - 1),
        (current[0], current[1] + 1),
        (current[0] + 1, current[1] - 1),
        (current[0] + 1, current[1]),
        (current[0] + 1, current[1] + 1)
    ]

    return [neighbour for neighbour in neighbours if is_coordinate_on_map(neighbour, size)]


def is_coordinate_on_map(coordinate, size):
    if coordinate[0] >= size[0] or coordinate[1] >= size[1] or coordinate[0] < 0 or coordinate[1] < 0:
        return False

    return True


def is_there_lava(world_map, coordinate):
    coordinate_row = world_map[coordinate[1]]
    if coordinate_row[coordinate[0]] == Constants.lava:
        return True

    return False


def print_map_with_path(path, world_lava, start, diamond, size):
    map = []
    a = ""
    for row in range(size[1]):
        list_of_steps_in_row = []
        for step in path:
            if step[1] == row:
                list_of_steps_in_row.append(step)
        string_row = make_string_row(list_of_steps_in_row, world_lava, row, size[0])
        map.append(string_row)
    for count in range(len(map)):
        a += "%s \n" % (map[count])
    # print(a)
    # print(len(map))

    return map


def make_string_row(list_of_steps_in_row, world_map, current_row, row_length):
    row = [Constants.free_path] * row_length

    for step in list_of_steps_in_row:
        x, y = step
        row[x] = Constants.path

    for i in range(row_length):
        current = world_map[current_row][i]
        if current in Constants.lava:
            row[i] = Constants.lava
        if current in Constants.s:
            row[i] = Constants.s
        if current in Constants.D:
            row[i] = Constants.D

    row = "".join(row)
    return row


def insert_str(string, str_to_insert, index):
    return string[:index - 1] + str_to_insert + string[index:]


def manhattan_distance(current, diamond):
    currentx, currenty = current
    diamondx, diamondy = diamond
    return abs(currentx - diamondx) + abs(currenty - diamondy)


def eucleidean_distance(current, diamond):
    currentx, currenty = current
    diamondx, diamondy = diamond
    return math.sqrt(pow(diamondx - currentx, 2) + pow(diamondy - currenty, 2))


def compare_algorithms(astar, greedy, type):

    print("astar_time, astar_steps", astar, type)
    print("greedy_time, greedy_steps", greedy, type)


# astar_call = astar(Constants.lava_map1, eucleidean_distance)
# greedy_call = greedy(Constants.lava_map1, eucleidean_distance)
# compare_algorithms(astar_call, greedy_call, "euc")
#
# astar_euc = astar(Constants.lava_map1, manhattan_distance)
# greedy_euc = greedy(Constants.lava_map1, manhattan_distance)
# compare_algorithms(astar_euc, greedy_euc, "manhatt")

astar_call_small = astar(return_map_small(), manhattan_distance)
greedy_call_small = greedy(return_map_small(), manhattan_distance)
compare_algorithms(astar_call_small, greedy_call_small, "mannhattan_small")

astar_euc_middle = astar(return_map_middle(), manhattan_distance)
greedy_euc_middle = greedy(return_map_middle(), manhattan_distance)
compare_algorithms(astar_euc_middle, greedy_euc_middle, "mannhattan_middle")

astar_euc_big = astar(return_map_big(), manhattan_distance)
greedy_euc_big = greedy(return_map_big(), manhattan_distance)
compare_algorithms(astar_euc_big, greedy_euc_big, "mannhattan_big")

astar_call_small = astar(return_map_small(), eucleidean_distance)
greedy_call_small = greedy(return_map_small(), eucleidean_distance)
compare_algorithms(astar_call_small, greedy_call_small, "eucleidean_small")

astar_euc_middle = astar(return_map_middle(), eucleidean_distance)
greedy_euc_middle = greedy(return_map_middle(), eucleidean_distance)
compare_algorithms(astar_euc_middle, greedy_euc_middle, "eucleidean_middle")

astar_euc_big = astar(return_map_big(), eucleidean_distance)
greedy_euc_big = greedy(return_map_big(), eucleidean_distance)
compare_algorithms(astar_euc_big, greedy_euc_big, "eucleidean_big")

