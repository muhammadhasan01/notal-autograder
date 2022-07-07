import copy


class GraphComponent:
    def __init__(self, component_id=None, info=[]):
        self.component_id: int = component_id
        self.info: list[dict] = info

    def get_id(self):
        return self.component_id

    def is_eps(self):
        return self.get_id() is None

    def is_not_eps(self):
        return self.get_id() is not None


class Node(GraphComponent):
    def __init__(self, component_id=None, info=[]):
        super().__init__(component_id, info)
        self.edges: list[Edge] = []
        self.out_edges: list[Edge] = []
        self.in_edges: list[Edge] = []

    def get_edges(self):
        return self.edges

    def set_edges(self, edges: list):
        self.edges = edges
        self.out_edges = []
        self.in_edges = []
        for edge in self.edges:
            if edge.from_node.get_id() == self.get_id():
                self.out_edges.append(edge)
            if edge.to_node.get_id() == self.get_id():
                self.in_edges.append(edge)

    def erase_edge(self, edge_id: int):
        self.edges = list(filter(lambda x: x.get_id() != edge_id, self.edges))
        self.out_edges = list(filter(lambda x: x.get_id() != edge_id, self.out_edges))
        self.in_edges = list(filter(lambda x: x.get_id() != edge_id, self.in_edges))

    def add_edge(self, edge):
        self.edges.append(edge)
        if edge.from_node.get_id() == self.get_id():
            self.out_edges.append(edge)
        if edge.to_node.get_id() == self.get_id():
            self.in_edges.append(edge)

    def get_out_edges(self):
        return self.out_edges

    def get_in_edges(self):
        return self.in_edges

    def get_edge_to(self, node):
        for edge in self.out_edges:
            if node.get_id() == edge.to_node.get_id():
                return edge
        return None

    def clone_node_only(self):
        node = Node(self.get_id(), copy.deepcopy(self.info))
        return node

    def __str__(self):
        edges = []
        for edge in self.edges:
            edges.append(f'{edge.get_id() : <3}: {(edge.from_node.get_id(), edge.to_node.get_id())}')
        ret = f'{self.get_id() : <3} label: {self.info}\n{"edges:" : <7} {edges}'
        return ret


class Edge(GraphComponent):
    def __init__(self, component_id=None, from_node=None, to_node=None, info=[]):
        super().__init__(component_id, info)
        self.from_node: Node = from_node
        self.to_node: Node = to_node

    def get_other_end(self, node: Node):
        if node.get_id() == self.from_node.get_id():
            return self.to_node
        return self.from_node

    def get_edge_type(self, node: Node):  # 0 out, 1 in, 2 self, 3 undef
        if node.get_id() == self.from_node.get_id():
            if node.get_id() == self.to_node.get_id():
                return 2
            return 0
        elif node.get_id() == self.to_node.get_id():
            return 1
        return 3

    def __str__(self):
        return f'{self.get_id(): <3}: {(self.from_node.get_id(), self.to_node.get_id())}'
