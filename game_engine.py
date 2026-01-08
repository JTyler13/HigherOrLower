# Higher or Lower Game

# Here we are building a version of 'Higher or Lower', whereby the game will pick a random number between 1 and n (n provided by the user) and then randomly guess numbers until it reaches the correct choice. This is not the optimal way of playing the game (i.e. splitting the options in half every guess), but does give an interesting insight into a random method.

#### Import packages ####
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

#### Game function ####
def play_game(upper_bound=10):
    current_guess=0
    guesses=[]
    target=random.randint(1,upper_bound)
    p1=1
    p2=upper_bound

    while current_guess != target:
        current_guess=random.randint(p1,p2)
        guesses.append(current_guess)
        if current_guess == target:
            break
        elif current_guess > target:
            p2 = current_guess -1
        else:
            p1 = current_guess +1

    return {
        "target": target,
        "count": len(guesses),
        "history": guesses,
        "limit":upper_bound
    }


#### Plot function ####
def plot_game(result):
    history = result['history']
    target = result['target']
    limit = result['limit']

    attempts = range(1, len(history) + 1)

    point_cols=[]
    for guess in history:
        if guess > target:
            point_cols.append('red')
        elif guess < target:
            point_cols.append('blue')
        else:
            point_cols.append('green')

    plt.figure(figsize=(10, 6)) # Optional: make it big

    plt.axhline(y=target, color='green', linestyle='--', label='Target')

    plt.plot(attempts, history, color='grey', alpha=0.5)

    plt.scatter(attempts, history, c=point_cols, s=100, zorder=5)

    plt.title(f"Game History (Target: {target} & Attempts: {len(history)})")
    plt.xlabel("Attempt Number")
    plt.ylabel("Guess Value")
    plt.ylim(1,limit)

    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.show()
