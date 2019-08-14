import search
from search import Problem


def read_txt_file(filename):
    with open(filename) as f:
        city_count = f.readline()
        lines = f.readlines()
        matrix = []
        for line in lines:
            city_lengths = line.split()
            city_lengths = [int(i) for i in city_lengths]
            matrix.append(city_lengths)
    # print(matrix)
    return int(city_count), matrix


def get_initial_route(city_matrix, city_count):
    b = 0
    initial_route = [b]

    for i in range(city_count - 1):
        print(initial_route, i)
        city_row = city_matrix[b]
        b = city_row.index(min(cost for cost in city_row if city_row.index(cost) not in initial_route))
        print(b)
        initial_route.append(b)
    print(initial_route)
    return initial_route


def get_possible_pairs(city_count):
    list_of_pairs = []
    for i in range(city_count):
        for a in range(city_count):
            if [i, a] not in list_of_pairs:
                list_of_pairs.append([i, a])

    return tuple(list_of_pairs)


def two_opt_swap_route(route, i, k):
    route_as_list = list(route)
    route_first_side = route_as_list[0:i]
    reversed = route_as_list[i:k + 1]
    reversed.reverse()
    route_first_side.extend(reversed)
    route_end = route_as_list[k + 1:]
    route_first_side.extend(route_end)
    return tuple(route_first_side)


class TSP(Problem):
    def __init__(self, instance):
        self.city_count, self.matrix = read_txt_file(instance + ".txt")
        self.initial = get_initial_route(self.matrix, self.city_count)

    def actions(self, state):
        return get_possible_pairs(self.city_count)

    def result(self, state, action):
        return two_opt_swap_route(state, *action)

    def cost(self, state):
        cost = 0
        start = state[0]

        for end in state[1:]:
            num = self.matrix[start][end]
            cost += num
            start = end

        last_to_home = self.matrix[state[-1]][state[0]]
        return cost + last_to_home

    def value(self, state):
        return 1 / (self.cost(state) + 1)

p = search.InstrumentedProblem(TSP("gr48"))
g = search.hill_climbing(p)
print(g)
print(p.cost(g))
