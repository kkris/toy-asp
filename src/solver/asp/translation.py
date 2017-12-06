from solver.model import *


def literal_to_compact_string(literal):
    if literal.is_positive():
        return literal.atom.repr
    else:
        return "-" + literal.atom.repr


class Rule(object):

    def __init__(self, head, body, atom_factory):
        self.head = head
        self.body = body

        name = "β_{" + ", ".join(map(literal_to_compact_string, body)) + "}"
        self.atom = atom_factory.create_atom(name)


class AtomFactory(object):

    def __init__(self, sequence_start):
        self.current_id = sequence_start

    def create_atom(self, name="new"):
        atom = Atom(self.current_id, name)
        self.current_id += 1

        return atom


def compute_clarks_completion(atoms, raw_rules):
    atom_factory = AtomFactory(len(atoms) + 1)

    rules = []
    for (head, body) in raw_rules:
        rules.append(Rule(head, body, atom_factory))

    translated = []

    for rule in rules:
        no_goods = translate_rule(rule)

        translated.extend(no_goods)

    translated.extend(translate_atom_support(atoms, rules))

    all_atoms = atoms[:]
    for rule in rules:
        all_atoms.append(rule.atom)

    return atoms, Instance(all_atoms, translated)


def translate_rule(rule):
    no_goods = gamma(rule.body, rule.atom)

    no_goods.append(
        NoGood.of(T(rule.atom), F(rule.head))
    )

    return no_goods


def translate_atom_support(atoms, rules):
    no_goods = []

    for atom in atoms:
        literals = [T(atom)]
        for rule in rules:
            if atom == rule.head:
                literals.append(F(rule.atom))

        no_goods.append(NoGood.of(*literals))

    return no_goods


def gamma(literals, beta):
    no_goods = [
        NoGood.of(*([F(beta)] + literals))
    ]

    for literal in literals:
        no_goods.append(
            NoGood.of(T(beta), literal.complement())
        )

    return no_goods


def project(assignment, atoms):
    projected = Assignment()

    atoms = set(atoms)
    for literal in assignment:
        if literal.atom in atoms:
            projected.add(literal)

    return projected
