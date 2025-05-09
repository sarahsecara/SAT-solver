from utils import parse_dimacs
import sys

def resolve(pos, neg, var):
    return (pos - {var}) | (neg - {-var})

def dp_algorithm(clauses, variables):
    clauses = [set(clause) for clause in clauses]
    while variables:
        var = variables.pop(0)
        pos_clauses = [c for c in clauses if var in c]
        neg_clauses = [c for c in clauses if -var in c]
        new_clauses = []
        for pos in pos_clauses:
            for neg in neg_clauses:
                resolvent = resolve(pos, neg, var)
                if not resolvent:
                    return False  
                new_clauses.append(resolvent)
        clauses = [c for c in clauses if var not in c and -var not in c]
        clauses.extend(new_clauses)
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python dp.py <cnf_file>')
        sys.exit(1)
    file_path = sys.argv[1]
    clauses, variables = parse_dimacs(file_path)
    sat = dp_algorithm(clauses, variables)
    print('SATISFIABLE' if sat else 'UNSATISFIABLE')
