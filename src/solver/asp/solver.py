from solver.sat.solver import solve_dpll
from solver.asp.translation import compute_clarks_completion, project


def solve(rules):
    atoms = set()
    for (head, body) in rules:
        for literal in head:
            atoms.add(literal.atom)

        for literal in body:
            atoms.add(literal.atom)

    atoms = list(atoms)

    original_atoms, instance = compute_clarks_completion(atoms, rules)

    solutions = solve_dpll(instance, all_solutions=True)

    return list(map(lambda s: project(s, original_atoms), solutions))