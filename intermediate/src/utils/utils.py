import os.path

from data.data_path import PARENT_DIR as DATA_ROOT
from intermediate.src.classes.graph import Graph

from grader.src.ged.classes.graph import Graph as GGraph
from grader.src.ged.classes.graph_component import Node as GNode, Edge as GEdge
from cfg_generator.src.api.functions import get_cfg


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
    from graph_grader.src.utils.graph_collapser import collapse
    from grader.src.ged.utils.graph_collapser import collapse as grader_collapse, uncollapse, propagate_branching

    # filename = os.path.join(DATA_ROOT, 'input_examples', 'notal', 'ekspresi.in')
    def check(filename):
        graph = Graph(get_cfg(filename, use_expression_type=True))
        ggraph = graph_to_grader_graph(graph)

        collapse(graph)
        graph = graph_to_grader_graph(graph)
        # print(graph)

        ggraph = grader_collapse(ggraph, collapse_branch_entry=False)
        # print(ggraph)

        def check_same(graph, ggraph):
            if not (len(graph.nodes) == len(ggraph.nodes) and len(graph.edges) == len(ggraph.edges)):
                return "FAIL"

            node_count = {}
            for node in graph.nodes:
                node_count[node.get_id()] = 1
            for node in ggraph.nodes:
                if node.get_id() not in node_count:
                    return "FAIL"
                node_count[node.get_id()] -= 1

            edge_count = {}
            for edge in graph.edges:
                e = (edge.from_node.get_id(), edge.to_node.get_id())
                edge_count[e] = 1
            for edge in ggraph.edges:
                e = (edge.from_node.get_id(), edge.to_node.get_id())
                if e not in edge_count:
                    return "FAIL"
                edge_count[e] -= 1

            for x in node_count.values():
                if x != 0:
                    return "FAIL"
            for x in edge_count.values():
                if x != 0:
                    return "FAIL"

            return "YUP"

        return check_same(graph, ggraph)
    # check(filename)
    path = os.path.join(DATA_ROOT, 'exams', 'Kuis_2_IF2210_2020', 'IC')
    # path = os.path.join(DATA_ROOT, 'exams', 'UTS_IF2210_2020', 'IB')
    for file in os.listdir(path):
        filename = os.path.join(path, file)
        print(f'{filename}: {check(filename)}')
