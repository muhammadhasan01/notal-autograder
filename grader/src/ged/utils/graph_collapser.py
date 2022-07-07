import copy

from grader.src.api.functions import *

from grader.src.ged.utils.dsu import CollapserDSU
from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import *


def collapse(input_graph: Graph):
    """
    Collapse graph nodes and edges if merging is possible.

    Note: Graph collapsing would not preserve information in edges that were collapsed
    """
    input_graph = compress_graph_component_id(input_graph)
    nodes = input_graph.nodes
    edges = input_graph.edges
    dsu = CollapserDSU(nodes)

    # Merge nodes with the same flow
    for node in nodes:
        out_edges = node.get_out_edges()
        if len(out_edges) > 1:
            continue

        id = node.get_id()
        for out_edge in out_edges:
            out_node = out_edge.to_node
            adj_id = out_node.get_id()
            if len(out_node.get_in_edges()) <= 1:
                dsu.merge(id, adj_id)

    graph = Graph()
    id_node = {}
    for node in nodes:
        if node.get_id() == dsu.find_par(node.get_id()):
            new_node = Node(node.get_id(), dsu.info[node.get_id()])
            graph.add_node(new_node)
            id_node[new_node.get_id()] = new_node

    for edge in edges:
        new_from_id = dsu.find_par(edge.from_node.get_id())
        new_to_id = dsu.find_par(edge.to_node.get_id())

        if new_from_id != new_to_id or edge.from_node.get_id() == edge.to_node.get_id():
            from_node = id_node[new_from_id]
            to_node = id_node[new_to_id]
            new_edge = Edge(edge.get_id(), from_node, to_node, copy.deepcopy(edge.info))

            from_node.add_edge(new_edge)
            if from_node.get_id() != to_node.get_id():
                to_node.add_edge(new_edge)
            graph.add_edge(new_edge)

    # Erase empty node if in-nodes and out-nodes can be connected directly
    last_id = graph.find_last_id()
    erased_nodes = []
    for node in graph.nodes:
        if len(node.info) == 0 and len(node.in_edges) == 1 and len(node.out_edges) == 1:
            if node.in_edges[0].get_id() == node.out_edges[0].get_id():
                continue
            erased_nodes.append(node)

    for node in erased_nodes:
        prev_node = node.in_edges[0].from_node
        next_node = node.out_edges[0].to_node
        graph.erase_node(node.get_id())

        last_id += 1
        new_edge = Edge(last_id, prev_node, next_node)

        prev_node.add_edge(new_edge)
        if prev_node.get_id() != next_node.get_id():
            next_node.add_edge(new_edge)
        graph.add_edge(new_edge)

    return compress_graph_component_id(graph)


def propagate_branching(input_graph: Graph, node_key: str = "label"):
    """
    Propagate branching on if statement
    """
    graph = collapse(input_graph)
    last_id = 0
    for node in graph.nodes:
        new_info = []
        for info in node.info:
            new_info.append({ikey: info[ikey] for ikey in info if ikey == node_key})
        node.info = new_info
        last_id = max(last_id, node.get_id())
        for edge in node.out_edges:
            last_id = max(last_id, edge.get_id())

    while True:
        erase_nodes = []
        found = False
        for node in graph.nodes:
            if not (len(node.in_edges) == 1 and len(node.out_edges) > 1):
                continue
            parent = node.in_edges[0].from_node
            if len(node.info) == 0 or len(parent.info) == 0:
                continue
            parent_last = parent.info[-1][node_key]
            last = node.info[-1][node_key]
            if last != parent_last or node.get_id() == parent.get_id():
                continue
            found = True

            # Add intermediate nodes
            added_intermediate = set()
            erase_edges = []
            new_edges = []
            for edge in node.out_edges:
                onode = edge.to_node
                if onode.get_id() in added_intermediate:
                    erase_edges.append(edge)
                    continue
                added_intermediate.add(onode.get_id())

                last_id += 1
                new_node = Node(last_id)
                last_id += 1
                new_edge = Edge(last_id, node, new_node)
                last_id += 1
                new_oedge = Edge(last_id, new_node, onode)

                new_edges.append(new_edge)
                new_node.add_edge(new_edge)
                new_node.add_edge(new_oedge)
                onode.add_edge(new_oedge)

                graph.add_node(new_node)
                graph.add_edge(new_edge)
                graph.add_edge(new_oedge)

                erase_edges.append(edge)

            for new_edge in new_edges:
                node.add_edge(new_edge)

            for erase_edge in erase_edges:
                edge_id = erase_edge.get_id()
                graph.erase_edge(edge_id)
                erase_edge.from_node.erase_edge(edge_id)
                erase_edge.to_node.erase_edge(edge_id)
            # End of intermediate nodes addition

            for edge in node.out_edges:
                onode = edge.to_node
                new_oinfo = copy.deepcopy(node.info[:-1])
                for oinfo in onode.info:
                    new_oinfo.append(oinfo)
                onode.info = new_oinfo

                last_id += 1
                new_edge = Edge(last_id, parent, onode)

                parent.add_edge(new_edge)
                onode.add_edge(new_edge)
                graph.add_edge(new_edge)
            erase_nodes.append(node)

        for erase_node in erase_nodes:
            graph.erase_node(erase_node.get_id())

        graph = collapse(graph)
        last_id = graph.find_last_id()
        if not found:
            break

    return graph


def uncollapse(input_graph: Graph):
    input_graph = compress_graph_component_id(input_graph)
    graph = Graph()
    last_id = 0
    input_size = len(input_graph.nodes) + 1
    id_nodes = {}
    for input_node in input_graph.nodes:
        id_nodes[input_node.get_id()] = []
        if len(input_node.info) == 0:
            last_id += 1
            node = Node(last_id, [])
            id_nodes[input_node.get_id()].append(node)
            graph.add_node(node)
        else:
            for input_info in input_node.info:
                last_id += 1
                node = Node(last_id, [copy.deepcopy(input_info)])
                id_nodes[input_node.get_id()].append(node)
                graph.add_node(node)

    for input_edge in input_graph.edges:
        input_from_id = input_edge.from_node.get_id()
        input_to_id = input_edge.to_node.get_id()

        from_node = id_nodes[input_from_id][-1]
        to_node = id_nodes[input_to_id][0]

        last_id += 1
        edge = Edge(last_id, from_node, to_node, copy.deepcopy(input_edge.info))

        from_node.add_edge(edge)
        if from_node.get_id != to_node.get_id:
            to_node.add_edge(edge)

        graph.add_edge(edge)

    for nodes in id_nodes.values():
        from_node = None
        for to_node in nodes:
            if from_node is not None:
                last_id += 1
                edge = Edge(last_id, from_node, to_node)

                from_node.add_edge(edge)
                if from_node.get_id != to_node.get_id:
                    to_node.add_edge(edge)

                graph.add_edge(edge)
            from_node = to_node

    return graph
