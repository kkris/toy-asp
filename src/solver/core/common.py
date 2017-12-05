class State(object):

    def __init__(self):
        self.current_dl = 0
        self.implicants = {}

        self.guesses = {}
        self.decision_levels_for_atoms = {}

    def get_current_dl(self):
        return self.current_dl

    def increase_dl(self):
        self.current_dl += 1

    def decrease_dl(self):
        self.current_dl -= 1

    def set_decision_level(self, level):
        self.current_dl = level

    def get_implicant(self, literal):
        if literal in self.implicants:
            return self.implicants[literal]
        return None

    def set_implicant(self, literal, implicant):
        self.implicants[literal] = implicant

    def add_guess(self, literal, dl):
        self.guesses[dl] = literal

    def get_guess_at(self, dl):
        return self.guesses[dl]

    def get_decision_level_for(self, literal):
        if literal.atom not in self.decision_levels_for_atoms:
            return -1

        return self.decision_levels_for_atoms[literal.atom]

    def set_decision_level_for(self, literal, dl):
        self.decision_levels_for_atoms[literal.atom] = dl

    def compute_greatest_level_with_alternative(self, assignment):
        # compute k
        j = 1
        for i in range(1, self.get_current_dl() + 1):
            if self.get_guess_at(i) in assignment:
                j = max(j, i)

        return j - 1

    def get_assigned_atoms_beyond(self, k):
        for literal, dl in self.decision_levels_for_atoms.items():
            if dl > k:
                yield literal
