from models.operator import Operator


class Constraint:
    def __init__(self, operator, factor, value, output):
        self.operator = operator
        self.factor = factor
        self.value = value
        self.output = output

    def check(self, factor_value):
        if factor_value.factor.id != self.factor.id:
            return 0

        if self.operator == Operator.EQUAL:
            return self.output if self.value == factor_value.value else 0

        elif self.operator == Operator.NOT_EQUAL:
            return self.output if self.value != factor_value.value else 0

        elif self.operator == Operator.GREATER:
            return self.output if self.value < factor_value.value else 0

        elif self.operator == Operator.SMALLER:
            return self.output if self.value > factor_value.value else 0

        else:
            return 0
