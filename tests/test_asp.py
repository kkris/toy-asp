from solver.model import *
from solver.asp.solver import solve


def test_example():
    a = Atom(1, "a")
    b = Atom(2, "b")

    rules = [
        ([T(a)], [T(b)]),
        ([T(b)], [T(a)])
    ]

    solutions = solve(rules)

    assert len(solutions) == 2
    assert Assignment.of(F(a), F(b)) in solutions
    assert Assignment.of(T(a), T(b)) in solutions


def test_facts():
    a = Atom(1, "a")
    b = Atom(2, "b")
    c = Atom(3, "c")
    d = Atom(4, "d")

    rules = [
        ([T(a)], []),
        ([T(b)], []),
        ([T(c)], [T(d)])
    ]

    solutions = solve(rules)

    assert len(solutions) == 1
    assert Assignment.of(T(a), T(b), F(c), F(d)) == solutions[0]


def test_negation():
    a = Atom(1, "a")
    b = Atom(2, "b")

    rules = [
        ([T(a)], [F(b)]),
        ([T(b)], [])
    ]

    solutions = solve(rules)

    assert len(solutions) == 1
    assert Assignment.of(F(a), T(b)) == solutions[0]


def test_ewbs_1():
    man = Atom(1, "man")
    single = Atom(2, "single")
    husband = Atom(3, "husband")

    rules = [
        ([T(man)], []),
        ([T(single)], [T(man), F(husband)]),
        ([T(husband)], [T(man), F(single)])
    ]

    solutions = solve(rules)

    assert len(solutions) == 2
    assert Assignment.of(T(man), T(single), F(husband)) in solutions
    assert Assignment.of(T(man), F(single), T(husband)) in solutions


def test_killing_clause():
    p = Atom(1, "p")
    rules = [
        ([T(p)], [F(p)]),
    ]

    solutions = solve(rules)

    assert len(solutions) == 0


def test_instances():
    from instances import ASP_INSTANCES

    for (rules, expected) in ASP_INSTANCES:
        solutions = solve(rules)

        for s in solutions:
            assert s in expected