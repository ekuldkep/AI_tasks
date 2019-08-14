import games


class Constants:
    neighbours = {"a1": ("a3", "b2", "b1"), "b1": ("a1", "c1", "d1"), "c1": ("b1", "c2", "d1"),
                  "d1": ("b1", "c1", "e1"), "e1": ("d1", "d2", "e3"), "a3": ("a1", "b3", "a5"),
                  "b3": ("a3", "b2", "c3", "b4"), "b2": ("a1", "b3", "c2"), "c2": ("b2", "d2", "c1", "c3"),
                  "d2": ("c2", "d3", "e1"), "d3": ("d2", "c3", "d4", "e3"), "c3": ("b3", "c2", "d3", "c4"),
                  "b4": ("b3", "a5", "c4"), "c4": ("b4", "c5", "c3", "d4"), "d4": ("d3", "c4", "e5"),
                  "a5": ("b4", "a3", "b5"), "b5": ("a5", "c5", "d5"), "c5": ("b5", "c4", "d5"),
                  "d5": ("b5", "c5", "e5"), "e5": ("d5", "d4", "e3"), "e3": ("e1", "e5", "d3")}
    bear = "Bear"
    man1 = "man1"
    man2 = "man2"
    man3 = "man3"
    player_bear = "player_bear"
    player_human = "player_human"
    # initial turn, bear, hunters


def get_bear_moves(state):
    moves = []
    neighbours = Constants.neighbours[state[2]]
    [moves.append((state[2], neighbour)) for neighbour in neighbours if neighbour not in state[3:]]
    return moves


def get_hunters_moves(state):
    moves = []
    dict = {}
    for hunter_pos in state[3:]:
        neighbours = Constants.neighbours[hunter_pos]
        dict[hunter_pos] = neighbours
    for key in dict:
        for value in dict[key]:
            if value not in state[2:]:
                moves.append((key, value))
    return moves


class BearGame(games.Game):
    def __init__(self):
        self.initial = (0, Constants.player_bear, "c3", "b1", "c1", "d1")
        return

    def to_move(self, state):
        return state[1]

    def actions(self, state):
        if state[1] == Constants.player_bear:
            return tuple(get_bear_moves(state))
        else:
            return tuple(get_hunters_moves(state))

    def result(self, state, action):
        from_place, to_place = action
        state_list = list(state)
        state_list[0] += 1
        if state[1] == Constants.player_bear:
            state_list[2] = to_place
            state_list[1] = Constants.player_human
        else:
            hunter_position_to_change = state_list.index(from_place)
            state_list[hunter_position_to_change] = to_place
            state_list[1] = Constants.player_bear
        return tuple(state_list)

    def utility(self, state, side):
        bear_step_count = len(get_bear_moves(state))
        win = 1000
        step_count = state[0]
        bear_is_alive = bool(bear_step_count) * win

        score = bear_is_alive + bear_step_count
        score += step_count * 0.1

        if state[1] == Constants.player_bear:
            return score

        return -score

    def terminal_test(self, state):
        print("test", state)
        if state[1] == Constants.player_bear:
            if not get_bear_moves(state):
                return True
        return False


bg = BearGame()

bg.play_game(games.query_player,
              games.random_player)