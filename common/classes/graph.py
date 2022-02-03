from common.classes.node import Node


class Graph:
    def __init__(self, cfg=None):
        self.nodes: list[Node] = []
        self.edges: list[tuple[Node, Node]] = []
        if cfg is not None:
            self.build_from_cfg_graph(cfg)

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edges(self, u: Node, v: Node):
        self.edges.append((u, v))

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def build_from_cfg_graph(self, cfg):
        for node in cfg:
            self.add_node(node)
            for adj_node in node.get_adjacent():
                self.add_edges(node, adj_node)
