import numpy as np

from models.edge import Edge
from models.graph import Graph
from models.node import Node


def traverse_dependency_graph(all_activities, all_evas, dependency_graph, p, d):
    c = np.zeros((len(all_evas), len(all_activities)), dtype=int)

    level_dictionary = dependency_graph.get_node_dictionary(-1)
    depth_first_search(dependency_graph, level_dictionary, 0, dependency_graph.get_start_node())
    level_graph = create_level_graph(level_dictionary, dependency_graph)

    sorted_nodes = sorted(level_graph.nodes, key=lambda n: n.id)

    for node in sorted_nodes[1:-1]:
        node_activities = node.value
        assign(c, node_activities, p, all_evas, d, all_activities, dependency_graph)

    return c


def depth_first_search(graph, level_dictionary, depth, node):
    level_dictionary[node.id] = depth if level_dictionary[node.id] < depth else level_dictionary[
        node.id]

    if node.id != 'end':
        children = list(graph.get_children(node))
        for child in children:
            depth_first_search(graph, level_dictionary, depth + 1, child)


def create_level_graph(level_dictionary, dependency_graph):
    levels = []
    values = dict(level_dictionary).values()
    for value in values:
        levels.append(value)

    nodes = []
    for level in set(levels):
        nodes.append(Node([], level))

    for key, value in dict(level_dictionary).items():
        activity = next(node.value for node in dependency_graph.nodes if node.id == key)
        node = next(node for node in nodes if node.id == value)
        node.value = node.value + [activity]

    sorted_nodes = sorted(nodes, key=lambda node: node.id)
    edges = []
    pre_node = None
    for node in sorted_nodes:
        if pre_node is not None:
            edges.append(Edge(pre_node, node))
        pre_node = node

    return Graph(nodes, edges)


def assign(c, activities, p, all_evas, d, all_activities, graph):
    possible_evas = calculate_possible_evas(activities, all_evas, d, all_activities, p)
    eva_with_activities = calculate_eva_with_activities(possible_evas)

    for eva, possible_activities in eva_with_activities.items():

        activities_with_weight = calculate_activities_with_weight(possible_activities, all_activities, graph,
                                                                  possible_evas)

        items = []
        for activity_id, weight in activities_with_weight.items():
            items.append((str(activity_id), int(weight), all_activities[activity_id].duration))

        capacity = int(all_evas[eva].get_duration())

        max_value, selected_items = knapsack_01(items, capacity)

        for item in selected_items:
            activity = all_activities[int(item[0])]
            activity.set_eva(all_evas[eva])

            all_evas[eva].add_activity(activity)

            c[eva, int(item[0])] = p[int(item[0]), eva]


def calculate_possible_evas(activities, evas, d, all_activities, p):
    possible_evas = {}
    for activity in activities:
        dates = []
        for i, a in enumerate(d[activity.id]):
            if a > 0:
                eva = all_activities[i].eva
                if eva is not None:
                    dates.append(eva.datetime)

        dates_empty = len(dates) == 0

        possible_evas[activity.id] = []
        for index, eva in enumerate(evas):
            if p[activity.id, index] > 0:
                if dates_empty:
                    possible_evas[activity.id] = possible_evas[activity.id] + [eva.id]
                else:
                    if eva.datetime > max(dates):
                        possible_evas[activity.id] = possible_evas[activity.id] + [eva.id]

    return possible_evas


def calculate_eva_with_activities(possible_evas):
    all_possible_evas = []
    for values in possible_evas.values():
        all_possible_evas = all_possible_evas + values

    eva_with_activities = {}
    for eva in set(all_possible_evas):
        eva_with_activities[eva] = []

        for key, value in possible_evas.items():
            if eva in value:
                eva_with_activities[eva] = eva_with_activities[eva] + [key]

    return eva_with_activities


def calculate_activities_with_weight(possible_activities, all_activities, graph, possible_evas):
    activities_with_weight = {}
    for possible_activity in possible_activities:
        if all_activities[possible_activity].eva is None:
            activities_with_weight[possible_activity] = calculate_weight1(possible_activity, possible_evas)

    successors = []
    durations = []

    for possible_activity in activities_with_weight.keys():
        count_successor = depth_first_search_successors(graph, graph.get_node_by_id(possible_activity))
        count_duration = depth_first_search_duration(graph, graph.get_node_by_id(possible_activity))

        successors.append((possible_activity, count_successor))
        durations.append((possible_activity, count_duration))

    alpha = beta = 0.5
    count_activities = len(activities_with_weight.keys())

    sorted_successors = sorted(successors, key=lambda x: x[1])
    sorted_durations = sorted(durations, key=lambda x: x[1])

    for index, item in enumerate(sorted_successors):
        key = item[0]
        w2 = ((index + 1) / count_activities) * 100 * alpha
        activities_with_weight[key] = activities_with_weight[key] + w2

    for index, item in enumerate(sorted_durations):
        key = item[0]
        w3 = ((index + 1) / count_activities) * 100 * beta
        activities_with_weight[key] = activities_with_weight[key] + w3

    return activities_with_weight


def knapsack_01(items, capacity):
    n = len(items)
    # Create a table to store the maximum value that can be obtained
    # with the first i items and a knapsack capacity of j
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill the table using dynamic programming
    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            weight_i = items[i - 1][2]  # Corrected indexing for weight
            value_i = items[i - 1][1]  # Corrected indexing for value
            if weight_i <= j:
                # If the current item's weight is less than or equal to the current capacity,
                # consider including it in the knapsack
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weight_i] + value_i)
            else:
                # If the current item's weight exceeds the current capacity,
                # do not include it in the knapsack
                dp[i][j] = dp[i - 1][j]

    # Reconstruct the selected items
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(items[i - 1])
            w -= items[i - 1][2]  # Corrected indexing for weight

    return dp[n][capacity], selected_items


def calculate_weight1(activity, possible_evas):
    return 1000 if len(possible_evas[activity]) == 1 else 0


def depth_first_search_duration(graph, node):
    if node.id != 'end':
        children = list(graph.get_children(node))

        results = []
        for child in children:
            results.append(depth_first_search_duration(graph, child))

        return sum(results) + 1
    else:
        return 0


def depth_first_search_successors(graph, node):
    if node.id != 'end':
        children = list(graph.get_children(node))

        results = []
        for child in children:
            results.append(depth_first_search_successors(graph, child))

        return sum(results) + 1
    else:
        return 0
