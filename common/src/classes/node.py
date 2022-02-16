class Node:
    def __init__(self, label: int, info=None):
        self.info: list[str] = []
        self.adjacent: list[Node] = []
        self.in_nodes: list[Node] = []
        self.label: int = label
        if info and len(info) > 0:
            self.info = info

    def add_in_nodes(self, node):
        if node not in self.in_nodes:
            self.in_nodes.append(node)

    def add_info(self, information: str):
        self.info.append(information)

    def add_adjacent(self, node):
        if node not in self.adjacent:
            self.adjacent.append(node)
            node.add_in_nodes(self)

    def print_info(self):
        for info in self.info:
            print(info)

    def get_label(self):
        return self.label

    def get_info(self):
        return self.info

    def get_info_str(self):
        str_info = ''
        for info in self.get_info():
            if str_info == '':
                str_info += info
            else:
                str_info += f'\n{info}'
        return str_info

    def get_in_nodes(self):
        return self.in_nodes

    def get_adjacent(self):
        return self.adjacent

    def set_label(self, label: int):
        self.label = label

    def set_adjacent(self, adjacent: list):
        self.adjacent = adjacent

    def set_in_nodes(self, in_nodes: list):
        self.in_nodes = in_nodes

    def traverse(self, is_visited: dict[int, bool], graph: dict):
        is_visited[self.label] = True
        if self not in graph:
            graph[self] = self.adjacent
        for adj in self.adjacent:
            if not is_visited[adj.get_label()]:
                adj.traverse(is_visited, graph)
