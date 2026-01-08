# Higher or Lower Game Analysis

# main.py
from game_engine import play_game, plot_game
import math
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 1. Setup
    print("Starting simulation...")
    count = 1000
    limit = 10000
    results = []

    # 2. The Loop
    for _ in range(count):
        data = play_game(limit)
        results.append(data)

    # 3. Create DataFrame
    df = pd.DataFrame(results)

    # 4. Basic Analysis
    print("--- Simulation Results ---")
    print(df.describe())

    # Calculate the average attempts
    avg_attempts = df['count'].mean()
    print(f"\nAverage Attempts: {avg_attempts:.2f}")
    print(f"2*ln(N): {2*math.log(limit):.2f}")

# 5. Plotting
    plt.figure(figsize=(10,6))

    df['count'].hist(bins=range(1, 30), edgecolor='black', alpha=0.7)

    plt.title(f"Distribution of Guesses (N={count}, Limit={limit})")
    plt.xlabel("Number of Attempts")
    plt.ylabel("Frequency")
    plt.axvline(avg_attempts, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {avg_attempts:.2f}')
    plt.legend()
    plt.show()


    # 6. Outlier Analysis (The Unluckiest Game)
    max_attempts = df['count'].max()
    print(f"\nMax Attempts observed: {max_attempts}")

    # Find the row(s) where count == max_attempts
    worst_games = df[df['count'] == max_attempts]

    # Grab the raw dictionary of the first matching game
    worst_game_data = {
        "history": worst_games.iloc[0]['history'],
        "target": worst_games.iloc[0]['target'],
        "limit": limit
    }
    print("Plotting the unluckiest game...")
    plot_game(worst_game_data)
