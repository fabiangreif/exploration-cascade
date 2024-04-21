from models.edge import Edge
from models.graph import Graph
from models.node import Node


def create_dependency_graph(d, activities):
    start_node = Node(None, 'start')
    end_node = Node(None, 'end')
    nodes = [start_node, end_node]
    edges = []

    for activity in activities:
        nodes.append(Node(activity, activity.id))

    for i, row in enumerate(d):
        for j, cell in enumerate(row):
            if cell == 1:
                edges.append(Edge(Node(activities[j], activities[j].id), Node(activities[i], activities[i].id)))

    for i, row in enumerate(d):
        if sum(row) == 0:
            edges.append(Edge(start_node, Node(activities[i], activities[i].id)))

    for j in range(len(d)):
        column = []
        for i, row in enumerate(d):
            column.append(row[j])
        if sum(column) == 0:
            edges.append(Edge(Node(activities[j], activities[j].id), end_node))

    return Graph(nodes, edges)
