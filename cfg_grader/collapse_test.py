from pycfg.pycfg import PyCFG, CFGNode, slurp
from pycfg_ex import generate_cfg

def collapse(graph):
    new_graph = graph
    nodes = graph.nodes()
    to_be_removed = []
    for i in range(len(nodes)):
        curr_out_edges = graph.out_edges(nodes[i])
        if(len(curr_out_edges) == 1 and nodes[i] not in to_be_removed):
            start_node = nodes[i]
            curr_node = nodes[i]
            (_, next_node) = curr_out_edges[0]
            node = graph.get_node(start_node)
            label = node.attr['label']
            stop = False
            while(not stop):
                if(len(graph.out_edges(next_node)) == 1 and len(graph.in_edges(next_node)) == 1):
                    curr_node = next_node
                    to_be_removed.append(curr_node)
                    node = graph.get_node(curr_node)
                    label += '\n' + node.attr['label']
                    (_, next_node) = graph.out_edges(curr_node)[0]
                elif(len(graph.out_edges(next_node)) != 1 and len(graph.in_edges(next_node)) == 1):
                    stop_node = next_node
                    to_be_removed.append(next_node)
                    node = graph.get_node(next_node)
                    label += '\n' + node.attr['label']
                    stop = True
                else:
                    stop_node = curr_node
                    # node = graph.get_node(curr_node)
                    # label += '\n' + node.attr['label']
                    # if(start_node != stop_node):
                    #     to_be_removed.append(stop_node)

                    stop = True

            if(start_node != stop_node):
                if(len(graph.out_edges(stop_node)) > 0):
                    edges = graph.out_edges(stop_node)
                    for edge in edges:
                        (_, end_node) = edge
                        new_graph.add_edge(start_node, end_node)
                node = new_graph.get_node(start_node)
                node.attr['label'] = label
                
    if(len(to_be_removed) > 0):
        removed_edges = []
        [removed_edges.append(x) for x in new_graph.edges(to_be_removed) if x not in removed_edges]
        # print(to_be_removed)
        # removed_edges = new_graph.edges(to_be_removed)
        # print(removed_edges)
        # print(new_graph.edges())
        new_graph.remove_edges_from(removed_edges)
        new_graph.remove_nodes_from(to_be_removed)

    return new_graph

# filename = "example3.py"
# g1 = generate_cfg(filename)
# print(g1)
# g1.draw('old.png', prog ='dot')
# g2 = collapse(g1)
# print(g2)
# g2.draw('new.png', prog = 'dot')