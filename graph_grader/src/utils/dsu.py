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
