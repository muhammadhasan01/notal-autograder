import csv
import os
import time

from grader.src.constants import Constants
from grader.src.ged.classes.cost_function import CostFunction
from grader.src.ged.classes.general_cost_function import RelabelMethod, GeneralCostFunction
from grader.src.ged.classes.graph import Graph
from grader.src.ged.dfs_ged import DFSGED
from grader.src.ged.utils.graph_collapser import collapse as collapse, uncollapse, propagate_branching
from grader.src.grader import GraphPreprocessType
from graph_grader.src.grader.compare_graph import compare_graph
from intermediate.src.classes.graph import Graph as IGraph
from intermediate.src.utils.utils import graph_to_grader_graph
from cfg_generator.src.api.functions import get_cfg
import logging

ANSWER_NAME_FILE = 'answer'
EXAM_DIRECTORIES = {
    ('Kuis 2', 'IA'): 'Kuis_2_IF2210_2020\\IA',
    ('Kuis 2', 'IB'): 'Kuis_2_IF2210_2020\\IB',
    ('Kuis 2', 'IC'): 'Kuis_2_IF2210_2020\\IC',
    ('UTS', 'IA'): 'UTS_IF2210_2020\\IA',
    ('UTS', 'IB'): 'UTS_IF2210_2020\\IB'
}
HEADER = ['exam_name', 'number', 'nim', 'grade', 'time_spent', 'is_guaranteed_optimal', 'node_count1', 'node_count2']
RESULT_FILE_NAME = 'Time Data'


class Grader:
    def preprocess_graph(self, graph: Graph, preproc_type):
        if preproc_type == GraphPreprocessType.UNCOLLAPSE:
            graph = uncollapse(graph)
        elif preproc_type == GraphPreprocessType.COLLAPSE:
            graph = collapse(graph)
        elif preproc_type == GraphPreprocessType.PROPAGATE_BRANCHING:
            graph = propagate_branching(graph)
        return graph

    def get_node_edge_ed(self, dfs_ged) -> [float, float]:
        EPS = 1e-5
        total_node_cost = 0.0
        total_edge_cost = 0.0

        for node1 in dfs_ged.source.nodes:
            if node1.get_id() not in dfs_ged.ub_path.snode_mapping:
                return False
            node2 = dfs_ged.ub_path.snode_mapping[node1.get_id()]
            total_node_cost += dfs_ged.cost_function.get_node_cost(node1, node2)
        for node2 in dfs_ged.target.nodes:
            if node2.get_id() not in dfs_ged.ub_path.tnode_mapping:
                return False
            node1 = dfs_ged.ub_path.tnode_mapping[node2.get_id()]
            if node1.is_eps():
                total_node_cost += dfs_ged.cost_function.get_node_cost(node1, node2)

        for edge1 in dfs_ged.source.edges:
            if edge1.get_id() not in dfs_ged.ub_path.sedge_mapping:
                return False
            edge2 = dfs_ged.ub_path.sedge_mapping[edge1.get_id()]
            if edge2.is_eps():
                total_edge_cost += dfs_ged.cost_function.edge_cost
            else:
                if edge2.from_node == dfs_ged.ub_path.snode_mapping[edge1.from_node.get_id()] and \
                        edge2.to_node == dfs_ged.ub_path.snode_mapping[edge1.to_node.get_id()]:
                    continue
                total_edge_cost += dfs_ged.cost_function.edge_cost * 2
        for edge2 in dfs_ged.target.edges:
            if edge2.get_id() not in dfs_ged.ub_path.tedge_mapping:
                return False
            edge1 = dfs_ged.ub_path.tedge_mapping[edge2.get_id()]
            if edge1.is_eps():
                total_edge_cost += dfs_ged.cost_function.edge_cost
            else:
                if edge1.from_node == dfs_ged.ub_path.tnode_mapping[edge2.from_node.get_id()] and \
                        edge1.to_node == dfs_ged.ub_path.tnode_mapping[edge2.to_node.get_id()]:
                    continue
                total_edge_cost += dfs_ged.cost_function.edge_cost * 2

        return total_node_cost, total_edge_cost

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
        # total_node_cost, total_edge_cost = self.get_node_edge_ed(dfs_ged)
        if dfs_ged.time_spent < time_limit:
            assert dfs_ged.is_solution_optimal
        new_ub_normal_cost = dfs_ged.get_normalized_edit_distance()
        score = dfs_ged.get_similarity_score()

        return score * Constants.MAX_SCORE, new_ub_normal_cost, dfs_ged.time_spent, dfs_ged.is_solution_optimal

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
        cost_function = GeneralCostFunction(relabel_method=relabel_method, node_cost=node_cost, edge_cost=edge_cost,
                                            node_key=node_key)
        scores = []
        mx_score = 0
        errors = []
        feedback = []
        time_spent = 0
        is_guaranteed_optimal = False
        node_count1 = 0
        node_count2 = 0
        edge_count = 0

        start_time = time.time_ns()
        ub_normal_cost = Constants.INF
        for graph_target in graph_targets:
            cur_time = time.time_ns()
            if cur_time - start_time < time_limit * 1000000:
                remaining_time = (time_limit * 1000000 - (cur_time - start_time)) // 1000000
                try:
                    score, cur_ub_normal_cost, cur_time_spent, cur_is_guaranteed_optimal = self.__grade_one_on_one(
                        graph_source,
                        graph_target,
                        min(time_limit_per_unit,
                            remaining_time),
                        cost_function,
                        is_exact_computation=is_exact_computation,
                        ub_normal_cost=ub_normal_cost)
                    if use_ub:
                        ub_normal_cost = min(ub_normal_cost, cur_ub_normal_cost)
                    scores.append(score)
                    errors.append(None)
                    feedback.append("Success")
                    if mx_score < score:
                        mx_score = score
                        time_spent = cur_time_spent
                        is_guaranteed_optimal = cur_is_guaranteed_optimal
                        node_count1 = len(graph_source.nodes)
                        node_count2 = len(graph_target.nodes)
                        edge_count = len(graph_source.edges) + len(graph_target.edges)
                except Exception as e:
                    scores.append(0)
                    errors.append(e)
                    feedback.append("Failed to grade")
            else:
                scores.append(0)
                errors.append(None)
                feedback.append("Grader time limit exceeded")

        return score, time_spent, is_guaranteed_optimal, node_count1, node_count2


def main_test(relabel_method=RelabelMethod.BOOLEAN_COUNT,
              graph_preprocess_type=GraphPreprocessType.COLLAPSE,
              node_cost=1,
              edge_cost=1,
              is_exact_computation=True,
              write_csv=True,
              time_limit=3000,
              filename='Something.csv'):
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    results: list[tuple[str, str, str, str]] = []

    for exam, dir_exam in EXAM_DIRECTORIES.items():
        exam_name, number = exam
        logging.info(f'Grading for exam={exam_name} and number={number}')
        cur_dir = os.path.join(parent_dir, f'exams\\{dir_exam}')
        input_files = os.listdir(cur_dir)
        graph_inputs: dict[str, Graph] = {}
        for submission in input_files:
            nim = submission.split('.')[0]
            cur_path = os.path.join(cur_dir, submission)
            logging.info(f'Generating CFG of {nim} submission in exam={exam_name} - {number}')
            graph = IGraph(get_cfg(cur_path, use_expression_type=True))
            graph_inputs[nim] = graph_to_grader_graph(graph)

        if ANSWER_NAME_FILE not in graph_inputs:
            err_message = f'{ANSWER_NAME_FILE}.txt not found'
            logging.error(err_message)
            raise FileNotFoundError(err_message)

        graph_answer = graph_inputs[ANSWER_NAME_FILE]
        grader = Grader()
        for nim, graph in graph_inputs.items():
            if nim == ANSWER_NAME_FILE:
                continue
            grade, time_spent, is_guaranteed_optimal, node_count1, node_count2 = grader.grade(graph, [graph_answer], time_limit,
                                                                                time_limit,
                                                                                relabel_method=relabel_method,
                                                                                graph_preprocess_type=graph_preprocess_type,
                                                                                node_cost=node_cost,
                                                                                edge_cost=edge_cost,
                                                                                is_exact_computation=is_exact_computation)
            results.append((exam_name, number, nim, grade, time_spent, is_guaranteed_optimal, node_count1, node_count2))
            logging.info(f'In {exam_name} - {number}, {nim} has a grade of {grade}')

        logging.info(f'Successfully generated {len(graph_inputs) - 1} submissions on exam={exam_name}')

    if write_csv:
        with open(filename, 'w', encoding='UTF8', newline='') as exam_result:
            writer = csv.writer(exam_result)
            writer.writerow(HEADER)
            for res in results:
                writer.writerow(res)
    else:
        return HEADER, results

    logging.info(f'Successfully generated {len(results)} result submissions')


def main(time_limit):
    is_exact_computation = True
    node_cost = 3
    edge_cost = 1
    relabel_method = RelabelMethod.BOOLEAN_COUNT
    graph_preprocess_type = GraphPreprocessType.UNCOLLAPSE
    # for relabel_method in RelabelMethod.__iter__():
    #     for graph_preprocess_type in GraphPreprocessType.__iter__():
    #         if graph_preprocess_type == GraphPreprocessType.UNCOLLAPSE and \
    #                 relabel_method != RelabelMethod.NONE and \
    #                 relabel_method != RelabelMethod.BOOLEAN_COUNT:
    #             continue

    filename = f'{RESULT_FILE_NAME}_{relabel_method.name}_{graph_preprocess_type.name}_{time_limit}_C{node_cost}{edge_cost}.csv'
    if filename not in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        print(filename)
        main_test(relabel_method=relabel_method, graph_preprocess_type=graph_preprocess_type,
                  node_cost=node_cost, edge_cost=edge_cost, is_exact_computation=is_exact_computation,
                  time_limit=time_limit, filename=filename)


if __name__ == "__main__":
    for time_limit in [1000, 3000, 10000, 20000]:
        main(time_limit)
