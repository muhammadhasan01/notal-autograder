from common.classes.node import *


class CFG:
    def __init__(self, entry_block: Node, exit_block: list[Node]):
        # entry_block -> Node, exit_block -> [Node], entry_block -> exit_block must be connected
        self.entry_block = entry_block
        self.exit_block: list[Node] = exit_block

    def get_entry_block(self):
        return self.entry_block

    def get_exit_block(self):
        return self.exit_block

    def add_exit_block(self, node):
        self.exit_block.append(node)

    def merge_cfg(self, cfg):
        entry_block_next_cfg = cfg.get_entry_block()
        for exit_block in self.exit_block:
            exit_block.add_adjacent(entry_block_next_cfg)
        self.exit_block = cfg.get_exit_block()

    def get_graph(self, num_node):
        is_visited = [False for _ in range(0, num_node + 3)]
        graph = {}
        self.entry_block.traverse(is_visited, graph)

        start_node = Node(label=num_node, info=['start: main'])
        end_node = Node(label=num_node + 1, info=['end: main'])

        start_node.add_adjacent(self.entry_block)
        graph[start_node] = [self.entry_block]
        graph[end_node] = []
        for exit_node in self.exit_block:
            graph[exit_node].append(end_node)
            end_node.add_in_nodes(exit_node)

        return graph
