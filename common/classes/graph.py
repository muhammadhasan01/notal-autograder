from common.classes.node import Node


class Graph:
    def __init__(self):
        self.nodes: list[Node] = []
        self.edges: list[tuple[Node, Node]] = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edges(self, u: Node, v: Node):
        self.edges.append((u, v))

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges
