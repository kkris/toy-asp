from solver.model import *
from solver.propagation.unit import propagate

a = Atom(1, "a")
b = Atom(2, "b")
c = Atom(3, "c")
d = Atom(4, "d")

N1 = NoGood.of(F(b), T(c), T(d))
N2 = NoGood.of(T(a), T(b))
N3 = NoGood.of(T(b))

ATOMS = [a, b, c, d]


def test_basic_1():
    instance = Instance(ATOMS, [N1, N2])
    assignment = Assignment.of(T(a))
    changed = T(a)

    propagate(instance, assignment, changed)

    assert T(a) in assignment
    assert F(b) in assignment
    assert len(assignment.literals) == 2


def test_basic_2():
    instance = Instance(ATOMS, [N1, N2, N3])
    assignment = Assignment.of(T(a))
    changed = T(a)

    propagate(instance, assignment, changed)

    assert T(a) in assignment
    assert F(b) in assignment


def test_basic_3():
    instance = Instance(ATOMS, [N3])
    assignment = Assignment.of(T(d))
    changed = T(d)

    propagate(instance, assignment, changed)

    assert T(d) in assignment
    assert F(b) in assignment


def test_chain():
    atoms = [
        Atom(1, "a"),
        Atom(2, "b"),
        Atom(3, "c"),
        Atom(4, "d"),
        Atom(5, "e")
    ]

    no_goods = []
    for (antecedent, implicant) in zip(atoms, atoms[1:]):
        no_goods.append(NoGood.of(T(antecedent), F(implicant)))

    instance = Instance(atoms, no_goods)
    assignment = Assignment.of(T(atoms[0]))
    changed = T(atoms[0])

    propagate(instance, assignment, changed)

    for atom in atoms:
        assert T(atom) in assignment


def test_update_watch():
    a = Atom(1, "a")
    x = Atom(4, "x")
    y = Atom(5, "y")

    atoms = [a, b, c, x, y]

    no_goods = [
        NoGood.of(F(a), F(x), F(y))
    ]

    instance = Instance(atoms, no_goods)

    watches = instance.watcher.get_watches(no_goods[0])

    assert F(a) in watches
    assert F(x) in watches

    assignment = Assignment.of(F(a))
    propagate(instance, assignment, F(a))

    watches = instance.watcher.get_watches(no_goods[0])

    assert F(a) not in watches
    assert F(x) in watches
    assert F(y) in watches


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

    assignment = Assignment.of(F(a))
    propagate(instance, assignment, F(a))

    assignment.add(F(b))
    propagate(instance, assignment, F(b))

    assignment.add(F(c))
    propagate(instance, assignment, F(c))

    assignment.add(F(x))
    propagate(instance, assignment, F(x))

    assert F(y) in assignment
    assert F(y) in assignment


def test_example_redux():
    a = Atom(1, "a")
    b = Atom(2, "b")
    c = Atom(3, "c")
    x = Atom(4, "x")
    y = Atom(5, "y")

    atoms = [a, b, c, x, y]

    no_goods = [
        NoGood.of(F(a), F(x), F(y))
    ]

    instance = Instance(atoms, no_goods)

    assignment = Assignment.of(F(a))
    propagate(instance, assignment, F(a))

    assignment.add(F(x))
    propagate(instance, assignment, F(x))

    assert T(y) in assignment
