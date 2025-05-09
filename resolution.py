from utils import parse_dimacs
import sys

def resolve_clauses(c1, c2):
    for lit in c1:
        if -lit in c2:
            return (c1 - {lit}) | (c2 - {-lit})
    return None

def resolution_algorithm(clauses):
    clauses = [set(c) for c in clauses]
    new = set()
    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        for (pos, neg) in pairs:
            resolvent = resolve_clauses(pos, neg)
            if resolvent is not None:
                if not resolvent:
                    return False  # empty clause → UNSAT
                new.add(frozenset(resolvent))
        if new.issubset(set(map(frozenset, clauses))):
            return True  # no new clauses → SAT
        for clause in new:
            if set(clause) not in clauses:
                clauses.append(set(clause))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python resolution.py <cnf_file>')
        sys.exit(1)
    file_path = sys.argv[1]
    clauses, variables = parse_dimacs(file_path)
    result = resolution_algorithm(clauses)
    print('SATISFIABLE' if result else 'UNSATISFIABLE')
