from enum import Enum
from collections import defaultdict

from BitVector import BitVector


class Sign(Enum):
    NEGATIVE = 0
    POSITIVE = 1


class Atom(object):

    def __init__(self, name):
        self.id = -1
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class SignedLiteral(object):

    def __init__(self, atom, sign):
        self.atom = atom
        self.sign = sign

    def index(self, num_atoms):
        return self.atom.id + (self.sign * num_atoms)

    def __str__(self):
        if self.sign == Sign.POSITIVE:
            return "T(" + str(self.atom) + ")"
        else:
            return "F(" + str(self.atom) + ")"

    def __repr__(self):
        return str(self)


class LiteralSet(object):

    def __init__(self, atoms):
        self._atom_objects = atoms

        num_atoms = len(atoms)
        self._atoms = BitVector(size=num_atoms)
        self._signs = BitVector(size=num_atoms)

    def __contains__(self, item):
        # item == index of atom
        return self._atoms[item] == 1

    def add(self, atom_index, sign):
        self._atoms[atom_index] = 1
        self._signs[atom_index] = sign

    def get_literal(self, index):
        atom = self._get_atom(index)
        sign = self._get_sign(index)

        return SignedLiteral(atom, sign)

    def __str__(self):
        return "{" + ", ".join(self._get_literals()) + "}"

    def _get_atom(self, index):
        return self._atom_objects[index]

    def _get_sign(self, index):
        value = self._signs[index]
        if value == 0:
            return Sign.NEGATIVE
        else:
            return Sign.POSITIVE

    def _get_literals(self):
        literals = []
        for atom_index in self._atoms:
            literals.append(self.get_literal(atom_index))

        return literals


class NoGood(LiteralSet):

    def __init__(self, atoms, id):
        super().__init__(atoms)

        self.id = id

    def add(self, atom_index, sign):
        raise ValueError("NoGood is immutable")

    def __eq__(self, other):
        return self.id == other.id


class Watch(object):

    def __init__(self, a, b):
        self.literals = set
        self.no_good = no_good
        self.first = first
        self.second = second


class Watcher(object):

    def __init__(self, atoms, no_goods):
        self.num_atoms = len(atoms)

        self.watches_by_nogood = [None for _ in no_goods]
        self.no_goods_by_literal = [[] for _ in range(2 * len(atoms))]

        for no_good in no_goods:
            literals = no_good._get_literals()
            first = literals[0]
            if len(literals) >= 2:
                second = literals[1]
            else:
                second = None

            watch = Watch(no_good, first, second)
            self._add_watch(no_good, watch)

    def _add_watch(self, no_good, watch):
        self.watches_by_nogood[no_good.id] = watch
        self.no_goods_by_literal[watch.first.index(self.num_atoms)].append(no_good)

        if watch.second is not None:
            self.no_goods_by_literal[watch.second.index(self.num_atoms)].append(no_good)

    def remove_watch(self, literal, no_good):
        self.no_goods_by_literal[literal.index(self.num_atoms)].remove(no_good)

        watch = self.watches_by_nogood[no_good]


    def update_watch(self, literals, no_good):
        # remove old watches
        for watch in self.get_watches(no_good):
            self.no_goods_by_literal[watch.first.index(self.num_atoms)].remove(no_good)
            if watch.second is not None:
                self.no_goods_by_literal[watch.second.index(self.num_atoms)].remove(no_good)

        watch = self.watches_by_nogood
        self._add_watch(no_good, watch)

    def lookup(self, literal):
        return self.no_goods_by_literal[literal.index(self.num_atoms)]

    def get_watches(self, no_good):
        return self.watches_by_nogood[no_good.id]


class Instance(object):

    def __init__(self, atoms, no_goods):
        self.atoms = atoms
        self.no_goods = no_goods

        for index, atom in enumerate(self.atoms):
            atom.id = index

        for index, no_good in enumerate(no_goods):
            no_good.id = index

        self.watcher = Watcher(atoms, no_goods)

    def add_no_good(self, no_good):
        raise NotImplementedError("TODO")

