from common.classes.node import Node


class Graph:
    def __init__(self, cfg=None):
        self.nodes: list[Node] = []
        if cfg is not None:
            self.build_from_cfg_graph(cfg)

    def add_node(self, node: Node):
        self.nodes.append(node)

    def get_edges(self):
        edges: list[tuple[Node, Node]] = []
        for u in self.nodes:
            for v in u.get_adjacent():
                edges.append((u, v))
        return edges

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
