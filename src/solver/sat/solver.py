from solver.model import Assignment, T, F, NoGood
from solver.propagation.unit import propagate


def solve_dpll(instance, all_solutions=False):
    solutions = solve(instance, backtrack_dpll, all_solutions)

    if all_solutions:
        for solution in solutions:
            yield solution
    else:
        yield next(solutions)


def solve_cdnl(instance):
    solutions = solve(instance, backtrack_cdnl, all_solutions=False)

    yield next(solutions)


def solve(instance, backtrack_fn, all_solutions=False):
    logger = instance.logger

    state = instance.state
    assignment = Assignment()

    propagate(instance, assignment)

    while True:
        conflict = find_conflict(instance, assignment)

        if conflict is not None:
            logger.info("Conflict: " + str(conflict))

            if state.get_current_dl() == 0:
                logger.info("Conflict at dl 0. Exiting.")
                return
            else:
                logger.debug("Backtracking..")
                backtrack_fn(instance, assignment, conflict)
                continue

        if assignment.size() == instance.size():
            logger.info("Found satisfying assignment: " + str(assignment))

            if all_solutions:
                copy = Assignment.of(*assignment.literals)

                yield copy

                if state.get_current_dl() == 0:
                    # no backtracking possible anymore: found all solutions
                    return

                # backtrack to highest level with an alternative decision not tried yet
                backtrack_dpll(instance, assignment)
            else:
                yield assignment
                return
        else:
            # guess
            atom = select_unassigned_atom(instance, assignment)
            guess = F(atom)

            state.increase_dl()
            state.set_implicant(guess, None)
            state.add_guess(guess, state.get_current_dl())
            state.set_decision_level_for(guess, state.get_current_dl())

            assignment.add(guess)

            logger.info("Guess " + str(guess) + "@" + str(state.get_current_dl()))

            # propagate after guess
            propagate(instance, assignment, guess)


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

    for literal in state.get_assigned_literals_beyond(k):
        if literal in assignment:
            assignment.remove(literal)

    guess = state.get_guess_at(k + 1)
    state.decrease_dl()

    complement = guess.complement()
    assignment.add(complement)

    state.set_implicant(complement, None)
    state.set_decision_level_for(complement, k)

    instance.logger.debug("Backtrack to " + str(state.get_current_dl()))

    propagate(instance, assignment, complement)


def backtrack_cdnl(instance, assignment, conflict):
    state = instance.state

    instance.logger.debug("Resolving conflict " + str(conflict))

    learned_no_good, asserting_literal, k = analyse_conflict_1uip(instance, assignment, conflict)

    instance.logger.info("Learned no-good: " + str(learned_no_good) + " (" + str(asserting_literal) + " is asserting)")
    instance.logger.info("Backtrack to " + str(k))

    # back-jump to second-highest decision level
    for literal in state.get_assigned_literals_beyond(k):
        if literal in assignment:
            assignment.remove(literal)

    state.set_decision_level(k)
    is_duplicate = instance.add_no_good(learned_no_good, assignment)

    if is_duplicate:
        instance.logger.debug("Learned already known no-good")

    # learned no-good is unit
    complement = asserting_literal.complement()
    assignment.add(complement)

    state.set_decision_level_for(complement, state.get_current_dl())
    state.set_implicant(complement, learned_no_good)

    # propagate after force by learned clause
    propagate(instance, assignment, complement)


def analyse_conflict_1uip(instance, assignment, conflict):
    state = instance.state

    no_good = conflict

    max_dl = 0
    for literal in assignment:
        max_dl = max(max_dl, state.get_decision_level_for(literal))

    while contains_distinct_literals_assigned_at(no_good, state, max_dl):
        resolvent = select_resolvent(no_good, state, max_dl)
        implicant = state.get_implicant(resolvent)

        literals = set()
        for literal in implicant:
            if literal != resolvent.complement():
                literals.add(literal)
        for literal in no_good:
            if literal != resolvent:
                literals.add(literal)

        no_good = NoGood.of(*literals)

    levels = sorted(set(state.get_decision_level_for(literal) for literal in no_good))
    if -1 in levels:
        levels.remove(-1)

    if len(levels) == 1:
        k = 0
    else:
        k = levels[-2]  # second-highest decision level

    highest_dl = levels[-1]

    asserting_literal = None
    for literal in state.get_literals_assigned_at(highest_dl):
        if literal in no_good:
            asserting_literal = literal
            break

    return no_good, asserting_literal, k


def contains_distinct_literals_assigned_at(no_good, state, dl):
    literals = list(no_good.literals)

    for i, l1 in enumerate(literals[:-1]):
        for l2 in literals[i+1:]:
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
