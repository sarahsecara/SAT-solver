from utils import parse_dimacs
from collections import Counter
import random
import sys

def unit_clause_simplify(clauses, assignment):
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            if len(clause) == 1:
                lit = next(iter(clause))
                assignment.add(lit)
                clauses = simplify(clauses, lit)
                changed = True
                break
    return clauses, assignment

def simplify(clauses, lit):
    new_clauses = []
    for clause in clauses:
        if lit in clause:
            continue
        if -lit in clause:
            new_clause = clause - {-lit}
            if not new_clause:
                return [[]]
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

def select_variable(clauses, heuristic):
    if heuristic == 'random':
        literals = list(set(abs(lit) for clause in clauses for lit in clause))
        return random.choice(literals)
    elif heuristic == 'most_frequent':
        counts = Counter(abs(lit) for clause in clauses for lit in clause)
        if counts:
            most_common, _ = counts.most_common(1)[0]
            return most_common
        else:
            return None
    else:
        for clause in clauses:
            for lit in clause:
                return abs(lit)
        return None

def dpll(clauses, assignment, heuristic):
    clauses, assignment = unit_clause_simplify(clauses, assignment)
    if [] in clauses:
        return False
    if not clauses:
        return True

    var = select_variable(clauses, heuristic)
    if var is None:
        return False

    return dpll(simplify(clauses, var), assignment | {var}, heuristic) or \
           dpll(simplify(clauses, -var), assignment | {-var}, heuristic)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python dpll.py <cnf_file> [heuristic]')
        sys.exit(1)

    file_path = sys.argv[1]
    heuristic = sys.argv[2] if len(sys.argv) > 2 else 'first'

    clauses, variables = parse_dimacs(file_path)
    clauses = [set(clause) for clause in clauses]

    result = dpll(clauses, set(), heuristic)
    print('SATISFIABLE' if result else 'UNSATISFIABLE')
