from solver.model import *


def parse_head(head, atoms, atom_factory):
    head = head.strip()
    if not head:
        return [] # constraint

    if head not in atoms:
        atom = atom_factory.create_atom(head)
        atoms[head] = atom

    return [T(atoms[head])]


def parse_body(body, atoms, atom_factory):
    body = body.split(",")
    literals = []

    for literal in body:
        sign = T
        if "not" in literal:
            literal = literal.replace("not", "")
            sign = F

        literal = literal.strip()

        if literal not in atoms:
            atom = atom_factory.create_atom(literal)
            atoms[literal] = atom

        literals.append(sign(atoms[literal]))

    return literals


def parse_rule(r, atoms, atom_factory):
    if ":-" in r:
        parts = r.split(":-")
        head = parse_head(parts[0], atoms, atom_factory)
        body = parse_body(parts[1], atoms, atom_factory)

        return head, body
    else:
        # fact
        return parse_head(r, atoms, atom_factory), []


def parse(s):
    atoms = {}
    atom_factory = AtomFactory(1)

    rules = []
    solutions = []

    for line in s.splitlines():
        line = line.replace(".", "").strip()
        if not line:
            continue

        if line.startswith("#"):
            continue

        if line.startswith("S"):
            line = line.replace("S", "").replace("=", "").replace("{", "").replace("}", "").replace(" ", "").strip()

            answer_set = line.split(",")
            assignment = Assignment()
            for atom in atoms.values():
                if atom.repr in answer_set:
                    assignment.add(T(atom))
                else:
                    assignment.add(F(atom))

            solutions.append(assignment)
        else:
            rules.append(parse_rule(line, atoms, atom_factory))

    return rules, solutions
