class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def get_start_node(self):
        return self.nodes[0]

    def get_end_node(self):
        return self.nodes[-1]

    def get_children(self, node):
        return filter(lambda n: any((edge.node1.id == node.id and edge.node2.id == n.id) for edge in self.edges),
                      self.nodes)

    def get_node_dictionary(self, value):
        dictionary = {}
        for node in self.nodes:
            dictionary[node.id] = value

        return dictionary

    def get_node_by_id(self, id):
        return next((node for node in self.nodes if node.id == id), None)
