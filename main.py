from datetime import datetime

from dependency_graph_creation import create_dependency_graph
from dependency_graph_traversal import traverse_dependency_graph
from filtering import calculate_filter_matrix
from models.activity import Activity
from models.eva import EVA


def test():
    dependencies = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [1, 0, 1, 0]
    ]

    activities = [
        Activity(0, 100, []),
        Activity(1, 100, []),
        Activity(2, 100, []),
        Activity(3, 100, [])
    ]

    evas = [
        EVA(0, datetime.fromisoformat('2011-11-04T00:05:23+00:00'), 180, 0.1, []),
        EVA(1, datetime.fromisoformat('2011-11-05T00:05:23+00:00'), 180, 0.1, []),
        EVA(2, datetime.fromisoformat('2011-11-06T00:05:23+00:00'), 180, 0.1, []),
        EVA(3, datetime.fromisoformat('2011-11-07T00:05:23+00:00'), 180, 0.1, []),
        EVA(4, datetime.fromisoformat('2011-11-08T00:05:23+00:00'), 180, 0.1, [])
    ]

    p = calculate_filter_matrix(activities, evas)
    dependency_graph = create_dependency_graph(dependencies, activities)
    c = traverse_dependency_graph(activities, evas, dependency_graph, p, dependencies)

    print(c)


if __name__ == '__main__':
    test()
