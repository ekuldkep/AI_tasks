from queue import Queue


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


def sim_world(world_map):
    x_lenght = len(world_map[0])
    y_length = len(world_map)
    size = (x_lenght, y_length)

    start = get_coordinates_of(world_map, Constants.s)
    diamond = get_coordinates_of(world_map, Constants.D)

    frontier = Queue()
    frontier.put(start)
    came_from = {start: None}
    lava = []

    while not frontier.empty():
        current = frontier.get()

        for next in get_neighbours(current, size):
            if next not in came_from and not is_there_lava(world_map, next):
                frontier.put(next)
                came_from[next] = current

        if current == diamond:
            path = reconstruct_path(came_from, diamond, start)
            print("path:", path)
            break

    print("lava:", lava)
    e = print_map_with_path(path, world_map, start, diamond, size)


def reconstruct_path(came_from, diamond, start):
    path = []
    new = diamond

    while new != start:
        pointer = came_from[new]
        new = pointer
        path.append(pointer)
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
    print(a)
    print(len(map))

    return map


def make_string_row(list_of_steps_in_row, world_map, current_row, row_length):
    print("row_length:", row_length)
    row = [Constants.free_path] * row_length

    print(len(list_of_steps_in_row))

    for step in list_of_steps_in_row:
        x, y = step
        row[x] = Constants.path

    for i in range(row_length):
        current = world_map[current_row][i]
        if current == Constants.lava:
            row[i] = Constants.lava
        if current in Constants.s:
            row[i] = Constants.s
        if current in Constants.D:
            row[i] = Constants.D

    row = "".join(row)
    print("row:", row)
    return row


def insert_str(string, str_to_insert, index):
    return string[:index - 1] + str_to_insert + string[index:]


sim_world(Constants.lava_map1)
