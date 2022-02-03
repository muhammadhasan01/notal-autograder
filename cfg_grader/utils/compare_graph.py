from munkres import Munkres

from common.classes.constants import Constants
from cfg_grader.utils.cost_matrix import create_cost_matrix
from cfg_grader.utils.helpers import get_count_edges


def compare(g1, g2):
    munkres = Munkres()
    cost_matrix = create_cost_matrix(g1, g2)
    indexes = munkres.compute(cost_matrix)

    total = 0
    details = []
    for i, j in indexes:
        val = cost_matrix[i][j]
        total += val
        details.append([i, j, val])

    node1 = len(g1)
    node2 = len(g2)
    edge1 = get_count_edges(g1)
    edge2 = get_count_edges(g2)
    score = (1 - (total / (node1 + node2 + edge1 + edge2))) * Constants.MAX_SCORE

    return score, total, details
