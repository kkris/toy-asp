from solver.model import *
from solver.core.solver import solve_dpll


def test_simple():
    a = Atom(1, "a")
    b = Atom(2, "b")

    no_goods = [
        NoGood.of(F(a), F(b))
    ]

    instance = Instance([a, b], no_goods)

    solutions = solve_dpll(instance, all_solutions=True)

    assert len(solutions) == 3

def test_example():
    a = Atom(1, "a")
    b = Atom(2, "b")
    c = Atom(3, "c")
    x = Atom(4, "x")
    y = Atom(5, "y")

    atoms = [a, b, c, x, y]

    no_goods = [
        NoGood.of(T(a), T(b)),
        NoGood.of(T(a), T(c)),
        NoGood.of(F(a), T(x), T(y)),
        NoGood.of(F(a), T(x), F(y)),
        NoGood.of(F(a), F(x), T(y)),
        NoGood.of(F(a), F(x), F(y))
    ]

    instance = Instance(atoms, no_goods)

    assignment = solve_dpll(instance)

    assert T(a) in assignment
    assert F(b) in assignment
    assert F(c) in assignment
    assert F(x) in assignment
    assert F(y) in assignment


def test_instances():
    from instances import INSTANCES, LARGE_INSTANCES

    for instance, solution in INSTANCES:
        result = solve_dpll(instance)

        assert result == solution

    for instance, is_sat in LARGE_INSTANCES[:3]:
        result = solve_dpll(instance)

        if is_sat:
            assert result is not None
        else:
            assert result is None
