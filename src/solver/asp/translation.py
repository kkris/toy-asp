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

    instance = Instance(all_atoms, translated)

    instance.logger.debug("Translated: " + str(translated))

    return atoms, instance


def translate_rule(rule):
    no_goods = gamma(rule.body, rule.atom)

    if len(rule.head) > 0:
        no_goods.append(
            NoGood.of(T(rule.atom), F(rule.head[0].atom))
        )
    else:
        # constraint
        no_goods.append(
            NoGood.of(T(rule.atom))
        )

    return no_goods


def translate_atom_support(atoms, rules):
    no_goods = []

    for atom in atoms:
        literals = [T(atom)]
        for rule in rules:
            for head_literal in rule.head:
                if atom == head_literal.atom:
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
