from solver.model import Assignment, F, T
from solver.propagation.unit import propagate


def solve(instance):
    logger = instance.logger

    assignment = Assignment()
    current_dl = 0

    guesses = {}
    dl = {}
    implicants = {}

    updated = propagate(instance, assignment)
    for literal in updated:
        dl[literal] = current_dl

    while True:
        backtracked = False

        for no_good in instance.no_goods:
            if assignment.contains(no_good):
                if current_dl == 0:
                    logger.debug("Instance not satisfiable")
                    return None
                else:
                    k = max((i if guesses[i] in assignment else 1) for i in range(1, current_dl + 1)) - 1

                    for literal in list(dl.keys()):
                        level = dl[literal]
                        if level > k:
                            assignment.remove(literal) # remove only positive?
                            del dl[literal]

                    guess = guesses[k + 1]
                    current_dl -= 1

                    complement = guess.complement()
                    assignment.add(complement)

                    dl[complement] = k
                    implicants[complement] = None

                    logger.debug("Backtrack to " + str(current_dl))

                    # propagate after guess
                    updated = propagate(instance, assignment, guess)
                    for literal in updated:
                        dl[literal] = current_dl

                    backtracked = True
                    break

        if backtracked:
            continue

        if assignment.size() == instance.size():
            logger.debug("Found satisfying assignment: " + str(assignment))
            return assignment
        else:
            # guess
            atom = select_unassigned_atom(instance, assignment)
            guess = F(atom)

            current_dl += 1
            guesses[current_dl] = guess
            dl[guess] = current_dl
            implicants[guess] = None

            assignment.add(guess)

            logger.debug("Guess " + str(guess) + "@" + str(current_dl))
            logger.debug("Assignment: " + str(assignment))

            # propagate after guess
            updated = propagate(instance, assignment, guess)
            for literal in updated:
                dl[literal] = current_dl
            logger.debug("Assignment: " + str(assignment))


def select_unassigned_atom(instance, assignment):
    for atom in instance.atoms:
        if not assignment.assigns_atom(atom):
            return atom

    raise ValueError("unreachable")

