from solver.model import *


def parse(s):
    atoms = []
    no_goods = []
    satisfiable = False

    for line in s.splitlines():
        line = line.strip()
        if line.startswith("c"):
            continue

        if line.startswith("s"):
            if int(line.split(" ")[1]) == 1:
                satisfiable = True
            else:
                satisfiable = False
            continue

        if line.startswith("%") or line.startswith("0"):
            break

        if line.startswith("p"):
            parts = line.split(" ")
            num_variables = int(parts[2])

            for i in range(num_variables):
                atoms.append(Atom(i, str(i)))
        else:
            parts = list(map(int, line.split(" ")))
            assert parts[-1] == 0

            literals = []
            for id in parts[:-1]:
                index = id
                if id < 0:
                    index = -id

                index -= 1
                atom = atoms[index]

                if id < 0:
                    literals.append(T(atom))
                else:
                    literals.append(F(atom))

            no_goods.append(NoGood.of(*literals))

    return Instance(atoms, no_goods), satisfiable
