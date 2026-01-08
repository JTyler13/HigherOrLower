import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import math
from game_engine import play_game, play_optimal_game, play_human_game, play_bayesian_game, get_human_probabilities

# --- GLOBAL CONFIGURATION ---
# Change these values to resize ALL plots at once
PLOT_CONFIG = {
    "figsize": (15, 7.5),   # Width, Height in inches
    "dpi": 250           # Resolution
}
# ----------------------------

st.set_page_config(page_title="Higher or Lower Analysis", layout="wide")

st.title("🎲 Higher or Lower: The Mathematics of Guessing")
st.markdown("Explore the efficiency of random guessing strategies vs. optimal strategies.")

# Helper function to draw the game plot safely for Streamlit
def draw_game_safe(result):
    """
    Re-implements the logic from plot_game but returns a Figure object.
    """
    history = result['history']
    target = result['target']
    limit = result['limit']
    attempts = range(1, len(history) + 1)

    point_cols = []
    for guess in history:
        if guess > target:
            point_cols.append('red')
        elif guess < target:
            point_cols.append('blue')
        else:
            point_cols.append('green')

    # USE GLOBAL CONFIG
    fig, ax = plt.subplots(figsize=PLOT_CONFIG["figsize"], dpi=PLOT_CONFIG["dpi"])

    ax.axhline(y=target, color='green', linestyle='--', label='Target')
    ax.plot(attempts, history, color='grey', alpha=0.5)
    ax.scatter(attempts, history, c=point_cols, s=80, zorder=5)

    ax.set_title(f"Game History (Target: {target} | Attempts: {len(history)})")
    ax.set_xlabel("Attempt Number")
    ax.set_ylabel("Guess Value")
    ax.set_ylim(1, limit)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    return fig

# Create the tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Distribution",
    "🔍 Game Inspector",
    "📈 Scaling Convergence",
    "⚔️ Strategy Compare",
    "🧠 Human Mode"
])

# --- TAB 1: Distribution Analysis ---
with tab1:
    st.header("Simulation Distribution")
    st.write("Run a batch of games to see the probability distribution of guesses needed.")

    col1, col2 = st.columns(2)
    with col1:
        sim_limit = st.number_input("Upper Bound (N)", min_value=10, value=10000, step=100)
    with col2:
        sim_count = st.slider("Number of Games to Simulate", 100, 5000, 1000)

    if st.button("Run Simulation", key="btn_sim"):
        with st.spinner("Simulating..."):
            results = [play_game(sim_limit) for _ in range(sim_count)]
            df_dist = pd.DataFrame(results)

            avg_attempts = df_dist['count'].mean()
            theoretical = 2 * math.log(sim_limit)

            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Average Guesses", f"{avg_attempts:.2f}")
            m2.metric("Theoretical (2 * ln N)", f"{theoretical:.2f}")
            m3.metric("Max Guesses", df_dist['count'].max())

            # PLOTTING WITH GLOBAL CONFIG
            fig, ax = plt.subplots(figsize=PLOT_CONFIG["figsize"], dpi=PLOT_CONFIG["dpi"])

            df_dist['count'].hist(bins=range(1, df_dist['count'].max() + 2),
                                ax=ax, edgecolor='black', alpha=0.7)
            ax.axvline(avg_attempts, color='red', linestyle='dashed', label=f'Mean: {avg_attempts:.2f}')
            ax.set_title(f"Distribution of Guesses (N={sim_limit})")
            ax.set_xlabel("Guesses Needed")
            ax.set_ylabel("Frequency")
            ax.legend()

            # Center the plot
            c1, c2, c3 = st.columns([1, 4, 1])
            with c2:
                st.pyplot(fig, width="content")

            st.session_state['df_dist'] = df_dist
            st.session_state['sim_limit'] = sim_limit

# --- TAB 2: Game Inspector ---
with tab2:
    st.header("Visualizing the Path")

    inspect_mode = st.radio("Choose Game to Inspect:",
                            ["Play New Random Game", "View Unluckiest from Batch (Tab 1)"])

    if inspect_mode == "Play New Random Game":
        insp_limit = st.number_input("Game Limit", value=100, step=10, key="insp_limit")
        if st.button("Play & Plot"):
            result = play_game(insp_limit)
            fig = draw_game_safe(result)

            c1, c2, c3 = st.columns([1, 4, 1])
            with c2:
                st.pyplot(fig, width="content")

    elif inspect_mode == "View Unluckiest from Batch (Tab 1)":
        if 'df_dist' in st.session_state:
            df = st.session_state['df_dist']
            max_attempts = df['count'].max()
            worst_game = df[df['count'] == max_attempts].iloc[0]

            st.info(f"Showing a game that took {max_attempts} guesses!")

            worst_game_data = {
                "history": worst_game['history'],
                "target": worst_game['target'],
                "limit": sim_limit if 'sim_limit' in locals() else 10000,
                "count": worst_game['count']
            }

            fig = draw_game_safe(worst_game_data)

            c1, c2, c3 = st.columns([1, 4, 1])
            with c2:
                st.pyplot(fig, width="content")
        else:
            st.warning("Please run a simulation in Tab 1 first.")

# --- TAB 3: Scaling ---
with tab3:
    st.header("Convergence of Theory")
    st.write("How many simulations do we need before the average matches the theory?")

    if st.button("Run Scaling Experiment"):
        with st.spinner("Crunching numbers..."):
            limits_to_test = [100, 1000, 10000]
            sim_counts = [10, 50, 100, 500, 1000, 5000]
            summary_data = []

            progress_bar = st.progress(0)
            total_steps = len(limits_to_test)
            step_counter = 0

            for limit in limits_to_test:
                max_sims = max(sim_counts)
                current_batch = [play_game(limit)['count'] for _ in range(max_sims)]
                batch_series = pd.Series(current_batch)
                theoretical = 2 * math.log(limit)

                for n in sim_counts:
                    subset_avg = batch_series.head(n).mean()
                    summary_data.append({
                        "limit": limit,
                        "n_simulations": n,
                        "ratio": subset_avg / theoretical
                    })
                step_counter += 1
                progress_bar.progress(step_counter / total_steps)

            df_scale = pd.DataFrame(summary_data)

            # PLOTTING WITH GLOBAL CONFIG
            fig, ax = plt.subplots(figsize=PLOT_CONFIG["figsize"], dpi=PLOT_CONFIG["dpi"])

            for limit in limits_to_test:
                subset = df_scale[df_scale['limit'] == limit]
                ax.plot(subset['n_simulations'], subset['ratio'], marker='o', label=f"Limit {limit}")

            ax.axhline(1.0, color='red', linestyle='--', label="Theory (1.0)")
            ax.set_xscale('log')
            ax.set_title("Convergence of Estimate")
            ax.set_xlabel("Number of Simulations (Log Scale)")
            ax.set_ylabel("Ratio (Observed / Theory)")
            ax.legend()
            ax.grid(True, which="both", ls="-", alpha=0.2)

            c1, c2, c3 = st.columns([1, 4, 1])
            with c2:
                st.pyplot(fig, width="content")

# --- TAB 4: Strategy Comparison ---
with tab4:
    st.header("Random vs. Optimal Strategy")
    st.write("Comparing the 'Random' approach against a Binary Search.")

    if st.button("Run Comparison"):
        with st.spinner("Comparing strategies..."):
            comp_limits = [100, 1000, 10000, 100000]
            comp_results = []

            for limit in comp_limits:
                r_avg = sum([play_game(limit)['count'] for _ in range(50)]) / 50
                o_avg = sum([play_optimal_game(limit)['count'] for _ in range(50)]) / 50

                comp_results.append({
                    "limit": limit,
                    "Random": r_avg,
                    "Optimal": o_avg,
                    "Theory (Log2)": math.log2(limit)
                })

            df_comp = pd.DataFrame(comp_results)

            # --- INFOGRAPHICS ---
            hardest_data = df_comp.iloc[-1]
            max_limit_val = int(hardest_data['limit'])

            st.subheader(f"Results for N = {max_limit_val:,}")

            k1, k2, k3 = st.columns(3)
            k1.metric("Random Strategy Avg", f"{hardest_data['Random']:.1f}", "Inefficient", delta_color="inverse")
            k2.metric("Optimal Strategy Avg", f"{hardest_data['Optimal']:.1f}", "Best Possible", delta_color="normal")
            ratio = hardest_data['Random'] / hardest_data['Optimal']
            k3.metric("Speed Multiplier", f"{ratio:.1f}x Faster", "Optimal is faster")

            st.divider()

            # PLOTTING WITH GLOBAL CONFIG
            fig, ax = plt.subplots(figsize=PLOT_CONFIG["figsize"], dpi=PLOT_CONFIG["dpi"])

            x_vals = df_comp['limit'].astype(str)
            ax.plot(x_vals, df_comp['Random'], marker='o', label='Random', color='blue')
            ax.plot(x_vals, df_comp['Optimal'], marker='o', label='Optimal', color='green')
            ax.plot(x_vals, df_comp['Theory (Log2)'], linestyle='--', label='Theory', color='red', alpha=0.5)

            ax.set_title("Efficiency Comparison")
            ax.set_ylabel("Average Guesses")
            ax.set_xlabel("Game Limit (N)")
            ax.legend()
            ax.grid(True, alpha=0.3)

            c1, c2, c3 = st.columns([1, 4, 1])
            with c2:
                st.pyplot(fig, width="content")

            with st.expander("View Raw Data"):
                st.dataframe(df_comp)

# --- TAB 5: Human Mode ---
with tab5:
    st.header("The Human Element")
    st.write("Humans are not random. We prefer birthdays (1-31), odd numbers, and 'lucky' numbers.")

    h_limit = st.number_input(
        "Range Limit",
        value=100,
        min_value=10,
        max_value=5000,
        step=10,
        key="human_limit"
    )

    # 1. Visualize the Bias
    probs = get_human_probabilities(h_limit)
    df_bias = pd.DataFrame({
        "Number": range(1, h_limit + 1),
        "Probability": probs
    })

    st.subheader("The 'Human' Probability Distribution")
    st.write("Peaks indicate numbers humans are more likely to pick (e.g., dates, primes).")

    # PLOTTING WITH GLOBAL CONFIG
    fig, ax = plt.subplots(figsize=PLOT_CONFIG["figsize"], dpi=PLOT_CONFIG["dpi"])
    ax.bar(df_bias["Number"], df_bias["Probability"], color='purple', alpha=0.7)
    ax.set_xlabel("Number Selection")
    ax.set_ylabel("Probability")
    ax.set_title(f"Human Bias Model (1-{h_limit})")

    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.pyplot(fig, width="content")

    # 2. Run Head-to-Head-to-Head
    st.divider()
    st.subheader("Strategy Showdown")
    st.write("Comparing strategies against a Human opponent (Simulating 5,000 Games).")

    if st.button("Run Large Experiment"):
        with st.spinner("Simulating 5,000 games (this may take a moment)..."):
            n_games = 5000  # Increased from 1,000

            # Storage for results
            random_scores = []
            standard_scores = []
            bayesian_scores = []

            for _ in range(n_games):
                # Run the Human Game
                human_results = play_human_game(h_limit)

                # Extract scores
                random_scores.append(human_results['random']['count'])
                standard_scores.append(human_results['optimal']['count'])
                bayesian_scores.append(play_bayesian_game(h_limit)['count'])

            # Calculate Averages
            avg_random = sum(random_scores) / n_games
            avg_standard = sum(standard_scores) / n_games
            avg_bayesian = sum(bayesian_scores) / n_games

            # --- DISPLAY METRICS ---
            c1, c2, c3 = st.columns(3)

            c1.metric("Random Guessing", f"{avg_random:.2f}", "Baseline", delta_color="off")
            c2.metric("Standard Binary", f"{avg_standard:.2f}", f"{(avg_random - avg_standard):.2f} faster than random", delta_color="normal")
            c3.metric("Bayesian Search", f"{avg_bayesian:.2f}", f"{(avg_standard - avg_bayesian):.2f} faster than binary", delta_color="normal")

            # --- DENSITY PLOT ---
            st.subheader("Probability Density of Guesses")
            st.caption("Note: 'Random' is excluded from the plot as it averages ~50 guesses, which would distort the scale.")

            # Create a DataFrame for easy plotting
            df_density = pd.DataFrame({
                'Standard (Binary)': standard_scores,
                'Bayesian (Human-Aware)': bayesian_scores
            })

            fig, ax = plt.subplots(figsize=PLOT_CONFIG["figsize"], dpi=PLOT_CONFIG["dpi"])

            # Kernel Density Estimate (KDE) plot
            df_density.plot(kind='density', ax=ax, linewidth=2)

            # Fill the area under the curves for better visuals
            # (We use a little numpy trickery to get the data from the plot lines)
            lines = ax.get_lines()

            # Fill Standard
            x_std, y_std = lines[0].get_data()
            ax.fill_between(x_std, y_std, alpha=0.2, color='blue')

            # Fill Bayesian
            x_bay, y_bay = lines[1].get_data()
            ax.fill_between(x_bay, y_bay, alpha=0.2, color='orange')

            ax.set_title("Performance Density: Standard vs. Bayesian")
            ax.set_xlabel("Number of Guesses Needed")
            ax.set_xlim(0, 20) # Focus on the relevant range for intelligent algorithms
            ax.grid(True, alpha=0.3)

            c1, c2, c3 = st.columns([1, 4, 1])
            with c2:
                st.pyplot(fig, width="content")

            improvement = (1 - avg_bayesian/avg_standard) * 100
            st.success(f"Bayesian Search is consistently shifting the curve to the left, resulting in a {improvement:.1f}% efficiency gain!")
