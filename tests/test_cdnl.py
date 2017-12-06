from solver.model import *
from solver.sat.solver import solve_cdnl, analyse_conflict_1uip


def test_simple():
    a = Atom(1, "a")
    b = Atom(2, "b")

    no_goods = [
        NoGood.of(F(a), F(b))
    ]

    instance = Instance([a, b], no_goods)

    solutions = solve_cdnl(instance, all_solutions=True)

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

    assignment = solve_cdnl(instance)

    assert T(a) in assignment
    assert F(b) in assignment
    assert F(c) in assignment
    assert F(x) in assignment
    assert F(y) in assignment


def test_instances():
    from instances import INSTANCES, LARGE_INSTANCES, REALLY_LARGE_INSTANCES

    for instance, solution in INSTANCES:
        result = solve_cdnl(instance)

        assert result == solution

    for instance, is_sat in LARGE_INSTANCES + REALLY_LARGE_INSTANCES:
        result = solve_cdnl(instance)

        if is_sat:
            assert result is not None
        else:
            assert result is None


def test_1uip():
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
        NoGood.of(F(a), F(x), F(y)),
        NoGood.of(F(a), F(x))  # learned no-good
    ]

    instance = Instance(atoms, no_goods)

    assignment = Assignment.of(F(a), T(x), F(y))

    state = instance.state

    state.set_decision_level(1)

    state.set_decision_level_for(F(a), 1)
    state.set_decision_level_for(T(x), 1)
    state.set_decision_level_for(F(y), 1)

    state.set_implicant(T(x), no_goods[6])
    state.set_implicant(F(y), no_goods[2])

    learned, k = analyse_conflict_1uip(instance, assignment, no_goods[3])

    assert k == 0
    assert learned == NoGood.of(F(a))

    # assignment = solve_cdnl(instance)

    analyse_conflict_1uip