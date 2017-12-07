from solver.model import *
from solver.asp.solver import solve


def test_example():
    a = Atom(1, "a")
    b = Atom(2, "b")

    rules = [
        (a, [T(b)]),
        (b, [T(a)])
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
        (a, []),
        (b, []),
        (c, [T(d)])
    ]

    solutions = solve(rules)

    assert len(solutions) == 1
    assert Assignment.of(T(a), T(b), F(c), F(d)) == solutions[0]


def test_negation():
    a = Atom(1, "a")
    b = Atom(2, "b")

    rules = [
        (a, [F(b)]),
        (b, [])
    ]

    solutions = solve(rules)

    assert len(solutions) == 1
    assert Assignment.of(F(a), T(b)) == solutions[0]


def test_ewbs_1():
    man = Atom(1, "man")
    single = Atom(2, "single")
    husband = Atom(3, "husband")

    rules = [
        (man, []),
        (single, [T(man), F(husband)]),
        (husband, [T(man), F(single)])
    ]

    solutions = solve(rules)

    assert len(solutions) == 2
    assert Assignment.of(T(man), T(single), F(husband)) in solutions
    assert Assignment.of(T(man), F(single), T(husband)) in solutions


def test_killing_clause():
    p = Atom(1, "p")
    rules = [
        (p, [F(p)]),
    ]

    solutions = solve(rules)

    assert len(solutions) == 0