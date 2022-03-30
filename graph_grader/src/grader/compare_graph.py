from munkres import Munkres

from intermediate.src.classes.constants import Constants
from graph_grader.src.grader.cost_matrix import create_cost_matrix
from intermediate.src.classes.graph import Graph


def compare_graph(g1: Graph, g2: Graph):
    munkres = Munkres()
    cost_matrix = create_cost_matrix(g1, g2)
    indexes = munkres.compute(cost_matrix)

    total = 0
    details = []
    for i, j in indexes:
        val = cost_matrix[i][j]
        total += val
        details.append([i, j, val])

    node1 = len(g1.get_nodes())
    node2 = len(g2.get_nodes())
    edge1 = len(g1.get_edges())
    edge2 = len(g2.get_edges())
    score = (1 - (total / (node1 + node2 + edge1 + edge2))) * Constants.MAX_SCORE

    return score, total, details
