from solver.model import Assignment, F, T
from solver.propagation.unit import propagate
from solver.core.common import State


def solve(instance):
    logger = instance.logger

    state = instance.state
    assignment = Assignment()

    propagate(instance, assignment)

    while True:
        backtracked = False

        for no_good in instance.no_goods:
            if assignment.contains(no_good):
                if state.get_current_dl() == 0:
                    logger.debug("Instance not satisfiable")
                    return None
                else:
                    k = state.compute_greatest_level_with_alternative(assignment)

                    for literal in state.get_literals_beyond(k):
                        if literal in assignment:
                            assignment.remove(literal)

                    guess = state.get_guess_at(k + 1)
                    state.decrease_dl()

                    complement = guess.complement()
                    assignment.add(complement)

                    state.set_implicant(complement, None)
                    state.set_decision_level_for(complement, k)

                    logger.debug("Backtrack to " + str(state.get_current_dl()))

                    # propagate after guess
                    propagate(instance, assignment, guess)

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

            state.increase_dl()
            state.set_implicant(guess, None)
            state.add_guess(guess, state.get_current_dl())
            state.set_decision_level_for(guess, state.get_current_dl())

            assignment.add(guess)

            logger.debug("Guess " + str(guess) + "@" + str(state.get_current_dl()))
            logger.debug("Assignment: " + str(assignment))

            # propagate after guess
            propagate(instance, assignment, guess)
            logger.debug("Assignment: " + str(assignment))


def select_unassigned_atom(instance, assignment):
    for atom in instance.atoms:
        if not assignment.assigns_atom(atom):
            return atom

    raise ValueError("unreachable")

