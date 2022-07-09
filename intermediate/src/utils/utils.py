import copy
import os.path

from data.data_path import PARENT_DIR as DATA_ROOT
from intermediate.src.classes.graph import Graph

from grader.src.ged.classes.graph import Graph as GGraph
from grader.src.ged.classes.graph_component import Node as GNode, Edge as GEdge
from notal_to_cfg_generator.src.api.functions import get_cfg


def graph_to_grader_graph(graph: Graph):
    ggraph = GGraph()
    node_id = {}
    id_gnode = {}
    last_id = 0
    for node in graph.nodes:
        last_id += 1
        node_id[node] = last_id
        gnode = GNode(last_id, [{'label': info} for info in node.info])
        id_gnode[last_id] = gnode
        ggraph.add_node(gnode)

    for source in graph.nodes:
        source_id = node_id[source]
        for target in source.adjacent:
            target_id = node_id[target]
            last_id += 1

            gsource = id_gnode[source_id]
            gtarget = id_gnode[target_id]
            gedge = GEdge(last_id, gsource, gtarget)
            gsource.add_edge(gedge)
            gtarget.add_edge(gedge)
            ggraph.add_edge(gedge)
    return ggraph


if __name__ == '__main__':
    filename = os.path.join(DATA_ROOT, 'input_examples', 'notal', 'ekspresi.in')
    # filename = os.path.join(DATA_ROOT, 'exams', 'Kuis_2_IF2210_2020', 'IA', '10119048.txt')
    print(filename)
    graph = Graph(get_cfg(filename, use_expression_type=True))
    print(graph)
    ggraph = graph_to_grader_graph(graph)
    print(ggraph)
