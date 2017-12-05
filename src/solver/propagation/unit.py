def propagate(instance, assignment, changed_literal=None):
    changed = set()

    for propagated in propagate_singletons(instance, assignment):
        changed.add(propagated)

    if changed_literal is not None:
        changed.add(changed_literal)

    while changed:
        literal = changed.pop()
        propagated = propagate_step(instance, assignment, literal)
        for l in propagated:
            changed.add(l)


def propagate_singletons(instance, assignment):
    propagated_literals = set()

    for no_good in instance.no_goods:
        if len(no_good.literals) == 1:
            for literal in no_good:
                complement = literal.complement()

                if complement not in assignment:
                    assignment.add(complement)
                    propagated_literals.add(complement)
                    # instance.logger.debug("Propagate [SNGT] " + str(complement))
                    print("Propagate [SNGT] " + str(complement))

    return propagated_literals


def propagate_step(instance, assignment, assigned_literal):
    propagated_literals = set()

    for no_good in instance.watcher.lookup(assigned_literal)[:]:
        if assignment.contains(no_good):
            # no good already falsified
            continue
        if assignment.contains_complement(no_good):
            # already satisfied
            continue

        watched_literals = instance.watcher.get_watches(no_good)

        if len(watched_literals) == 1:
            # only one unassigned literal
            # this happens only for learned clauses after backtracking
            complement = propagate_unit(instance, assignment, no_good, watched_literals[0])
            propagated_literals.add(complement)
            continue

        if assigned_literal == watched_literals[0]:
            other = watched_literals[1]
        else:
            other = watched_literals[0]

        # find unassigned atom
        unassigned = None
        for literal in no_good:
            if literal == other:
                continue

            if not assignment.assigns_atom(literal.atom):
                # found unassigned atom
                unassigned = literal
                break

        if unassigned is not None:
            if unassigned == assigned_literal:
                a = 1
            else:
                instance.watcher.update_watch(assigned_literal, unassigned, no_good)
        else:
            # propagate unit
            complement = propagate_unit(instance, assignment, no_good, other)
            propagated_literals.add(complement)

    return propagated_literals


def propagate_unit(instance, assignment, no_good, literal):
    complement = literal.complement()
    assignment.add(complement)

    dl = max(instance.state.get_decision_level_for(l) for l in no_good if l != literal)

    instance.state.set_implicant(complement, no_good)
    instance.state.set_decision_level_for(complement, dl)

    # instance.logger.debug("Propagate [UNIT] " + str(complement))
    print("Propagate [UNIT] " + str(complement))

    return complement
