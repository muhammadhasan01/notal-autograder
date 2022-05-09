import csv
import os

from graph_grader.src.grader.compare_graph import compare_graph
from graph_grader.src.utils.graph_collapser import collapse
from intermediate.src.classes.graph import Graph
from notal_to_cfg_generator.src.api.functions import get_cfg
import logging

ANSWER_NAME_FILE = 'answer'
EXAM_DIRECTORIES = {
    'Kuis 2 IA': 'Kuis_2_IF2210_2020\\IA'
}
HEADER = ['exam_name', 'nim', 'grade']


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    results: list[tuple[str, str, str]] = []

    for exam_name, dir_exam in EXAM_DIRECTORIES.items():
        logging.info(f'Comparing Answer for exam={exam_name}')
        cur_dir = os.path.join(parent_dir, f'exams\\{dir_exam}')
        input_files = os.listdir(cur_dir)
        graph_inputs: dict[str, Graph] = {}
        for submission in input_files:
            nim = submission.split('.')[0]
            cur_path = os.path.join(cur_dir, submission)
            graph = Graph(get_cfg(cur_path))
            collapse(graph)
            graph_inputs[nim] = graph

        if ANSWER_NAME_FILE not in graph_inputs:
            raise FileNotFoundError(f'{ANSWER_NAME_FILE}.txt not found')

        graph_answer = graph_inputs[ANSWER_NAME_FILE]
        for nim, graph in graph_inputs.items():
            if nim == ANSWER_NAME_FILE:
                continue
            grade, _, _ = compare_graph(graph_answer, graph)
            results.append((exam_name, nim, grade))
            logging.info(f'In {exam_name}, {nim} has a grade of {grade}')

        logging.info(f'Successfully generated {len(graph_inputs) - 1} submissions on exam={exam_name}')

    with open(f'results.csv', 'w', encoding='UTF8', newline='') as exam_result:
        writer = csv.writer(exam_result)
        writer.writerow(HEADER)
        for res in results:
            writer.writerow(res)


if __name__ == "__main__":
    main()
