from drawer import Drawer
from states import get_states

if __name__ == "__main__":
    states = get_states()
    print("Number of unique states:", len(states))
    Drawer().draw(states, "states_poster")
