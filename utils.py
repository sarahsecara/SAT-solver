def parse_dimacs(filepath):
    clauses = []
    variables = set()
    try:
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith('c') or line.startswith('p'):
                    continue
                tokens = line.split()
                if tokens[-1] != '0':
                    raise ValueError(f"Line {line_num} missing terminating 0: {line}")
                try:
                    literals = list(map(int, tokens[:-1]))
                except ValueError:
                    raise ValueError(f"Invalid literal on line {line_num}: {line}")
                clauses.append(literals)
                for lit in literals:
                    variables.add(abs(lit))
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    return clauses, sorted(variables)
