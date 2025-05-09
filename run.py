import subprocess
import time
import os
import csv

solvers = {
    'DP': 'dp.py',
    'DPLL': 'dpll.py',
    'Resolution': 'resolution.py'
}

cnf_folder = 'cnf'
output_file = 'results_summary.csv'

# Collect .cnf files safely
try:
    cnf_files = [f for f in os.listdir(cnf_folder) if f.endswith('.cnf')]
except FileNotFoundError:
    print(f"Error: Folder '{cnf_folder}' not found.")
    exit(1)

if not cnf_files:
    print(f"No .cnf files found in '{cnf_folder}'.")
    exit(1)

with open(output_file, mode='w', newline='') as csvfile:
    fieldnames = ['CNF File', 'Solver', 'Result', 'Time (seconds)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for cnf_file in cnf_files:
        cnf_path = os.path.join(cnf_folder, cnf_file)
        print(f"\n=== Testing on {cnf_file} ===")
        for solver_name, solver_script in solvers.items():
            print(f"--- {solver_name} ---")
            start = time.time()
            try:
                result = subprocess.run(
                    ['python', solver_script, cnf_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=60
                )
                end = time.time()
                runtime = end - start

                # Get meaningful output or fallback error
                output = result.stdout.strip()
                if not output:
                    output = result.stderr.strip()
                if not output:
                    output = "No output"

                print(f"Result: {output}")
                print(f"Time: {runtime:.4f} seconds")

                writer.writerow({
                    'CNF File': cnf_file,
                    'Solver': solver_name,
                    'Result': output,
                    'Time (seconds)': f"{runtime:.4f}"
                })

            except subprocess.TimeoutExpired:
                print(f"{solver_name} timed out after 60 seconds.")
                writer.writerow({
                    'CNF File': cnf_file,
                    'Solver': solver_name,
                    'Result': 'TIMEOUT',
                    'Time (seconds)': '60.0000'
                })

            except Exception as e:
                print(f"Error running {solver_name} on {cnf_file}: {e}")
                writer.writerow({
                    'CNF File': cnf_file,
                    'Solver': solver_name,
                    'Result': f'ERROR: {e}',
                    'Time (seconds)': 'N/A'
                })

print(f"\nSummary written to {output_file}")
