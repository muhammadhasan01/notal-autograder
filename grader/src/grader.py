import time
from enum import Enum

from grader.src.constants import Constants
from grader.src.ged.classes.cost_function import CostFunction
from grader.src.ged.classes.general_cost_function import GeneralCostFunction, RelabelMethod
from grader.src.ged.classes.graph import Graph
from grader.src.ged.dfs_ged import DFSGED
from grader.src.ged.utils.graph_collapser import *


class GraphPreprocessType(Enum):
    UNCOLLAPSE = 0
    COLLAPSE = 1
    COLLAPSE_NBE = 2
    PROPAGATE_BRANCHING = 3


class Grader:
    def preprocess_graph(self, graph: Graph, preproc_type):
        if preproc_type == GraphPreprocessType.UNCOLLAPSE:
            graph = uncollapse(graph)
        elif preproc_type == GraphPreprocessType.COLLAPSE:
            graph = collapse(graph)
        elif preproc_type == GraphPreprocessType.COLLAPSE_NBE:
            graph = collapse(graph, collapse_branch_entry=False)
        elif preproc_type == GraphPreprocessType.PROPAGATE_BRANCHING:
            graph = propagate_branching(graph)
        return graph

    def __grade_one_on_one(self, graph_source: Graph,
                           graph_target: Graph,
                           time_limit: int,
                           cost_function: CostFunction = None,
                           is_exact_computation=True,
                           ub_normal_cost=Constants.INF,
                           node_key: str = "label") -> float:
        if cost_function is None:
            cost_function = GeneralCostFunction(node_key=node_key)

        dfs_ged = DFSGED(graph_source, graph_target, cost_function, time_limit)
        dfs_ged.compute_edit_distance(is_exact_computation=is_exact_computation,
                                      ub_cost=dfs_ged.normalized_ed_to_ed(ub_normal_cost))
        new_ub_normal_cost = dfs_ged.get_normalized_edit_distance()
        score = dfs_ged.get_similarity_score()

        return score * Constants.MAX_SCORE, new_ub_normal_cost

    def grade(self, graph_source: Graph,
              graph_targets: list[Graph],
              time_limit: int,
              time_limit_per_unit: int,
              relabel_method=RelabelMethod.BOOLEAN_COUNT,
              node_cost=1,
              edge_cost=1,
              graph_preprocess_type=GraphPreprocessType.PROPAGATE_BRANCHING,
              is_exact_computation=True,
              use_ub=False,
              node_key: str = "label") -> tuple[list, list, list]:
        graph_source = self.preprocess_graph(graph_source, graph_preprocess_type)
        graph_targets = [self.preprocess_graph(graph, graph_preprocess_type) for graph in graph_targets]
        cost_function = GeneralCostFunction(relabel_method=relabel_method, node_cost=node_cost, edge_cost=edge_cost, node_key=node_key)
        scores = []
        errors = []
        feedback = []

        start_time = time.time_ns()
        ub_normal_cost = Constants.INF
        for graph_target in graph_targets:
            cur_time = time.time_ns()
            if cur_time - start_time < time_limit * 1000000:
                remaining_time = (time_limit * 1000000 - (cur_time - start_time)) // 1000000
                try:
                    score, cur_ub_normal_cost = self.__grade_one_on_one(graph_source,
                                                                        graph_target,
                                                                        min(time_limit_per_unit, remaining_time),
                                                                        cost_function,
                                                                        is_exact_computation=is_exact_computation,
                                                                        ub_normal_cost=ub_normal_cost)
                    if use_ub:
                        ub_normal_cost = min(ub_normal_cost, cur_ub_normal_cost)
                    scores.append(score)
                    errors.append(None)
                    feedback.append("Success")
                except Exception as e:
                    scores.append(0)
                    errors.append(e)
                    feedback.append("Failed to grade")
            else:
                scores.append(0)
                errors.append(None)
                feedback.append("Grader time limit exceeded")

        return scores, errors, feedback
