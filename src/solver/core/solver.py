from solver.model import Assignment, F, NoGood
from solver.propagation.unit import propagate


def solve_dpll(instance):
    return solve(instance, backtrack_dpll)


def solve_cdnl(instance):
    return solve(instance, backtrack_cdnl)


def solve(instance, backtrack_fn):
    logger = instance.logger

    state = instance.state
    assignment = Assignment()

    propagate(instance, assignment)

    while True:
        conflict = find_conflict(instance, assignment)

        if conflict is not None:
            if state.get_current_dl() == 0:
                logger.debug("Instance not satisfiable")
                return None
            else:
                backtrack_fn(instance, assignment, conflict)
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


def find_conflict(instance, assignment):
    for no_good in instance.no_goods:
        if assignment.contains(no_good):
            return no_good

    return None


def backtrack_dpll(instance, assignment, conflict=None):
    state = instance.state

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

    instance.logger.debug("Backtrack to " + str(state.get_current_dl()))

    # propagate after guess
    propagate(instance, assignment, guess)


def backtrack_cdnl(instance, assignment, conflict):
    instance.logger.debug("Resolving conflict " + str(conflict))

    learned_no_good, k = analyse_conflict_1uip(instance, assignment, conflict)

    instance.add_no_good(learned_no_good)

    for literal in instance.state.get_literals_beyond(k):
        if literal in assignment:
            assignment.remove(literal)

    instance.state.set_decision_level(k)

    instance.logger.debug("Backtrack to " + str(instance.state.get_current_dl()))

    if k == 0:
        asserting_literal = None
    else:
        asserting_literal = instance.state.get_guess_at(k)

    instance.logger.debug("Asserting literal: " + str(asserting_literal))
    # propagate after guess
    propagate(instance, assignment, asserting_literal)


def analyse_conflict_1uip(instance, assignment, conflict):
    state = instance.state

    no_good = conflict

    max_dl = 0
    for literal in assignment:
        max_dl = max(max_dl, state.get_decision_level_for(literal))

    instance.logger.debug("max dl: " + str(max_dl))

    while contains_distinct_literals_assigned_at(no_good, state, max_dl):
        resolvent = select_resolvent(no_good, state, max_dl)

        if resolvent is None:
            raise ValueError("Should not happen")

        implicant = state.get_implicant(resolvent)

        xs = set()
        for x in implicant:
            if x != resolvent.complement():
                xs.add(x)
        for x in no_good:
            if x != resolvent:
                xs.add(x)

        no_good = NoGood.of(*xs)
        instance.logger.debug("State: " + str(no_good))

    instance.logger.debug("Learned: " + str(no_good))

    levels = sorted(set(state.get_decision_level_for(literal) for literal in no_good))
    if -1 in levels:
        levels.remove(-1)

    instance.logger.debug("Levels: " + str(levels))

    if len(levels) == 1:
        k = 0
    else:
        k = levels[-2]  # second-highest decision level

    return no_good, k


def contains_distinct_literals_assigned_at(no_good, state, dl):
    literals = list(no_good.literals)

    for l1, l2 in zip(literals, literals[1:]):
        dl1 = state.get_decision_level_for(l1)
        dl2 = state.get_decision_level_for(l2)

        if dl1 == dl2 and dl1 == dl:
            return True

    return False


def select_resolvent(no_good, state, max_dl):
    for literal in no_good:
        implicant = state.get_implicant(literal)

        if implicant is not None and state.get_decision_level_for(literal) == max_dl:
            return literal
