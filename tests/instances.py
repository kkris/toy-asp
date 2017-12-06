import os

from solver.model import *
from solver.parser.dimacs import parse


class CheckSat(object):

    def __eq__(self, other):
        assert other is not None
        assert isinstance(other, Assignment)


def _create_vote_instance():
    a = Atom(1, "a")
    b = Atom(2, "b")
    c = Atom(3, "c")

    atoms = [a, b, c]
    no_goods = [
        NoGood.of(F(a), F(b), T(c)),
        NoGood.of(F(b), F(c)),
        NoGood.of(T(b)),
        NoGood.of(T(a), F(c))
    ]

    instance = Instance(atoms, no_goods)
    solution = Assignment.of(T(a), F(b), T(c))

    return instance, solution


def _create_unsat():
    a = Atom(1, "a")

    instance = Instance([a], [NoGood.of(T(a)), NoGood.of(F(a))])

    return instance, None


def _create_trivial_sat():
    a = Atom(1, "a")

    instance = Instance([a], [NoGood.of(T(a), F(a))])  # a v -a
    solution = Assignment.of(F(a))

    return instance, solution


def _create_example_2():
    # N 1 : {Fa, Tb}, N 2 : {Fa, Tc}, N 3 : {Fb, Fc, Td}, N 4 : {Fd, Te}, N 5 : {Fd, Tf }, N 6 : {Fe, Ff }

    a = Atom(1, "a")
    b = Atom(2, "b")
    c = Atom(3, "c")
    d = Atom(4, "d")
    e = Atom(5, "e")
    f = Atom(6, "f")

    no_goods = [
        NoGood.of(F(a), T(b)),
        NoGood.of(F(a), T(c)),
        NoGood.of(F(b), F(c), T(d)),
        NoGood.of(F(d), T(e)),
        NoGood.of(F(d), T(f)),
        NoGood.of(F(e), F(f))
    ]

    solution = Assignment.of(T(d), T(a), F(b), T(c), F(e), T(f))

    return Instance([a, b, c, d, e, f], no_goods), solution


def _load_instances():
    instances = []
    for file in os.listdir("resources"):
        if "large" in file:
            continue

        with open(os.path.join("resources", file)) as fh:
            contents = fh.read()
            instances.append(parse(contents))

    return instances


def _load_huge_instances():
    instances = []
    for file in os.listdir("resources"):
        if "large" not in file:
            continue

        with open(os.path.join("resources", file)) as fh:
            contents = fh.read()
            instances.append(parse(contents))

    return instances


INSTANCES = [
    _create_unsat(),
    _create_trivial_sat(),
    _create_vote_instance(),
    _create_example_2()
]

LARGE_INSTANCES = _load_instances()

REALLY_LARGE_INSTANCES = _load_huge_instances()
