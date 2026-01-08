# Higher or Lower Game

# Here we are building a version of 'Higher or Lower', whereby the game will pick a random number between 1 and n (n provided by the user) and then randomly guess numbers until it reaches the correct choice. This is not the optimal way of playing the game (i.e. splitting the options in half every guess), but does give an interesting insight into a random method.

#### Import packages ####
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

#### Game functions ####
def play_game(upper_bound=10, fixed_target=None):
    """
    Plays the 'Random Choice' model.
    It guesses randomly, but respects the feedback (High/Low) to narrow the range.
    """
    current_guess = 0
    guesses = []

    # Allow a pre-set target (e.g., from Human choice), otherwise random
    if fixed_target is None:
        target = random.randint(1, upper_bound)
    else:
        target = fixed_target

    p1 = 1
    p2 = upper_bound

    while current_guess != target:
        # Guess a random number within the current valid range
        current_guess = random.randint(p1, p2)
        guesses.append(current_guess)

        if current_guess == target:
            break
        elif current_guess > target:
            p2 = current_guess - 1
        else:
            p1 = current_guess + 1

    return {
        "target": target,
        "count": len(guesses),
        "history": guesses,
        "limit": upper_bound
    }

def play_optimal_game(upper_bound=10, fixed_target=None):
    current_guess = 0
    guesses = []

    if fixed_target is None:
        target = random.randint(1, upper_bound)
    else:
        target = fixed_target # Use the pre-selected "Human" target

    p1 = 1
    p2 = upper_bound

    while current_guess != target:
        current_guess = (p1 + p2) // 2
        guesses.append(current_guess)
        if current_guess == target:
            break
        elif current_guess > target:
            p2 = current_guess - 1
        else:
            p1 = current_guess + 1

    return {
        "target": target,
        "count": len(guesses),
        "history": guesses,
        "limit": upper_bound
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

#### Human Influence ####

def get_human_probabilities(limit):
    """
    Creates a probability distribution that mimics human bias.
    Optimized for LARGE limits using 'PIN Code' psychology.
    """
    weights = np.ones(limit + 1)  # Start with uniform weights

    # ---------------------------------------------------------
    # 1. THE "YEAR" BIAS (The strongest signal in large ranges)
    # ---------------------------------------------------------
    # People heavily prefer years relevant to their lives (1950-2025).
    current_year = 2026
    start_year = 1950

    if limit >= start_year:
        effective_end = min(limit, current_year)
        if effective_end > start_year:
            # Massive 8x boost for modern years
            weights[start_year : effective_end + 1] *= 8.0

    # ---------------------------------------------------------
    # 2. THE "DATE" BIAS (MMDD format)
    # ---------------------------------------------------------
    # If the limit allows, people pick dates like 1225 (Dec 25).
    # This affects numbers 101 to 1231 heavily.
    if limit >= 101:
        # Boost valid MMDD ranges roughly
        # We'll just boost the whole block 100-1231 for simplicity,
        # or we could get fancy and only boost valid dates.
        # Let's boost the block:
        date_limit = min(limit, 1231)
        if date_limit > 100:
            weights[100 : date_limit + 1] *= 3.0

    # ---------------------------------------------------------
    # 3. LOW NUMBER BIAS (1-31)
    # ---------------------------------------------------------
    # Birthdays (Day only) are still huge.
    if limit >= 31:
        weights[1:32] *= 4.0

    # ---------------------------------------------------------
    # 4. PATTERN & REPEATED DIGITS (PIN Codes)
    # ---------------------------------------------------------
    # Humans love 1111, 2222, 1234, etc.
    patterns = [
        # Sequences
        123, 1234, 12345, 2345, 3456, 4567, 5678, 6789,
        # Repetitions
        111, 222, 333, 444, 555, 666, 777, 888, 999,
        1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999,
        # Famous/Meme numbers
        42, 69, 420, 666, 1337, 8008, 6969
    ]

    for p in patterns:
        if p <= limit:
            weights[p] *= 5.0  # Big spike for specific patterns

    # ---------------------------------------------------------
    # 5. ROUND NUMBER AVOIDANCE (The "Randomness" Fallacy)
    # ---------------------------------------------------------
    # Humans think 5000 is "not random enough", so they pick 4892.
    for i in range(1, limit + 1):
        if i % 1000 == 0:
            weights[i] *= 0.1  # Crush clean thousands
        elif i % 100 == 0:
            weights[i] *= 0.3  # Punish clean hundreds

    # Normalize so they sum to 1
    probabilities = weights[1:] / weights[1:].sum()
    return probabilities

def play_human_game(upper_bound=100):
    """
    Simulates a target chosen by a HUMAN (biased).
    Runs both Optimal (Binary) and Random Choice models against this target.
    """
    # 1. Generate the Human Target
    probs = get_human_probabilities(upper_bound)
    target = np.random.choice(range(1, upper_bound + 1), p=probs)

    # 2. Run Optimal Strategy against this target
    # (We cast target to int because numpy types can sometimes cause issues)
    optimal_result = play_optimal_game(upper_bound, fixed_target=int(target))

    # 3. Run Random Choice Strategy against the SAME target
    random_result = play_game(upper_bound, fixed_target=int(target))

    # 4. Return both results
    return {
        "optimal": optimal_result,
        "random": random_result
    }

def play_bayesian_game(upper_bound=100):
    """
    Simulates a target chosen by a HUMAN (biased).
    The computer plays using BAYESIAN Search (exploiting the bias).
    """
    probs = get_human_probabilities(upper_bound)
    target = np.random.choice(range(1, upper_bound + 1), p=probs)

    current_guess = 0
    guesses = []

    # We maintain the current valid range
    low = 1
    high = upper_bound

    # Get the CDF (Cumulative Distribution Function) to find the median
    # We re-normalize the probabilities inside the current window [low, high]

    while current_guess != target:
        # 1. Slice the probability distribution for the current valid range
        # Note: adjust for 0-based indexing of arrays vs 1-based numbers
        current_probs = probs[low-1 : high]

        # 2. Normalize so it sums to 1
        current_probs = current_probs / current_probs.sum()

        # 3. Calculate Cumulative Sum
        cdf = np.cumsum(current_probs)

        # 4. Find the Median (where CDF crosses 0.5)
        # This is the point that splits the *probability mass* in half, not just the range
        median_index = np.searchsorted(cdf, 0.5)
        current_guess = low + median_index

        guesses.append(int(current_guess))

        if current_guess == target:
            break
        elif current_guess > target:
            high = current_guess - 1
        else:
            low = current_guess + 1

    return {
        "target": target,
        "count": len(guesses),
        "history": guesses,
        "limit": upper_bound
    }
