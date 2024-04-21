class Activity:
    def __init__(self, id, duration, constraints):
        self.id = id
        self.duration = duration
        self.constraints = constraints
        self.eva = None

    def get_constraints(self):
        return self.constraints

    def set_eva(self, eva):
        self.eva = eva

    def get_eva(self):
        return self.eva
