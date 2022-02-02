def get_count_out(cfg):
    count_out = {}
    for node in cfg:
        for adj_node in cfg[node]:
            label = adj_node.get_label()
            if label not in count_out:
                count_out[label] = 1
            else:
                count_out[label] += 1
    return count_out