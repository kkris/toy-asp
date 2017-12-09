import os
import argparse

from solver.parser.dimacs import parse as parse_dimacs
from solver.sat.solver import solve_cdnl, solve_dpll


def parse_arguments():
    parser = argparse.ArgumentParser(description='SAT/ASP solver')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sat", action="store_true", help="Solve the given sat instance")
    group.add_argument("--asp", action="store_true", help="Solve the given (ground) asp instance")

    bt_group = parser.add_mutually_exclusive_group(required=True)
    bt_group.add_argument("--dpll", action="store_true", help="DPLL-style backtracking")
    bt_group.add_argument("--cdnl", action="store_true", help="Conflict-driven backtracking with nogood learning")

    parser.add_argument("--instance", type=str, required=True)

    return parser.parse_args()


def display_sat_solution(solution):
    literals = sorted(solution, key=lambda l: l.atom.repr)

    s = ""
    for literal in literals:
        if literal.is_positive():
            s += str(literal.atom)
        else:
            s += "-" + str(literal.atom)

        s += " "

    print(s)


def solve_sat(args):
    with open(args.instance) as fh:
        instance, _ = parse_dimacs(fh.read())

    import logging
    instance.logger.setLevel(logging.ERROR)

    if args.dpll:
        solutions = solve_dpll(instance, all_solutions=True)
    else:
        solutions = solve_cdnl(instance)

    unsat = True
    for solution in solutions:

        # verify solution
        for no_good in instance.no_goods:
            if solution.contains(no_good):
                print("Found wrong solution:")
                display_sat_solution(solution)
                return

        display_sat_solution(solution)
        unsat = False

    if unsat:
        print("Instance is unsatisfiable")


def solve_asp(args):
    pass


def main():
    args = parse_arguments()

    if not os.path.exists(args.instance):
        print("Instance '{}' does not exist.".format(args.instance))
        return

    if args.sat:
        solve_sat(args)
    else:
        solve_asp(args)


if __name__ == '__main__':
    main()