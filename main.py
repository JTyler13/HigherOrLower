# Higher or Lower Game

# main.py
from game_engine import play_game, plot_game

# Now you can use them as if they were defined right here!
if __name__ == "__main__":
    print("Starting Higher or Lower Simulation...")

    # 1. Run a single game
    data = play_game(100)

    # 2. Plot the result
    plot_game(data)
