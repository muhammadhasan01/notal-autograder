from cfg_grader.src.grader.compare_graph import compare_graph
from cfg_grader.src.utils.graph_collapser import collapse
from intermediate.src.classes.graph import Graph
from notal_to_cfg_generator.src.api.functions import get_cfg


def notal_grader(src_refs: list[str], src: str):
    if len(src_refs) == 0:
        raise ValueError("src_refs need to have at least one element")
    ret_score, ret_total, ret_details = 0.0, 0, [[]]
    graph_src = Graph()
    graph_src.build_from_cfg_graph(get_cfg(None, src))
    collapse(graph_src)
    for src_ref in src_refs:
        graph_src_answer = Graph()
        graph_src_answer.build_from_cfg_graph(get_cfg(None, src_ref))
        collapse(graph_src_answer)
        score, total, details = compare_graph(graph_src_answer, graph_src)
        if score > ret_score:
            ret_score, ret_total, ret_details = score, total, details

    return ret_score, ret_total, ret_details
