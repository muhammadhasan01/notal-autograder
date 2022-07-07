from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import *
from grader.src.ged.classes.cost_function import CostFunction
from grader.src.ged.utils.lsap_solver import Munkres
from grader.src.constants import Constants

import numpy as np


class EditPath:
    @classmethod
    def create_path(cls, cost_function: CostFunction, source: Graph, target: Graph,
                    starred_indices: list):
        snode_len = len(source.nodes)
        sedge_len = len(source.edges)
        tnode_len = len(target.nodes)
        tedge_len = len(target.edges)

        edit_path = EditPath(cost_function, source, target)
        for x in starred_indices:
            snode = Constants.NODE_EPS
            if x[0] < snode_len:
                snode = source.nodes[x[0]]

            tnode = Constants.NODE_EPS
            if x[1] < tnode_len:
                tnode = target.nodes[x[1]]

            if snode.is_not_eps() or tnode.is_not_eps():
                edit_path.add_mapping(snode, tnode)

        return edit_path

    @classmethod
    def create_root(cls, cost_function: CostFunction, source: Graph, target: Graph):
        edit_path = EditPath(cost_function, source, target)
        munkres = Munkres()
        matrix = edit_path.__build_node_matrix(edit_path.pending_nodes1, edit_path.pending_nodes2)
        total_cost = munkres.compute(matrix)
        starred_indices = munkres.get_starred_indices()
        edit_path.first_ub = starred_indices
        return edit_path

    @classmethod
    def clone(cls, edit_path):
        cloned = EditPath(edit_path.__cost_function)
        cloned.source = edit_path.source
        cloned.target = edit_path.target
        cloned.pending_nodes1.extend(edit_path.pending_nodes1)
        cloned.pending_edges1.extend(edit_path.pending_edges1)
        cloned.pending_nodes2.extend(edit_path.pending_nodes2)
        cloned.pending_edges2.extend(edit_path.pending_edges2)

        cloned.__total_cost = edit_path.__total_cost
        cloned.__heuristic_type = edit_path.__heuristic_type
        cloned.__heuristic_cost = edit_path.__heuristic_cost
        cloned.__is_heuristic_computed = edit_path.__is_heuristic_computed
        cloned.first_ub = edit_path.first_ub
        cloned.snode_mapping = copy.deepcopy(edit_path.snode_mapping)
        cloned.sedge_mapping = copy.deepcopy(edit_path.sedge_mapping)
        cloned.tnode_mapping = copy.deepcopy(edit_path.tnode_mapping)
        cloned.tedge_mapping = copy.deepcopy(edit_path.tedge_mapping)

        return cloned

    def __init__(self, cost_function: CostFunction, source: Graph = None, target: Graph = None,
                 heuristic_type: int = 1):
        self.source = source
        self.target = target

        self.pending_nodes1: list[Node] = []
        self.pending_edges1: list[Edge] = []
        self.pending_nodes2: list[Node] = []
        self.pending_edges2: list[Edge] = []

        if self.source is not None:
            self.pending_nodes1.extend(self.source.nodes)
            self.pending_edges1.extend(self.source.edges)

        if self.target is not None:
            self.pending_nodes2.extend(self.target.nodes)
            self.pending_edges2.extend(self.target.edges)

        # cost related
        self.__cost_function = cost_function

        self.__total_cost = 0.0
        self.__heuristic_type = heuristic_type
        self.__heuristic_cost = 0.0
        self.__is_heuristic_computed = False

        self.first_ub = []

        # distortion or mapping
        self.snode_mapping = {}
        self.sedge_mapping = {}
        self.tnode_mapping = {}
        self.tedge_mapping = {}

    def compute_heuristic_cost(self):
        if self.__is_heuristic_computed:
            return self.__heuristic_cost

        self.__is_heuristic_computed = True
        self.__heuristic_cost = 0.0
        if self.__heuristic_type == 1:
            self.__heuristic_cost = self.compute_heuristic_lsap()
        return self.__heuristic_cost

    def compute_heuristic_lsap(self):
        node_size1 = len(self.pending_nodes1)
        node_size2 = len(self.pending_nodes2)

        msize = node_size1 + node_size2
        if msize == 0:
            return 0.0

        matrix = np.zeros(shape=(msize, msize), dtype=float)
        for i in range(msize):
            node1 = Constants.NODE_EPS
            if i < node_size1:
                node1 = self.pending_nodes1[i]
            edges1 = node1.get_out_edges()
            for j in range(msize):
                node2 = Constants.NODE_EPS
                if j < node_size2:
                    node2 = self.pending_nodes2[j]
                edges2 = node2.get_out_edges()
                matrix[i][j] = self.__cost_function.get_node_cost(node1, node2) \
                               + self.__cost_function.get_edges_cost(edges1, edges2, node1, node2)

        return Munkres().compute(matrix)

    def predict_cost(self):
        return self.__total_cost + self.compute_heuristic_cost()

    def is_one_side_complete(self):
        return len(self.pending_nodes1) == 0 or len(self.pending_nodes2) == 0

    def complete(self):
        while len(self.pending_nodes2) > 0:
            self.add_mapping(Constants.NODE_EPS, self.pending_nodes2[0])

        while len(self.pending_nodes1) > 0:
            self.add_mapping(self.pending_nodes1[0], Constants.NODE_EPS)

    def __use_source_node(self, node: Node):
        self.pending_nodes1 = [x for x in self.pending_nodes1 if x.get_id() != node.get_id()]

    def __use_target_node(self, node: Node):
        self.pending_nodes2 = [x for x in self.pending_nodes2 if x.get_id() != node.get_id()]

    def __use_source_edge(self, edge: Edge):
        self.pending_edges1 = [x for x in self.pending_edges1 if x.get_id() != edge.get_id()]

    def __use_target_edge(self, edge: Edge):
        self.pending_edges2 = [x for x in self.pending_edges2 if x.get_id() != edge.get_id()]

    def add_mapping(self, component1: GraphComponent, component2: GraphComponent):
        if isinstance(component1, Node):
            self.__add_node_mapping(component1, component2)
        else:
            self.__add_edge_mapping(component1, component2)

    def __add_node_mapping(self, node1: Node, node2: Node):
        self.__is_heuristic_computed = False

        self.__total_cost += self.__cost_function.get_node_cost(node1, node2)
        if node1.is_not_eps():
            self.snode_mapping[node1] = node2
            self.__use_source_node(node1)
        if node2.is_not_eps():
            self.tnode_mapping[node2] = node1
            self.__use_target_node(node2)

        if node1.is_eps() and node2.is_eps():
            return

        # handle edges
        # node deletion
        if node2.is_eps():
            for edge1 in node1.edges:
                onode1 = edge1.get_other_end(node1)
                if onode1 in self.snode_mapping:
                    self.__add_edge_mapping(edge1, Constants.EDGE_EPS, node1, Constants.NODE_EPS)
            return

        # node insertion
        if node1.is_eps():
            for edge2 in node2.edges:
                onode2 = edge2.get_other_end(node2)
                if onode2 in self.tnode_mapping:
                    self.__add_edge_mapping(Constants.EDGE_EPS, edge2, Constants.NODE_EPS, node2)
            return

        for edge1 in node1.edges:
            onode1 = edge1.get_other_end(node1)
            is_out_edge = edge1.from_node.get_id() == node1.get_id()
            if onode1 in self.snode_mapping:
                onode2 = self.snode_mapping[onode1]
                if onode2.is_eps():
                    self.__add_edge_mapping(edge1, Constants.EDGE_EPS, node1, Constants.NODE_EPS)
                else:
                    edge2 = None
                    if is_out_edge:
                        edge2 = node2.get_edge_to(onode2)
                    else:
                        edge2 = onode2.get_edge_to(node2)

                    if edge2 is None:
                        self.__add_edge_mapping(edge1, Constants.EDGE_EPS, node1, Constants.NODE_EPS)
                    else:
                        self.__add_edge_mapping(edge1, edge2, node1, node2)

        for edge2 in node2.edges:
            onode2 = edge2.get_other_end(node2)
            is_out_edge = edge2.from_node.get_id() == node2.get_id()
            if onode2 in self.tnode_mapping:
                onode1 = self.tnode_mapping[onode2]
                if onode1.is_not_eps():
                    edge1 = None
                    if is_out_edge:
                        edge1 = node1.get_edge_to(onode1)
                    else:
                        edge1 = onode1.get_edge_to(node1)

                    if edge1 is None:
                        self.__add_edge_mapping(Constants.EDGE_EPS, edge2, Constants.NODE_EPS, node2)
                else:
                    self.__add_edge_mapping(Constants.EDGE_EPS, edge2, Constants.NODE_EPS, node2)

    def __add_edge_mapping(self, edge1: Edge, edge2: Edge, node1: Node, node2: Node):
        self.__is_heuristic_computed = False

        self.__total_cost += self.__cost_function.get_edge_cost(edge1, edge2, node1, node2)
        if edge1.is_not_eps():
            self.sedge_mapping[edge1] = edge2
            self.__use_source_edge(edge1)
        if edge2.is_not_eps():
            self.tedge_mapping[edge2] = edge1
            self.__use_target_edge(edge2)

    def __build_node_matrix(self, nodes1: list[Node], nodes2: list[Node]):
        munkres = Munkres()

        size1 = len(nodes1)
        size2 = len(nodes2)

        msize = size1 + size2
        matrix = np.zeros(shape=(msize, msize), dtype=float)  # [[0.0] * msize for i in range(msize)]

        for i in range(size1):
            u = nodes1[i]
            for j in range(size2):
                v = nodes2[j]
                matrix[i][j] = self.__cost_function.get_node_cost(u, v) \
                               + self.__cost_function.get_edges_cost(u.get_edges(), v.get_edges(), u, v)

        for i in range(size1, msize):
            u = Constants.NODE_EPS
            for j in range(size2):
                if i - size1 == j:
                    v = nodes2[j]
                    matrix[i][j] = self.__cost_function.get_node_cost(u, v) \
                                   + self.__cost_function.get_edges_cost(u.get_edges(), v.get_edges(), u, v)
                else:
                    matrix[i][j] = Constants.INF

        for i in range(size1):
            u = nodes1[i]
            for j in range(size2, msize):
                if j - size2 == i:
                    v = Constants.NODE_EPS
                    matrix[i][j] = self.__cost_function.get_node_cost(u, v) \
                                   + self.__cost_function.get_edges_cost(u.get_edges(), v.get_edges(), u, v)
                else:
                    matrix[i][j] = Constants.INF

        for i in range(size1, msize):
            for j in range(size2, msize):
                matrix[i][j] = 0.0

        return matrix

    # def build_edge_matrix(self, node1: Node, node2: Node):
    #     edges1 = node1.get_edges()
    #     edges2 = node2.get_edges()
    #     size1 = len(edges1)
    #     size2 = len(edges2)
    #     msize = size1 + size2
    #
    #     edge_matrix = np.zeros(shape=(msize, msize), dtype=float)  # [[0.0] * msize for i in range(msize)]
    #
    #     for i in range(size1):
    #         edge1 = edges1[i]
    #         for j in range(size2):
    #             edge2 = edges2[j]
    #             edge_matrix[i][j] = self.__cost_function.get_edge_cost(
    #                 edge1,
    #                 edge2,
    #                 node1,
    #                 node2
    #             )
    #
    #     for i in range(size1, msize):
    #         edge1 = Constants.EDGE_EPS
    #         for j in range(size2):
    #             if i - size1 == j:
    #                 edge2 = edges2[j]
    #                 edge_matrix[i][j] = self.__cost_function.get_edge_cost(
    #                     edge1,
    #                     edge2,
    #                     node1,
    #                     node2
    #                 )
    #             else:
    #                 edge_matrix[i][j] = Constants.INF
    #
    #     for i in range(size1):
    #         edge1 = edges1[i]
    #         for j in range(size2, msize):
    #             if j - size2 == i:
    #                 edge2 = Constants.EDGE_EPS
    #                 edge_matrix[i][j] = self.__cost_function.get_edge_cost(
    #                     edge1,
    #                     edge2,
    #                     node1,
    #                     node2
    #                 )
    #             else:
    #                 edge_matrix[i][j] = Constants.INF
    #
    #     for i in range(size1, msize):
    #         for j in range(size2, msize):
    #             edge_matrix[i][j] = 0.0
    #
    #     return edge_matrix
