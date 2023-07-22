
WIN_STATES = [0b000000111, 0b000111000, 0b111000000, 0b100100100, 0b010010010, 0b001001001, 0b100010001, 0b001010100]


def dfs(x, o, turn, squares_left, states):
    square = 1

    while square < 0b1000000000:

        if square & squares_left:
            x_new = x
            o_new = o

            if turn:
                x_new |= square
            else:
                o_new |= square

            game_end = 0

            for state in WIN_STATES:
                if (state & x_new) == state or (state & o_new) == state:
                    game_end = 1
                    break

            states.add((x_new, o_new, game_end))

            if not game_end:
                dfs(x_new, o_new, not turn, square ^ squares_left, states)                

        square <<= 1


def get_states():
    states = set()
    states.add((0, 0, 0))
    dfs(0, 0, True, 0b111111111, states)
    return states
