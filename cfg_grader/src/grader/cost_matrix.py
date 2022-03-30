from intermediate.src.classes.constants import Constants
from intermediate.src.classes.graph import Graph


def get_cost_real(a: int, b: int):
    return a + b - (2 * min(a, b))


def create_cost_matrix(g1: Graph, g2: Graph):
    # Get number of nodes
    nodes1, nodes2 = g1.get_nodes(), g2.get_nodes()
    n, m = len(nodes1), len(nodes2)

    # Initialize cost matrix
    cost_matrix = [[0 for _ in range(n + m)] for _ in range(n + m)]

    # Fill section 1 (real node to real node)
    for i, u in enumerate(nodes1):
        for j, v in enumerate(nodes2):
            inp1 = len(u.get_in_nodes())
            inp2 = len(v.get_in_nodes())
            out1 = len(u.get_adjacent())
            out2 = len(v.get_adjacent())
            cost_matrix[i][j] = get_cost_real(inp1, inp2) + get_cost_real(out1, out2)

    # Fill section 2 (delete node in graph 1)
    for i, u in enumerate(nodes1):
        for j in range(n):
            if i == j:
                ie = len(u.get_in_nodes())
                oe = len(u.get_adjacent())
                cost_matrix[i][j + m] = 1 + ie + oe
            else:
                cost_matrix[i][j + m] = Constants.INF

    # Fill Section 3 (delete node in graph 2)
    for i, u in enumerate(nodes2):
        for j in range(m):
            if i == j:
                ie = len(u.get_in_nodes())
                oe = len(u.get_adjacent())
                cost_matrix[i + n][j] = 1 + ie + oe
            else:
                cost_matrix[i + n][j] = Constants.INF

    return cost_matrix
