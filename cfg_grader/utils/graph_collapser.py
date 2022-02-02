from cfg_grader.utils.dsu import DSU


def collapse(g):
    dsu = DSU(len(g))

    # Merge nodes with the same flow
    for node in g:
        if len(g[node]) > 1:
            continue
        label = node.get_label()
        for adj_node in g[node]:
            if len(g[adj_node]) > 1:
                continue
            adj_label = adj_node.get_label()
            if len(adj_node.get_in_nodes()) == 1:
                dsu.merge(label, adj_label)

    # Store information from merged nodes
    add_infos = {}
    for node in g:
        label = node.get_label()
        par_label = dsu.find_par(label)
        if label == par_label:
            continue
        if par_label not in add_infos:
            add_infos[par_label] = []
        for info in node.get_info():
            add_infos[par_label].append(info)

    # Add information to parent node
    for node in g:
        label = node.get_label()
        if label in add_infos:
            for info in add_infos[label]:
                node.get_info().append(info)

    # Get new adjacency list and store label to node data
    new_adj, label_to_node = {}, {}
    for node in g:
        label = node.get_label()
        label_to_node[label] = node
        par_label = dsu.find_par(label)
        for adj_node in g[node]:
            adj_label = adj_node.get_label()
            par_adj_label = dsu.find_par(adj_label)
            if dsu.check_same(par_label, par_adj_label):
                continue
            if par_label not in new_adj:
                new_adj[par_label] = []
            new_adj[par_label].append(par_adj_label)

    # Get new graph
    new_g = {}
    for node in g:
        label = node.get_label()
        if label == dsu.find_par(label):
            new_g[node] = []
            if label in new_adj:
                for adj_label in new_adj[label]:
                    new_g[node].append(label_to_node[adj_label])

    # Re-Enumerate Label
    for idx, node in enumerate(new_g):
        node.set_label(idx + 1)

    return new_g
