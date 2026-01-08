# Higher or Lower: Algorithm Simulation & Analysis

A Python-based simulation engine that models the "Higher or Lower" guessing game to empirically compare search algorithms. This project demonstrates the efficiency gap between **Randomized Search** ($2 \ln N$) and **Binary Search** ($\log_2 N$).

## 📊 The Analysis
The core of this project is a simulation script that runs thousands of games to visualize algorithmic complexity.

**Key Findings:**
* **Random Guessing:** Follows a $2 \ln N$ efficiency curve (approx. 27 guesses for 1,000,000 numbers).
* **Optimal Strategy:** Uses Binary Search to achieve $\log_2 N$ efficiency (approx. 20 guesses for 1,000,000 numbers).
* **Law of Large Numbers:** The simulation demonstrates how the observed average converges to the theoretical limit as $N$ increases.

## 🚀 Features
* **Game Engine:** A reusable module (`game_engine.py`) containing the game logic for both Random and Optimal players.
* **Simulation Pipeline:** A script that runs thousands of iterations, handling data collection and aggregation.
* **Pandas Integration:** Uses DataFrames for efficient storage and statistical analysis of game history.
* **Visualization:** Matplotlib scripts to generate convergence charts and efficiency comparisons.

## 📂 Project Structure
```text
.
├── game_engine.py        # Core library containing the logic for Random and Binary Search players
├── main.py               # Intro simulation: Runs 1,000 games and visualizes the distribution of guesses
├── scaling.py            # Convergence analysis: Demonstrates the Law of Large Numbers as N increases
├── compare_strategies.py # Efficiency showdown: Plots Random Search (2 ln N) vs Optimal Binary Search (log2 N)
├── requirements.txt      # List of required Python libraries (pandas, matplotlib)
└── README.md             # Project documentation and summary of findings
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

3. Run the Simulations
- Intro Simulation (Distribution of Guesses):
```Bash
python main.py
```
- Convergence Analysis (Scaling Experiment):
```Bash
python scaling.py
```
- Head-to-Head Comparison (Random Vs Optimal):
```Bash
python compare_strategies.py
```

## 🧠 What I Learned
- **Python Modules:** Refactoring code into reusable modules (game_engine) vs execution scripts.

- **List Comprehensions:** Replacing R-style loops with Pythonic list construction.

- **Pandas vs R:** Translating tidyverse concepts into Pandas DataFrames.

- **Algorithmic Complexity:** Empirically proving Big O notation through simulation.

`This code was created in conjunction with GitHub Copilot`
