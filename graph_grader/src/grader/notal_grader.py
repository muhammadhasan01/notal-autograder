from graph_grader.src.grader.compare_graph import compare_graph
from graph_grader.src.utils.graph_collapser import collapse
from intermediate.src.classes.graph import Graph
from cfg_generator.src.api.functions import get_cfg


def notal_grader(src_refs: list[str], src: str):
    if len(src_refs) == 0:
        raise ValueError("src_refs need to have at least one element")
    ret_score = 0.0
    graph_src = Graph()
    try:
        cfg_src = get_cfg(None, src)
    except Exception as e:
        raise SyntaxError(f"solution submission got a syntax error='{e}'")
    graph_src.build_from_cfg_graph(cfg_src)
    collapse(graph_src)
    for idx, src_answer in enumerate(src_refs):
        graph_src_answer = Graph()
        try:
            cfg_answer = get_cfg(None, src_answer)
        except Exception as e:
            raise SyntaxError(f"reference submission-{idx + 1} got a syntax error='{e}'")
        graph_src_answer.build_from_cfg_graph(cfg_answer)
        collapse(graph_src_answer)
        score = compare_graph(graph_src_answer, graph_src)
        if score > ret_score:
            ret_score = score

    return ret_score
