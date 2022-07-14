from grader.src.ged.classes.graph_component import *
import math


class Constants:
    INF = math.inf
    MAX_SCORE = 100

    FIRST_UB = []

    EDGE_EPS = Edge(-1)
    NODE_EPS = Node(-1)

    node_cost_matrix: list[list] = None
    edge_cost_matrix: list[list] = None
