def get_count_out(g):
    count_out = {}
    for node in g:
        for adj_node in g[node]:
            label = adj_node.get_label()
            if label not in count_out:
                count_out[label] = 1
            else:
                count_out[label] += 1
    return count_out


def get_count_edges(g):
    ret = 0
    for u in g:
        ret += len(u.get_adjacent())
    return ret
