"""Dinic's Max Flow Algorithm Engine.
100% Python Standard Library.
"""

import collections

class DinicMaxFlow:
    """Dinic's algorithm for maximum network flow using level graphs and blocking flow."""
    class Edge:
        def __init__(self, u, v, cap):
            self.u = u
            self.v = v
            self.cap = cap
            self.flow = 0
            self.rev = None

    def __init__(self, num_nodes):
        self.n = num_nodes
        self.adj = [[] for _ in range(num_nodes)]
        self.level = [-1] * num_nodes
        self.ptr = [0] * num_nodes

    def add_edge(self, u, v, cap):
        e1 = self.Edge(u, v, cap)
        e2 = self.Edge(v, u, 0)
        e1.rev = e2
        e2.rev = e1
        self.adj[u].append(e1)
        self.adj[v].append(e2)

    def _bfs(self, s, t):
        self.level = [-1] * self.n
        self.level[s] = 0
        queue = collections.deque([s])
        while queue:
            u = queue.popleft()
            for edge in self.adj[u]:
                if edge.cap - edge.flow > 0 and self.level[edge.v] == -1:
                    self.level[edge.v] = self.level[u] + 1
                    queue.append(edge.v)
        return self.level[t] != -1

    def _dfs(self, u, t, pushed):
        if pushed == 0 or u == t:
            return pushed
        for cid in range(self.ptr[u], len(self.adj[u])):
            self.ptr[u] = cid
            edge = self.adj[u][cid]
            tr = edge.v
            if self.level[u] + 1 != self.level[tr] or edge.cap - edge.flow == 0:
                continue
            tr_pushed = self._dfs(tr, t, min(pushed, edge.cap - edge.flow))
            if tr_pushed == 0:
                continue
            edge.flow += tr_pushed
            edge.rev.flow -= tr_pushed
            return tr_pushed
        return 0

    def compute_max_flow(self, s, t):
        flow = 0
        while self._bfs(s, t):
            self.ptr = [0] * self.n
            while True:
                pushed = self._dfs(s, t, float("inf"))
                if pushed == 0:
                    break
                flow += pushed
        return flow
