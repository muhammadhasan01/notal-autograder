import csv
import os

from data.coef_training_generator import main as coef_training_main
from grader.src.ged.classes.general_cost_function import RelabelMethod
from grader.src.ged.classes.graph import Graph as GGraph
from grader.src.ged.classes.graph_component import Node as GNode, Edge as GEdge
from grader.src.ged.utils.graph_collapser import collapse as grader_collapse, uncollapse, propagate_branching
from grader.src.grader import Grader, GraphPreprocessType
from graph_grader.src.grader.compare_graph import compare_graph
from graph_grader.src.utils.graph_collapser import collapse
from intermediate.src.classes.graph import Graph
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
HEADER = ['exam_name', 'number', 'nim', 'grade']
RESULT_FILE_NAME = 'Grade'


def main():
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
            graph = Graph(get_cfg(cur_path))
            collapse(graph)
            graph_inputs[nim] = graph

        if ANSWER_NAME_FILE not in graph_inputs:
            err_message = f'{ANSWER_NAME_FILE}.txt not found'
            logging.error(err_message)
            raise FileNotFoundError(err_message)

        graph_answer = graph_inputs[ANSWER_NAME_FILE]
        for nim, graph in graph_inputs.items():
            if nim == ANSWER_NAME_FILE:
                continue
            grade = compare_graph(graph_answer, graph)
            results.append((exam_name, number, nim, grade))
            logging.info(f'In {exam_name} - {number}, {nim} has a grade of {grade}')

        logging.info(f'Successfully generated {len(graph_inputs) - 1} submissions on exam={exam_name}')

    with open(f'{RESULT_FILE_NAME}.csv', 'w', encoding='UTF8', newline='') as exam_result:
        writer = csv.writer(exam_result)
        writer.writerow(HEADER)
        for res in results:
            writer.writerow(res)

    logging.info(f'Successfully generated {len(results)} result submissions')


def main2(relabel_method=RelabelMethod.BOOLEAN_COUNT,
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
            graph = Graph(get_cfg(cur_path, use_expression_type=True))
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
            grades, _, _ = grader.grade(graph, [graph_answer], time_limit, time_limit,
                                        relabel_method=relabel_method,
                                        graph_preprocess_type=graph_preprocess_type,
                                        node_cost=node_cost,
                                        edge_cost=edge_cost,
                                        is_exact_computation=is_exact_computation)
            grade = max(grades)
            results.append((exam_name, number, nim, grade))
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


def test_coef(relabel_method, graph_preprocess_type, node_cost, edge_cost):
    is_exact_computation = True
    filename = f'Test Coef_{relabel_method.name}_{graph_preprocess_type.name}.csv'
    if filename in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        return

    print(filename)
    main2(relabel_method=relabel_method,
          graph_preprocess_type=graph_preprocess_type,
          node_cost=node_cost,
          edge_cost=edge_cost,
          is_exact_computation=is_exact_computation,
          time_limit=5000,
          filename=filename)


if __name__ == "__main__":
    # main()
    # coef_training_main()
    # test_coef(RelabelMethod.BOOLEAN_COUNT, GraphPreprocessType.UNCOLLAPSE, 0.8584438636207447, 0.5129075287143761)
    for is_exact_computation in [False, True]:
        for edge_cost in range(1, 4):
            for node_cost in range(1, 4):
                if node_cost == edge_cost and node_cost != 1:
                    continue
                for relabel_method in RelabelMethod.__iter__():
                    for graph_preprocess_type in GraphPreprocessType.__iter__():
                        if graph_preprocess_type == GraphPreprocessType.UNCOLLAPSE and \
                                relabel_method != RelabelMethod.NONE and \
                                relabel_method != RelabelMethod.BOOLEAN_COUNT:
                            continue

                        pref = ''
                        if not is_exact_computation:
                            pref = 'APR_'

                        filename = f'{pref}{RESULT_FILE_NAME}_{relabel_method.name}_{graph_preprocess_type.name}_C{node_cost}{edge_cost}.csv'
                        if filename in os.listdir(os.path.dirname(os.path.abspath(__file__))):
                            continue

                        print(filename)
                        main2(relabel_method=relabel_method,
                              graph_preprocess_type=graph_preprocess_type,
                              node_cost=node_cost,
                              edge_cost=edge_cost,
                              is_exact_computation=is_exact_computation,
                              filename=filename)
