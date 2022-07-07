import astor
from staticfg import CFGBuilder, CFG, Block

from grader.src.ged.classes.graph import Graph
from grader.src.ged.classes.graph_component import Node, Edge


class PythonCfgGenerator:
    def __init__(self):
        self.cfg_builder = CFGBuilder()

    def __get_statement_type_string(self, statement):
        ret = type(statement).__name__.lower()
        if ret == "for" or ret == "while":
            ret = "for/while"
        return ret

    def __block_to_node(self, block: Block):
        info = []
        for statement in block.statements:
            current = {
                "rawLine": (astor.to_source(statement)).split('\n')[0],
                "label": self.__get_statement_type_string(statement)
            }
            info.append(current)
        node = Node(block.id, info)
        return node

    def __compress_blocks_id(self, cfg: CFG, start=1):
        for block in cfg:
            block.id = start
            start += 1
        return cfg

    def __cfg_to_graph(self, cfg: CFG):
        self.__compress_blocks_id(cfg)

        graph = Graph()
        last_id = 0
        id_node = {}
        for block in cfg:
            node = self.__block_to_node(block)
            id_node[node.get_id()] = node
            last_id = max(last_id, node.get_id())
            graph.add_node(node)

        for block in cfg:
            for out_edge in block.exits:
                from_node = id_node[out_edge.source.id]  # graph.find_node_with_id(out_edge.source.id)
                to_node = id_node[out_edge.target.id]  # graph.find_node_with_id(out_edge.target.id)

                last_id += 1
                edge = Edge(last_id, from_node, to_node)

                from_node.add_edge(edge)
                if from_node.get_id() != to_node.get_id():
                    to_node.add_edge(edge)

                graph.add_edge(edge)

        # Add an exit for 'if' blocks with only one exit
        new_nodes = []
        for node in graph.nodes:
            if len(node.info) > 0 and node.info[-1]['label'].lower() == 'if' and len(node.out_edges) == 1:
                last_id += 1
                new_node = Node(last_id)
                last_id += 1
                new_edge = Edge(last_id, node, new_node)

                node.add_edge(new_edge)
                new_node.add_edge(new_edge)
                new_nodes.append(new_node)
                graph.add_edge(new_edge)

        for new_node in new_nodes:
            graph.add_node(new_node)

        return graph

    def draw_python_from_file(self, filename, img_filename):
        cfg = self.cfg_builder.build_from_file("", filename)
        cfg = self.__compress_blocks_id(cfg)
        cfg.build_visual(img_filename, "jpg")

    def generate_python(self, raw_code) -> Graph:
        cfg = self.cfg_builder.build_from_src("", raw_code)
        return self.__cfg_to_graph(cfg)

    def generate_python_from_file(self, filename) -> Graph:
        with open(filename, 'r', encoding='UTF-8') as file:
            raw_code = file.read()
            return self.generate_python(raw_code)
