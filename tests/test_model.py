from solver.model import *

atoms = [Atom(1, "p(a)"), Atom(2, "p(b)"), Atom(3, "q(a)")]


def test_atoms():
    assert atoms[0] == atoms[0]
    assert hash(atoms[0]) == 1


def test_literals():
    t1 = T(atoms[0])
    f1 = F(atoms[1])

    assert t1.sign == Sign.POSITIVE
    assert f1.sign == Sign.NEGATIVE


def test_complement():
    t1 = T(atoms[0])
    f1 = F(atoms[1])

    assert t1.sign.complement() == Sign.NEGATIVE
    assert f1.sign.complement() == Sign.POSITIVE

    assert t1.complement().atom == t1.atom
    assert f1.complement().atom == f1.atom

    assert t1.complement().sign == Sign.NEGATIVE
    assert f1.complement().sign == Sign.POSITIVE


def test_nogoods():
    t1 = T(atoms[0])
    t2 = T(atoms[2])
    f1 = F(atoms[1])

    n1 = NoGood.of(t1, f1)
    n2 = NoGood.of(t2)

    assert t1 in n1
    assert f1 in n1
    assert t2 not in n1
    assert t2 in n2
