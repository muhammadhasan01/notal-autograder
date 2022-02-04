from common.classes.node import Node


class Graph:
    def __init__(self, cfg=None):
        self.nodes: list[Node] = []
        if cfg is not None:
            self.build_from_cfg_graph(cfg)

    def add_node(self, node: Node):
        self.nodes.append(node)

    def get_clone(self):
        g = Graph()
        for u in self.nodes:
            new_node = Node(u.get_label(), u.get_info())
            g.add_node(new_node)

        for i, u in enumerate(self.nodes):
            cur_node = g.get_node(u.get_label())
            for v in u.get_adjacent():
                adj_node = g.get_node(v.get_label())
                cur_node.add_adjacent(adj_node)

        return g

    def get_edges(self):
        edges: list[tuple[Node, Node]] = []
        for u in self.nodes:
            for v in u.get_adjacent():
                edges.append((u, v))
        return edges

    def get_node(self, label):
        if label < 1 or label > len(self.nodes):
            raise IndexError("Label graph out of range")
        return self.nodes[label - 1]

    def get_nodes(self):
        return self.nodes

    def set_nodes(self, nodes: list[Node]):
        self.nodes = nodes

    def build_from_cfg_graph(self, cfg: dict):
        for node in cfg:
            self.add_node(node)

    def generate_to_cfg_graph(self):
        cfg = {}
        for node in self.nodes:
            cfg[node] = node.get_adjacent()
        return cfg
