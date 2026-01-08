# Higher or Lower: Algorithm Simulation & Analysis

A Python-based simulation engine that models the "Higher or Lower" guessing game to empirically compare search algorithms. This project demonstrates the efficiency gap between **Randomized Search** ($2 \ln N$) and **Binary Search** ($\log_2 N$).

Now features an **Interactive Web Dashboard** to visualize game paths, scaling experiments, and strategy comparisons in real-time.

## 📊 The Analysis
The core of this project is a simulation script that runs thousands of games to visualize algorithmic complexity.

**Key Findings:**
* **Random Guessing:** Follows a $2 \ln N$ efficiency curve (approx. 27 guesses for 1,000,000 numbers).
* **Optimal Strategy:** Uses Binary Search to achieve $\log_2 N$ efficiency (approx. 20 guesses for 1,000,000 numbers).
* **Law of Large Numbers:** The simulation demonstrates how the observed average converges to the theoretical limit as $N$ increases.

## 🚀 Features
* **Interactive Dashboard:** A full Streamlit web application (`app.py`) allowing users to:
    * Run live simulations with adjustable parameters.
    * Inspect specific game paths visually.
    * Compare strategy efficiency on the fly.
* **Game Engine:** A reusable module (`game_engine.py`) containing the game logic for both Random and Optimal players.
* **Simulation Pipeline:** Scripts that run thousands of iterations, handling data collection and aggregation.
* **Pandas Integration:** Uses DataFrames for efficient storage and statistical analysis of game history.
* **Custom Theming:** Implements a "Minty" Bootstrap theme via `.streamlit/config.toml` for a clean UI.

## 📂 Project Structure
```text
.
├── app.py                # Main Entry Point: Streamlit Web Dashboard
├── game_engine.py        # Core library containing the logic for Random and Binary Search players
├── .streamlit/
│   └── config.toml       # Theme configuration (Minty Theme colors)
├── main.py               # CLI: Intro simulation (Distribution of guesses)
├── scaling.py            # CLI: Convergence analysis (Law of Large Numbers)
├── compare_strategies.py # CLI: Efficiency showdown (Random vs Optimal)
├── requirements.txt      # List of required libraries (streamlit, pandas, matplotlib)
└── README.md             # Project documentation
```

## 🛠️ Installation & Usage
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
