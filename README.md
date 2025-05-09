# SAT Solver Comparison Project

This project implements and compares several SAT solving algorithms, including:
- **Resolution**
- **Davis–Putnam (DP)**
- **Davis–Putnam–Logemann–Loveland (DPLL)**

It also includes experimental evaluation of different heuristic strategies, such as:
- First-literal selection
- Random literal selection
- Most-frequent literal selection

##  Repository Structure

- `resolution.py`: Python script implementing the Resolution algorithm.
- `dp.py`: Python script implementing the Davis–Putnam (DP) algorithm.
- `dpll.py`: Python script implementing the DPLL algorithm with heuristics.
- `utils.py`: Shared utility functions (including DIMACS CNF parser).
- `run.py`: Master script to run experiments across multiple solvers and datasets.
- `cnf/`: Directory containing benchmark CNF files.
- `results_summary.csv`: Automatically generated file summarizing experimental results.

##  Requirements

- Python 3.x
- Standard Python libraries (no external dependencies required)

## How to Run

1. ** Run an individual solver:**
   ```bash
   python resolution.py cnf/example.cnf
   python dp.py cnf/example.cnf
   python dpll.py cnf/example.cnf [heuristic]
