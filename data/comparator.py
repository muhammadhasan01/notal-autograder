import os

from graph_grader.src.grader.compare_graph import compare_graph
from graph_grader.src.utils.graph_collapser import collapse
from intermediate.src.classes.graph import Graph
from notal_to_cfg_generator.src.api.functions import get_cfg

ANSWER_NAME_FILE = 'answer'


def main():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    print(parent_dir)
    kuis_2_ia = os.path.join(parent_dir, "exams\\Kuis_2_IF2210_2020\\IA")
    print(kuis_2_ia)
    input_files = os.listdir(kuis_2_ia)
    print(input_files)
    graph_inputs = {}
    for submission in input_files:
        name = submission.split('.')[0]
        cur_path = os.path.join(kuis_2_ia, submission)
        print(cur_path)
        graph = Graph(get_cfg(cur_path))
        collapse(graph)
        graph_inputs[name] = graph

    if ANSWER_NAME_FILE not in graph_inputs:
        raise FileNotFoundError(f'{ANSWER_NAME_FILE}.txt not found')

    graph_answer = graph_inputs[ANSWER_NAME_FILE]
    for name, graph in graph_inputs.items():
        if name == ANSWER_NAME_FILE:
            continue
        grade, _, _ = compare_graph(graph_answer, graph)
        print(name, grade)


if __name__ == "__main__":
    main()
