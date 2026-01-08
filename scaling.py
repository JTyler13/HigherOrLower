# scaling_v2.py
from game_engine import play_game
import math
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Starting Multi-Variable Scaling Experiment...")

    # Parameters
    limits_to_test = [100, 1000, 10000, 100000]
    sim_counts_to_test = [10, 50, 100, 500, 1000, 5000, 10000, 20000]

    # We will store the SUMMARY data here (not every single game)
    summary_data = []

    for limit in limits_to_test:
        print(f"Running games for Limit: {limit}...")

        max_sims = max(sim_counts_to_test)
        current_batch = []

        for _ in range(max_sims):
            result = play_game(limit)
            current_batch.append(result['count'])

        # 2. Convert this batch to a Series for easy math
        batch_series = pd.Series(current_batch)
        theoretical = 2 * math.log(limit)

        # 3. "Slice" the data for each simulation size we want to test
        for n in sim_counts_to_test:
            # Take the first 'n' games
            subset = batch_series.head(n)
            avg = subset.mean()

            # Store the aggregate result
            summary_data.append({
                "limit": limit,
                "n_simulations": n,
                "observed_avg": avg,
                "theoretical": theoretical,
                "ratio": avg / theoretical
            })

    # Create the Summary DataFrame
    df_summary = pd.DataFrame(summary_data)

    print("\n--- Experiment Complete ---")
    print(df_summary)

    # --- Plotting ---
    # We want a line plot: X=Simulations, Y=Ratio, Color=Limit
    plt.figure(figsize=(10, 6))

    # We loop through the limits to draw one line per limit
    for limit in limits_to_test:
        subset = df_summary[df_summary['limit'] == limit]
        plt.plot(subset['n_simulations'], subset['ratio'], marker='o', label=f"Limit {limit}")

    plt.axhline(1.0, color='red', linestyle='--', label="Theory (1.0)")

    # Log scale makes it easier to see the jump from 10 to 10000
    plt.xscale('log')

    plt.title("Convergence of Estimate by Simulation Count")
    plt.xlabel("Number of Simulations (Log Scale)")
    plt.ylabel("Ratio (Observed / Theory)")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.show()
