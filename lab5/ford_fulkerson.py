from collections import deque
from math import inf

import igraph as ig

from lab5.random_flow_network import RandomFlowNetwork, draw_flow_network


class ResidualNetwork:
    def __init__(self, G: ig.Graph):
        self.G = G
        self.us = [e.source for e in G.es]
        self.vs = [e.target for e in G.es]
        self.c = list(G.es["weight"])
        self.f = [0] * G.ecount()
        self.out_edges = G.get_inclist(mode="out")
        self.in_edges = G.get_inclist(mode="in")

    def cf(self, edge_id: int, forward: bool) -> int:
        if forward:
            return self.c[edge_id] - self.f[edge_id]
        return self.f[edge_id]

    def neighbors(self, v: int) -> list[tuple[int, int, bool]]:
        neighbors = []
        for edge_id in self.out_edges[v]:
            if self.cf(edge_id, forward=True) > 0:
                neighbors.append((self.vs[edge_id], edge_id, True))

        for edge_id in self.in_edges[v]:
            if self.cf(edge_id, forward=False) > 0:
                neighbors.append((self.us[edge_id], edge_id, False))

        return neighbors

    def save_flow(self):
        self.G.es["flow"] = self.f


def init(Gf: ResidualNetwork, s: int) -> tuple[list, list]:
    n = Gf.G.vcount()
    ds = [inf] * n
    ps = [None] * n
    ds[s] = 0
    return ds, ps


def bfs(Gf: ResidualNetwork, s: int, t: int) -> list[tuple[int, bool]] | None:
    ds, ps = init(Gf, s)
    Q = deque([s])

    while Q:
        v = Q.popleft()
        for u, edge_id, forward in Gf.neighbors(v):
            if ds[u] == inf:
                ds[u] = ds[v] + 1
                ps[u] = (v, edge_id, forward)
                if u == t:
                    return get_path(ps, s, t)
                Q.append(u)

    return None


def get_path(ps: list, s: int, t: int) -> list[tuple[int, bool]]:
    p = []
    v = t
    while v != s:
        previous, edge_id, forward = ps[v]
        p.append((edge_id, forward))
        v = previous
    p.reverse()
    return p


class FordFulkerson:
    def __init__(self, G: ig.Graph, s: int, t: int):
        self.G = G
        self.s = s
        self.t = t
        self.max_flow = 0

    def run(self) -> ig.Graph:
        Gf = ResidualNetwork(self.G)
        self.max_flow = 0

        while (p := bfs(Gf, self.s, self.t)) is not None:
            cf_p = min(Gf.cf(edge_id, forward) for edge_id, forward in p)
            for edge_id, forward in p:
                if forward:
                    Gf.f[edge_id] += cf_p
                else:
                    Gf.f[edge_id] -= cf_p
            self.max_flow += cf_p

        Gf.save_flow()
        return self.G


if __name__ == "__main__":
    rfn = RandomFlowNetwork(3)
    G = rfn.run()
    draw_flow_network(G).save("RandomFlowNetwork.png")
    ff = FordFulkerson(G, rfn.s, rfn.t)
    G = ff.run()
    print(f"Maksymalny przepływ: {ff.max_flow}")
    G.es["label"] = [f"{e['flow']}/{e['weight']}" for e in G.es]
    draw_flow_network(G).save("FordFulkerson.png")
