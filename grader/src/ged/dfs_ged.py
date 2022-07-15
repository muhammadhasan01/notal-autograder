import time
from typing import Callable

from grader.src.api.functions import is_graph_components_id_ordered
from grader.src.ged.classes.edit_path import EditPath
from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.cost_function import CostFunction
from grader.src.ged.classes.search_node import SearchNode
from grader.src.constants import Constants


class DFSGED:
    """
    precondition:
    - each graph nodes should have component_id in the range [1, len(nodes)]
    - each graph edges should have component_id in the range [len(nodes) + 1, len(nodes) + len(edges)]

    note: precondition exist to sped up computation
    """

    def __init__(self, source: Graph, target: Graph, cost_function: CostFunction, time_limit=3000):
        assert (is_graph_components_id_ordered(source) and is_graph_components_id_ordered(target))

        self.source = source
        self.target = target
        self.cost_function = cost_function
        self.cost_function.set_precompute(source, target)

        # time limit in milliseconds
        self.__start_time = None
        self.__time_limit = time_limit

        # bound
        self.ub_path: EditPath = None
        self.ub_cost: float = Constants.INF

        self.is_solution_optimal = False

    def reset(self):
        self.ub_path: EditPath = None
        self.ub_cost: float = Constants.INF
        self.is_solution_optimal = False

    def set_time_limit(self, time_limit):
        self.__time_limit = time_limit

    def __search_ged(self, no_edit: EditPath):
        cur_node = SearchNode(no_edit)
        while cur_node is not None:
            cur_time = time.time_ns()
            if cur_time - self.__start_time >= self.__time_limit * 1000000:
                self.is_solution_optimal = False
                break

            if cur_node.edit_path.is_one_side_complete():
                cur_node.edit_path.complete()
                total_edit_cost = cur_node.edit_path.predict_cost()
                if self.ub_cost > total_edit_cost:
                    self.ub_cost = total_edit_cost
                    self.ub_path = cur_node.edit_path
                cur_node = cur_node.parent
            else:
                if len(cur_node.children) == 0 and not cur_node.sorted:  # check if not generated yet
                    self.__generate_children(cur_node)
                if len(cur_node.children) == 0:
                    cur_node = cur_node.parent
                else:
                    candidate_node = cur_node.remove_min_child()
                    if candidate_node.edit_path.predict_cost() >= self.ub_cost:
                        candidate_node = cur_node.parent
                    cur_node = candidate_node

    def __generate_children(self, search_node: SearchNode):
        edit_path = search_node.edit_path
        if len(edit_path.pending_nodes1) > 0:
            node1 = edit_path.pending_nodes1[0]
            for node2 in edit_path.pending_nodes2:
                ch_edit_path = EditPath.clone(edit_path)
                ch_edit_path.add_mapping(node1, node2)
                if ch_edit_path.is_one_side_complete():
                    ch_edit_path.complete()
                if ch_edit_path.predict_cost() < self.ub_cost:
                    search_node.add_child(ch_edit_path)

            ch_edit_path = EditPath.clone(edit_path)
            ch_edit_path.add_mapping(node1, Constants.NODE_EPS)
            if ch_edit_path.is_one_side_complete():
                ch_edit_path.complete()
            if ch_edit_path.predict_cost() < self.ub_cost:
                search_node.add_child(ch_edit_path)

    def compute_edit_distance(self, is_exact_computation=True, ub_cost=Constants.INF) -> float:
        self.cost_function.clear_precompute()

        # start timer
        self.__start_time = time.time_ns()
        self.ub_cost = ub_cost

        # creates root
        root, hu_approximation = EditPath.create_root(self.cost_function, self.source, self.target)

        self.ub_path = EditPath.create_path(self.cost_function, self.source, self.target, root.first_ub)
        self.ub_cost = min(self.ub_path.predict_cost(), self.ub_cost)

        if is_exact_computation:
            self.is_solution_optimal = True
            self.__search_ged(root)

            return self.ub_cost
        else:
            self.ub_cost = min(hu_approximation, self.ub_cost)
            return self.ub_cost

    def normalized_ed_to_ed(self, distance):
        if distance > 1:
            return Constants.INF
        elif distance < 0:
            return 0
        snode_size = len(self.source.nodes)
        tnode_size = len(self.target.nodes)
        sedge_size = len(self.source.edges)
        tedge_size = len(self.target.edges)

        return distance * ((snode_size + tnode_size) * self.cost_function.node_cost +
                           (sedge_size + tedge_size) * self.cost_function.edge_cost)

    def get_string_node_map(self):
        ret = []
        for k, v in self.ub_path.snode_mapping.items():
            ret.append(f'{k.get_id() : <4} -> {v.get_id()}')
        for k, v in self.ub_path.tnode_mapping.items():
            if v.is_eps():
                ret.append(f'{"EPS" : <4} -> {k.get_id()}')
        return '\n'.join(ret)

    def get_edit_distance(self) -> float:
        return self.ub_cost

    def get_normalized_edit_distance(self) -> float:
        snode_size = len(self.source.nodes)
        tnode_size = len(self.target.nodes)
        sedge_size = len(self.source.edges)
        tedge_size = len(self.target.edges)

        ret = self.ub_cost / ((snode_size + tnode_size) * self.cost_function.node_cost +
                               (sedge_size + tedge_size) * self.cost_function.edge_cost)
        return min(1, ret)

    def get_similarity_score(self, func: Callable[[float], float] = None) -> float:
        if func is None:
            return 1 - self.get_normalized_edit_distance()
        return func(1 - self.get_normalized_edit_distance())

    def is_valid_exact_computation(self):
        EPS = 1e-5
        total_cost = 0.0

        for node1 in self.source.nodes:
            if node1.get_id() not in self.ub_path.snode_mapping:
                return False
            node2 = self.ub_path.snode_mapping[node1.get_id()]
            total_cost += self.cost_function.get_node_cost(node1, node2)
        for node2 in self.target.nodes:
            if node2.get_id() not in self.ub_path.tnode_mapping:
                return False
            node1 = self.ub_path.tnode_mapping[node2.get_id()]
            if node1.is_eps():
                total_cost += self.cost_function.get_node_cost(node1, node2)

        for edge1 in self.source.edges:
            if edge1.get_id() not in self.ub_path.sedge_mapping:
                return False
            edge2 = self.ub_path.sedge_mapping[edge1.get_id()]
            if edge2.is_eps():
                total_cost += self.cost_function.edge_cost
            else:
                if edge2.from_node == self.ub_path.snode_mapping[edge1.from_node.get_id()] and \
                        edge2.to_node == self.ub_path.snode_mapping[edge1.to_node.get_id()]:
                    continue
                total_cost += self.cost_function.edge_cost * 2
        for edge2 in self.target.edges:
            if edge2.get_id() not in self.ub_path.tedge_mapping:
                return False
            edge1 = self.ub_path.tedge_mapping[edge2.get_id()]
            if edge1.is_eps():
                total_cost += self.cost_function.edge_cost
            else:
                if edge1.from_node == self.ub_path.tnode_mapping[edge2.from_node.get_id()] and \
                        edge1.to_node == self.ub_path.tnode_mapping[edge2.to_node.get_id()]:
                    continue
                total_cost += self.cost_function.edge_cost * 2

        diff = abs(self.ub_cost - total_cost)
        return diff <= EPS
