from graph_grader.src.utils.dsu import DSU
from intermediate.src.classes.graph import Graph


def collapse(g: Graph):
    nodes = g.get_nodes()
    dsu = DSU(len(nodes))

    # Merge nodes with the same flow
    for node in nodes:
        adjacent = node.get_adjacent()
        if len(adjacent) > 1:
            continue
        label = node.get_label()
        for adj_node in adjacent:
            if len(adj_node.get_adjacent()) > 1:
                continue
            adj_label = adj_node.get_label()
            if len(adj_node.get_in_nodes()) <= 1:
                dsu.merge(label, adj_label)

    # Store information from merged nodes
    add_infos = {}
    for node in nodes:
        label = node.get_label()
        par_label = dsu.find_par(label)
        if label == par_label:
            continue
        if par_label not in add_infos:
            add_infos[par_label] = []
        for info in node.get_info():
            add_infos[par_label].append(info)

    # Add information to parent node
    for node in nodes:
        label = node.get_label()
        if label in add_infos:
            for info in add_infos[label]:
                node.add_info(info)

    # Get new adjacency list
    new_adj = {}
    for node in nodes:
        label = node.get_label()
        par_label = dsu.find_par(label)
        for adj_node in node.get_adjacent():
            adj_label = adj_node.get_label()
            par_adj_label = dsu.find_par(adj_label)
            if dsu.check_same(par_label, par_adj_label):
                continue
            if par_label not in new_adj:
                new_adj[par_label] = []
            new_adj[par_label].append(par_adj_label)

    # Reset adjacent and in nodes list for every node
    for node in nodes:
        node.set_adjacent([])
        node.set_in_nodes([])

    # Get new nodes and add new adjacent for every node
    new_nodes = []
    for node in nodes:
        label = node.get_label()
        par_label = dsu.find_par(label)
        if label != par_label:
            continue
        new_nodes.append(node)
        if par_label in new_adj:
            for adj_label in new_adj[par_label]:
                node.add_adjacent(g.get_node(adj_label))

    # Relabel Node
    for idx, node in enumerate(new_nodes):
        node.set_label(idx + 1)

    # Set new node to graph
    g.set_nodes(new_nodes)
