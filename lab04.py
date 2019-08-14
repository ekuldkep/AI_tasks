import search
import math
from copy import deepcopy


class Constants:
    up = "Up"
    down = "Down"
    right = "Right"
    left = "Left"

    begin = (
        1, 2, 3,
        7, 0, 5,
        8, 4, 6
    )

    Goal = (
        1, 2, 3,
        4, 5, 6,
        7, 8, 0
    )

    possible_actions = ((down, right), (left, down, right), (left, down), (up, down, right), (up, left, down, right),
                        (up, left, down), (up, right), (up, right, left), (up, left))


class EightPuzzle(search.Problem):
    counter = 0

    def actions(self, state):
        zero_place = state.index(0)
        return Constants.possible_actions[zero_place]

    def result(self, state, action):
        zero_place = state.index(0)
        to_be_switched = get_action_specific_neighbour_index(action, state, zero_place)
        state_copy = deepcopy(state)
        tuple_to_list = list(state_copy)
        tuple_to_list[zero_place], tuple_to_list[to_be_switched] = tuple_to_list[to_be_switched], tuple_to_list[zero_place]

        # print(action)
        # print(state)
        # print(tuple_to_list)
        # print()
        return tuple(tuple_to_list)

    def goal_test(self, state):
        self.counter += 1
        if self.counter == 1000 and False:
            self.counter = 0
            return True
        if state == self.goal:
            return True

    def path_cost(self, c, state1, action, state2):
        return c + 1  # uus cost peale ühe sammu tegemist


def get_action_specific_neighbour_index(action, state, zero_place):
    row_length = int(math.sqrt(len(state)))
    if action == Constants.up:
        return zero_place - row_length
    if action == Constants.down:
        return zero_place + row_length
    if action == Constants.right:
        return zero_place + 1
    return zero_place - 1


problem = EightPuzzle(Constants.begin, Constants.Goal)
goalnode = search.breadth_first_graph_search(problem)
# sammud (tegevused, käigud) algolekust lõppolekuni
print(goalnode.solution())
# olekud algolekust lõppolekuni
print("path", goalnode.path())
print("path_len", len(goalnode.path()))

problem = EightPuzzle(Constants.begin, Constants.Goal)
goalnode = search.iterative_deepening_search(problem)
# sammud (tegevused, käigud) algolekust lõppolekuni
print(goalnode.solution())
# olekud algolekust lõppolekuni
print("path", goalnode.path())
print("path_len", len(goalnode.path()))


search.compare_searchers([problem], ["name", "result"],
                         searchers=[search.breadth_first_graph_search, search.iterative_deepening_search])

