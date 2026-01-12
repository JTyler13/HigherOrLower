# Higher or Lower: Algorithm Simulation & Analysis

A Python-based simulation engine that models the "Higher or Lower" guessing game to empirically compare search algorithms. This project demonstrates the efficiency gap between **Randomized Search** ($2 \ln N$) and **Binary Search** ($\log_2 N$), and the **Human-Aware Bayesian Search**.

Now features an **Interactive Web Dashboard** to visualize game paths, scaling experiments, and strategy comparisons in real-time.

## Features
* **Interactive Dashboard:** A full Streamlit web application (`app.py`) allowing users to:
    * Run live simulations with adjustable parameters.
    * Inspect specific game paths visually.
    * Compare strategy efficiency on the fly.
* **Game Engine:** A reusable module (`game_engine.py`) containing the game logic for **Random**, **Optimal** and **Human-Aware Bayesian** players.
* **Human Bias Model:** A simulation that models realistic human number selection psychology (e.g., clustering around years, dates, and common patterns) for robust comparison.
* **Simulation Pipeline:** Scripts that run thousands of iterations, handling data collection and aggregation.
* **Pandas Integration:** Uses DataFrames for efficient storage and statistical analysis of game history.
* **Custom Theming:** Implements a "Minty" Bootstrap theme via `.streamlit/config.toml` for a clean UI.

## Project Structure
```text
.
├── app.py                # Main Entry Point: Streamlit Web Dashboard
├── game_engine.py        # Core library containing the logic for Random, Binary and Human-Bias logic
├── .streamlit/
│   └── config.toml       # Theme configuration (Minty Theme colors)
├── main.py               # CLI: Intro simulation (Distribution of guesses)
├── scaling.py            # CLI: Convergence analysis (Law of Large Numbers)
├── compare_strategies.py # CLI: Efficiency showdown (Random vs Optimal)
├── requirements.txt      # List of required libraries (streamlit, pandas, matplotlib)
└── README.md             # Project documentation
```

## Installation & Usage
1. Clone the repository
```Bash
git clone https://github.com/JTyler13/HigherOrLower.git
cd HigherOrLower
```

2. Install Dependencies
It is recommended to use a virtual environment.
```Bash
pip install -r requirements.txt
```

3. Run the Dashboard
To launch the web interface:
```Bash
streamlit run app.py
```
4. Run Standalone Scripts (Optional)
If you prefer running specific analyses via the terminal:
```Bash
python main.py               # Run distribution analysis
python scaling.py            # Run scaling experiment
python compare_strategies.py # Run strategy comparison
```

`This code was created in conjunction with GitHub Copilot`
