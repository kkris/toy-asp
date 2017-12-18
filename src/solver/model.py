from enum import Enum
from collections import defaultdict

from solver.logger import Level, Logger
from solver.sat.common import State


class Sign(Enum):
    NEGATIVE = 0
    POSITIVE = 1

    def complement(self):
        return Sign.NEGATIVE if self == Sign.POSITIVE else Sign.POSITIVE


class Atom(object):

    def __init__(self, identifier, repr):
        self.identifier = identifier
        self.repr = repr

    def __str__(self):
        return self.repr

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.identifier

    def __eq__(self, other):
        return self.identifier == other.identifier


class SignedLiteral(object):

    def __init__(self, atom, sign):
        self.atom = atom
        self.sign = sign

    def complement(self):
        return SignedLiteral(self.atom, self.sign.complement())

    def is_positive(self):
        return self.sign == Sign.POSITIVE

    def is_negative(self):
        return self.sign == Sign.NEGATIVE

    def __eq__(self, other):
        return self.sign == other.sign and self.atom == other.atom

    def __hash__(self):
        sign = 17 if self.sign == Sign.NEGATIVE else 1
        return sign * self.atom.identifier

    def __str__(self):
        if self.sign == Sign.POSITIVE:
            return "T(" + str(self.atom) + ")"
        else:
            return "F(" + str(self.atom) + ")"

    def __repr__(self):
        return str(self)


class T(SignedLiteral):

    def __init__(self, atom):
        super().__init__(atom, Sign.POSITIVE)


class F(SignedLiteral):

    def __init__(self, atom):
        super().__init__(atom, Sign.NEGATIVE)


class LiteralSet(object):
    def __init__(self):
        self.literals = set()

    def __contains__(self, item):
        assert isinstance(item, SignedLiteral)

        return item in self.literals

    def add(self, literal):
        self.literals.add(literal)

    def size(self):
        return len(self.literals)

    def __iter__(self):
        return iter(self.literals)

    def __str__(self):
        return "{" + ", ".join(map(str, sorted(self.literals, key=lambda l: l.atom.identifier))) + "}"

    def __repr__(self):
        return str(self)

    @staticmethod
    def of(*items):
        literal_set = LiteralSet()
        for item in items:
            literal_set.add(item)

        return literal_set

    def __eq__(self, other):
        return self.literals == other.literals


class Assignment(LiteralSet):

    def contains(self, no_good):
        # is subset
        for literal in no_good:
            if literal not in self.literals:
                return False

        return True

    def remove(self, literal):
        self.literals.remove(literal)

    def contains_complement(self, no_good):
        # contains any of the literals in complementary form
        for literal in no_good:
            if literal.complement() in self.literals:
                return True

        return False

    def assigns_atom(self, atom):
        for literal in self:
            if literal.atom == atom:
                return True

        return False

    @staticmethod
    def of(*items):
        assignment = Assignment()
        for item in items:
            assignment.add(item)

        return assignment


class NoGood(LiteralSet):

    def copy(self):
        raise ValueError("NoGood is immutable")

    def add(self, literal):
        raise ValueError("NoGood is immutable")

    @staticmethod
    def of(*items):
        no_good = NoGood()
        for item in items:
            no_good.literals.add(item)

        return no_good

    def __hash__(self):
        p = 1
        for literal in self.literals:
            p *= hash(literal)

        return p


class Watcher(object):

    def __init__(self, no_goods):
        self.watches = defaultdict(list)
        self.no_goods = defaultdict(list)

        for no_good in no_goods:
            self.initialize_watches(no_good, Assignment())

    def add_watch(self, literal, no_good):
        self.watches[no_good].append(literal)
        self.no_goods[literal].append(no_good)

    def update_watch(self, old_literal, new_literal, no_good):
        self.no_goods[old_literal].remove(no_good)
        self.watches[no_good].remove(old_literal)

        self.add_watch(new_literal, no_good)

    def initialize_watches(self, no_good, assignment):
        if len(no_good.literals) <= 1:
            # don't watch singleton no-goods
            # they are unit by default or already satisfied/conflicting
            return

        # try to find two unassigned literals to watch
        watches = []
        for literal in no_good:
            if literal not in assignment:
                watches.append(literal)

            if len(watches) == 2:
                break

        if len(watches) == 1:
            # in the case of a learned no-good, there is only one unassigned atom
            # just add the next literal not already selected as a second watch
            for literal in no_good:
                if literal != watches[0]:
                    watches.append(literal)
                    break

        for watch in watches:
            self.add_watch(watch, no_good)

        return

    def lookup(self, literal):
        return self.no_goods[literal]

    def get_watches(self, no_good):
        return self.watches[no_good]


class Instance(object):

    def __init__(self, atoms, no_goods):
        self.atoms = atoms
        self.no_goods = no_goods
        self.watcher = Watcher(no_goods)
        self.state = State()

        self.logger = Logger()

    def size(self):
        return len(self.atoms)

    def add_no_good(self, no_good, assignment):
        if no_good in self.no_goods:
            return True

        self.no_goods.append(no_good)
        self.watcher.initialize_watches(no_good, assignment)

        return False


class AtomFactory(object):

    def __init__(self, sequence_start):
        self.current_id = sequence_start

    def create_atom(self, name="new"):
        atom = Atom(self.current_id, name)
        self.current_id += 1

        return atom