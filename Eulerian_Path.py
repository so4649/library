# オイラーツアー
# N:頂点数、M:辺の数、E:辺の集合
# O(|E|)

# https://neterukun1993.github.io/Library/Graph/Tree/EulerTour.py
class EulerTour:
    def __init__(self, tree, root=None):
        self.n = len(tree)
        self.tree = tree
        self.par = [-1] * self.n
        self.begin = [-1] * self.n
        self.end = [-1] * self.n
        self.walk_order = []

        if root is None:
            for v in range(self.n):
                if self.par[v] == -1:
                    self._traversal(v)
        else:
            self._traversal(root)

    def _traversal(self, rt):
        stack = [rt, 0]
        self.begin[rt] = len(self.walk_order)
        self.walk_order.append(rt)
        while stack:
            v, idx = stack[-2:]
            if idx < len(self.tree[v]):
                nxt_v = self.tree[v][idx]
                stack[-1] += 1
                if nxt_v == self.par[v]:
                    continue
                self.begin[nxt_v] = len(self.walk_order)
                self.walk_order.append(nxt_v)
                self.par[nxt_v] = v
                stack.append(nxt_v)
                stack.append(0)
            else:
                self.end[v] = len(self.walk_order) 
                if self.par[v] != -1:
                    self.walk_order.append(self.par[v])
                stack.pop()
                stack.pop()

    def build_lca(self):
        self.depth = self.walk_order[:]
        d = 0
        for i, (prv_v, v) in enumerate(zip(self.walk_order, self.walk_order[1:])):
            if self.par[v] == -1: d = 0
            elif self.par[v] == prv_v: d += 1
            else: d -= 1
            self.depth[i + 1] = (d << 32) + v
        self._build_rmq()

    def _build_rmq(self):
        size = len(self.depth)
        lg_size = size.bit_length()
        self.lg = [0] * (size + 1)
        for i in range(2, size + 1):
            self.lg[i] = self.lg[i // 2] + 1

        self.tbl = [[0] * size for _ in range(lg_size)]
        tbl = self.tbl
        for i, val in enumerate(self.depth):
            tbl[0][i] = val
        for k in range(lg_size - 1):
            for i in range(size - (1 << k + 1) + 1):
                tbl[k + 1][i] = min(tbl[k][i], tbl[k][i + (1 << k)])

    def _min_query(self, l, r):
        k = self.lg[r - l]
        return min(self.tbl[k][l], self.tbl[k][r - (1 << k)])                

    def lca(self, u, v):
        if self.begin[u] > self.begin[v]:
            u, v = v, u
        l, r = self.begin[u], self.begin[v] + 1
        lca_uv = self._min_query(l, r) & ((1 << 32) - 1)
        return lca_uv






# オイラーツアーの経路復元

import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

def Eulerian_Path(N, M, E):
    G = [[] for i in range(N)]
    deg = [0]*N
    rdeg = [0]*N
    for a, b in E:
        deg[a] += 1
        rdeg[b] += 1
        G[a].append(b)

    # find starting and ending vertices
    s = t = u = -1
    for i in range(N):
        if deg[i] == rdeg[i] == 0:
            continue
        df = deg[i] - rdeg[i]
        if not -1 <= df <= 1:
            return None
        if df == 1:
            if s != -1:
                return None
            s = i
        elif df == -1:
            if t != -1:
                return None
            t = i
        else:
            u = i
    v0 = (s if s != -1 else u)

    # find an Eulerian path (or circuit)
    res = []
    it = [0]*N
    st = [v0]
    *it, = map(iter, G)
    while st:
        v = st[-1]
        w = next(it[v], -1)
        if w == -1:
            res.append(v)
            st.pop()
            continue
        st.append(w)
    res.reverse()
    if len(res) != M+1:
        return None
    return res


# E = [
#   (2, 0), (0, 3), (0, 1), (3, 2), (1, 2),
# ]
# print(Eulerian Path(4, 5, E))
# # => "[0, 3, 2, 0, 1, 2]"

n = int(input())
E = []
for i in range(n-1):
    a,b = map(lambda x:int(x)-1,input().split())
    E.append((a,b))
    E.append((b,a))

print(Eulerian_Path(n,2*n-2,E))