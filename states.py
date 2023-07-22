# represent game as bitboard
WIN_STATES = [0b000000111, 0b000111000, 0b111000000, 0b100100100, 0b010010010, 0b001001001, 0b100010001, 0b001010100]


def dfs(x, o, turn, squares_left, states):
    square = 1 # bit indicates the square we are checking

    while square < 0b1000000000:

        if square & squares_left:
            x_new = x
            o_new = o

            # make move
            if turn:
                x_new |= square
            else:
                o_new |= square

            # check if a player has won
            game_won = 0
            for state in WIN_STATES:
                if (state & x_new) == state or (state & o_new) == state:
                    game_won = 1
                    break

            # store state tuple of (x-bitboard, o-bitboard, a player won)
            states.add((x_new, o_new, game_won))

            # only proceed to next state if no player has won yet
            if not game_won:
                dfs(x_new, o_new, not turn, square ^ squares_left, states)

        square <<= 1


def get_states():
    states = set()
    states.add((0, 0, 0)) # add starting empty state
    dfs(0, 0, True, 0b111111111, states)
    return states
