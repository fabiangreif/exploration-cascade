class EVA:
    def __init__(self, id, datetime, duration, reserve, factor_values):
        self.id = id
        self.datetime = datetime
        self.duration = duration
        self.reserve = reserve
        self.factor_values = factor_values
        self.activities = []

    def get_factor_values(self):
        return self.factor_values

    def add_activity(self, a):
        self.activities.append(a)

    def get_duration(self):
        time = self.duration * (1 - self.reserve)
        time_activities = sum(list(map(lambda a: a.duration, self.activities))) if len(self.activities) > 0 else 0
        return time - time_activities
