from cfg_grader.utils.dsu import DSU
from cfg_grader.utils.helpers import get_count_out


def collapse(cfg):
    count_out = get_count_out(cfg)
    dsu = DSU(len(cfg))

    # Merge nodes with the same flow
    for node in cfg:
        if len(cfg[node]) > 1:
            continue
        label = node.get_label()
        for adj_node in cfg[node]:
            if len(cfg[adj_node]) > 1:
                continue
            adj_label = adj_node.get_label()
            if adj_label not in count_out:
                continue
            if count_out[adj_label] == 1:
                print(node.get_info(), " and ", adj_node.get_info())
                dsu.merge(label, adj_label)

    # Store information from merged nodes
    add_infos = {}
    for node in cfg:
        label = node.get_label()
        par_label = dsu.find_par(label)
        if label == par_label:
            continue
        if par_label not in add_infos:
            add_infos[par_label] = []
        for info in node.get_info():
            add_infos[par_label].append(info)

    # Add information to parent node
    for node in cfg:
        label = node.get_label()
        if label in add_infos:
            for info in add_infos[label]:
                node.get_info().append(info)

    # Get new adjacency list and store label to node data
    new_adj, label_to_node = {}, {}
    for node in cfg:
        label = node.get_label()
        label_to_node[label] = node
        par_label = dsu.find_par(label)
        for adj_node in cfg[node]:
            adj_label = adj_node.get_label()
            par_adj_label = dsu.find_par(adj_label)
            if dsu.check_same(par_label, par_adj_label):
                continue
            if par_label not in new_adj:
                new_adj[par_label] = []
            new_adj[par_label].append(par_adj_label)

    # Get new CFG
    new_cfg = {}
    for node in cfg:
        label = node.get_label()
        if label == dsu.find_par(label):
            new_cfg[node] = []
            if label in new_adj:
                for adj_label in new_adj[label]:
                    new_cfg[node].append(label_to_node[adj_label])

    # Re-Enumerate Label
    for idx, node in enumerate(new_cfg):
        node.set_label(idx + 1)

    return new_cfg
