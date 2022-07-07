import copy

from grader.src.ged.classes.graph_component import Node


class DSU:
    def __init__(self, N: int):
        self.par = [i for i in range(N + 1)]

    def find_par(self, u: int):
        if self.par[u] == u:
            return u
        p = self.find_par(self.par[u])
        self.par[u] = p
        return p

    def merge(self, u: int, v: int):
        pu, pv = self.find_par(u), self.find_par(v)
        self.par[pv] = pu

    def check_same(self, u: int, v: int):
        pu, pv = self.find_par(u), self.find_par(v)
        return pu == pv


class CollapserDSU:
    def __init__(self, nodes: list[Node]):
        N = len(nodes)
        self.par = [i for i in range(N + 1)]
        self.info = [[] for i in range(N + 1)]
        for node in nodes:
            self.info[node.get_id()] = copy.deepcopy(node.info)

    def find_par(self, u: int):
        if self.par[u] == u:
            return u
        p = self.find_par(self.par[u])
        self.par[u] = p
        return p

    # has to be in order (u is predecessor of v)
    def merge(self, u: int, v: int):
        pu, pv = self.find_par(u), self.find_par(v)
        self.par[pv] = pu
        self.info[pu].extend(self.info[pv])

    def check_same(self, u: int, v: int):
        pu, pv = self.find_par(u), self.find_par(v)
        return pu == pv
