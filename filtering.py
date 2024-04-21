import numpy as np

from models.operator import Operator


def calculate_filter_matrix(activities, eva_times):
    p = np.zeros((len(activities), len(eva_times)), dtype=int)

    for i, activity in enumerate(activities):
        for j, eva in enumerate(eva_times):
            p[i, j] = is_possible(activity.get_constraints(),
                                  eva.get_factor_values()) if activity.duration < eva.duration * (
                        1 - eva.reserve) else 0

    return p


def is_possible(constraints, factor_values):
    result = 1
    for factor_value in factor_values:
        factored_constraints = filter(lambda c: c.factor.id == factor_value.factor.id, constraints)
        intermediate = check_constraint_by_factor_value(factor_value, factored_constraints)

        if intermediate == 0:
            return 0
        else:
            result = result * intermediate

    return result


def check_constraint_by_factor_value(factor_value, constraints):
    smaller_constraints = filter(lambda c: c.operator == Operator.SMALLER, constraints)
    greater_constraints = filter(lambda c: c.operator == Operator.GREATER, constraints)
    equal_constraints = filter(lambda c: c.operator == Operator.EQUAL, constraints)
    not_equal_constraints = filter(lambda c: c.operator == Operator.NOT_EQUAL, constraints)

    smaller_value = check_constraints(factor_value, smaller_constraints)
    greater_value = check_constraints(factor_value, greater_constraints)
    equal_value = check_constraints(factor_value, equal_constraints)
    not_equal_value = check_constraints(factor_value, not_equal_constraints)

    smaller_greater_value = min([smaller_value, greater_value])

    return max([smaller_greater_value, equal_value, not_equal_value])


def check_constraints(factor_value, constraints):
    results = []
    for constraint in constraints:
        results.append(constraint.check(factor_value))

    if len(results) == 0:
        return 1

    return max(results)
