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
├── game_engine.py      # Contains play_game() and play_optimal_game() logic
├── main.py             # The simulation script (runs the experiments)
├── requirements.txt    # Dependencies (pandas, matplotlib)
└── README.md           # This file
```

## 🛠️ Installation & Usage
Clone the repository
```Bash
git clone [https://github.com/YourUsername/HigherOrLower.git](https://github.com/YourUsername/HigherOrLower.git)
cd HigherOrLower
```

Install Dependencies It is recommended to use a virtual environment.
```Bash
pip install -r requirements.txt
```

Run the Simulation To run the head-to-head comparison:
```Bash
python main.py
```

## 🧠 What I Learned
- **Python Modules:** Refactoring code into reusable modules (game_engine) vs execution scripts.

- **List Comprehensions:** Replacing R-style loops with Pythonic list construction.

- **Pandas vs R:** Translating tidyverse concepts into Pandas DataFrames.

- **Algorithmic Complexity:** Empirically proving Big O notation through simulation.

`This code was created in conjunction with GitHub Copilot`
