from abc import ABC, abstractmethod

from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import *
import numpy as np


class CostFunction(ABC):
    def __init__(self, do_node_precompute=False):
        self.do_node_precompute = do_node_precompute
        self.snode_size: int = None
        self.tnode_size: int = None
        self.node_precompute: list[list] = None

    def set_precompute(self, source: Graph, target: Graph):  # Graph component_id should be continuous from 1 to N
        self.do_node_precompute = True

        self.snode_size = len(source.nodes)
        self.tnode_size = len(target.nodes)

        self.node_precompute = np.ndarray(shape=(self.snode_size + 1, self.tnode_size + 1), dtype=float)
        self.node_precompute.fill(-1.0)

    def clear_precompute(self):
        self.node_precompute.fill(-1.0)

    @abstractmethod
    def get_node_cost(self, a: Node, b: Node):
        pass

    @abstractmethod
    def get_edge_cost(self, a: Edge, b: Edge, a_node: Node, b_node: Node):
        pass

    @abstractmethod
    def get_edges_cost(self, a: list[Edge], b: list[Edge], a_node: Node, b_node: Node):
        pass
