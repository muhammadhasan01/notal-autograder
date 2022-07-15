from graph_grader.src.grader.compare_graph import compare_graph
from graph_grader.src.utils.graph_collapser import collapse
from intermediate.src.classes.graph import Graph
from cfg_generator.src.api.functions import *
from cfg_generator.src.api.visualize_ast import visualize_ast
from cfg_generator.src.api.visualize_cfg import visualize_cfg

FILE_PATH_TEST = 'test.in'
FILE_PATH_ONE = 'input_1.in'
FILE_PATH_TWO = 'input_2.in'
FILE_PATH_THREE = 'while.in'


def test_generate_ast():
    ast = get_ast(FILE_PATH_TEST)
    visualize_ast(ast, 'test-output/ast.gv')


def test_generate_cfg():
    cfg = get_cfg(FILE_PATH_TEST)
    visualize_cfg(cfg, False, 'test-output/cfg.gv')


def test_generate_collapsed_cfg():
    g = Graph(get_cfg(FILE_PATH_TEST))
    collapse(g)
    visualize_cfg(g.generate_to_cfg_graph(), False, 'test-output/cfg-collapsed.gv')


def test_compare():
    cfg1 = get_cfg(FILE_PATH_ONE)
    cfg2 = get_cfg(FILE_PATH_TWO)
    g1 = Graph()
    g2 = Graph()
    g1.build_from_cfg_graph(cfg1)
    g2.build_from_cfg_graph(cfg2)
    visualize_cfg(cfg1, False, 'test-output/graph-1.gv')
    visualize_cfg(cfg2, False, 'test-output/graph-2.gv')

    score = compare_graph(g1, g2)
    print(score)


def test_collapse():
    cfg = get_cfg(FILE_PATH_THREE)
    g = Graph()
    g.build_from_cfg_graph(cfg)
    nodes = g.get_nodes()
    for node in nodes:
        print(node.get_label(), node.get_info(), ":")
        for in_node in node.get_in_nodes():
            print(in_node.get_label(), in_node.get_info())
    visualize_cfg(g.generate_to_cfg_graph())
    collapse(g)
    visualize_cfg(g.generate_to_cfg_graph(), False, 'test-output/new-result.gv')
