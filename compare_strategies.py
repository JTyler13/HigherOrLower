# compare_strategies.py
from game_engine import play_game, play_optimal_game
import pandas as pd
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    print("Starting Head-to-Head Comparison...")

    limits = [100, 1000, 10000, 100000, 1000000]
    results = []

    # Run 1000 simulations for each limit to get stable averages
    SIM_COUNT = 1000

    for limit in limits:
        print(f"Testing Limit: {limit}")

        # 1. Test Random Strategy (Your original code)
        random_counts = []
        for _ in range(SIM_COUNT):
            data = play_game(limit)
            random_counts.append(data['count'])
        avg_random = sum(random_counts) / len(random_counts)

        # 2. Test Optimal Strategy (The new code)
        optimal_counts = []
        for _ in range(SIM_COUNT):
            data = play_optimal_game(limit)
            optimal_counts.append(data['count'])
        avg_optimal = sum(optimal_counts) / len(optimal_counts)

        # 3. Calculate Theory (Log Base 2 for optimal)
        theory_log2 = math.log2(limit)

        results.append({
            "limit": limit,
            "Random_Avg": avg_random,
            "Optimal_Avg": avg_optimal,
            "Theory_Log2": theory_log2
        })

    # Create DataFrame
    df = pd.DataFrame(results)
    print("\n--- Final Scoreboard ---")
    print(df)

    # --- Plotting ---
    plt.figure(figsize=(10, 6))

    # X-Axis: The difficulty (Limit)
    x_values = df['limit'].astype(str)

    # Line 1: Random Player
    plt.plot(x_values, df['Random_Avg'], marker='o', label='Random (2 * ln N)', color='blue')

    # Line 2: Optimal Player
    plt.plot(x_values, df['Optimal_Avg'], marker='o', label='Optimal (Binary Search)', color='green')

    # Line 3: Theoretical Limit (Log2)
    # This should overlay almost perfectly on the Optimal line
    plt.plot(x_values, df['Theory_Log2'], linestyle='--', label='Theory (Log2 N)', color='red', alpha=0.7)

    plt.title("Efficiency Comparison: Random vs Optimal")
    plt.xlabel("Game Limit (N)")
    plt.ylabel("Average Guesses Needed")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
