from collections import deque

n = int(input())
edge = [[] for i in range(n)]
for i in range(n-1):
    x, y = map(int, input().split())
    edge[x-1].append(y-1)
    edge[y-1].append(x-1)
 
parent = [-1] * n
q = deque([0])
while q:
    i = q.popleft()
    for a in edge[i]:
        if a != parent[i]:
            parent[a] = i
            q.append(a)
print(parent)


# 最小共通祖先（ダブリング）
# ABC14D

from collections import deque

def bfs(N,edge,start=0):
    dist = [-1]*N
    que = deque([start])
    dist[start] = 0
    prv = [-1]*N
    while que:
        v = que.popleft()
        d = dist[v]
        for w in edge[v]:
            if dist[w] > -1:
                continue
            dist[w] = d + 1
            prv[w] = v
            que.append(w)
    return dist,prv

import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

n = int(input())
edge = [[] for i in range(n)]
for i in range(n-1):
    x,y = map(lambda x:int(x)-1,input().split())
    edge[x].append(y)
    edge[y].append(x)

LV = (n-1).bit_length()
def construct(prv):
    kprv = [prv]
    S = prv
    for k in range(LV):
        T = [-1]*n
        for i in range(n):
            if S[i] == -1:
                continue
            T[i] = S[S[i]]
        kprv.append(T)
        S = T
    return kprv

def lca(u, v, kprv, depth):
    dd = depth[v] - depth[u]
    if dd < 0:
        u, v = v, u
        dd = -dd

    # assert depth[u] <= depth[v]
    for k in range(LV+1):
        if dd & 1:
            v = kprv[k][v]
        dd >>= 1

    # assert depth[u] == depth[v]
    if u == v:
        return u

    for k in range(LV-1, -1, -1):
        pu = kprv[k][u]; pv = kprv[k][v]
        if pu != pv:
            u = pu; v = pv

    # assert kprv[0][u] == kprv[0][v]
    return kprv[0][u]

depth,prv = bfs(n,edge,0)
kprv = construct(prv)

q = int(input())
for i in range(q):
    a,b = map(lambda x:int(x)-1,input().split())
    u = lca(a,b,kprv,depth)
    ans = depth[a]+depth[b]-depth[u]*2+1
    print(ans)



# HL分解
# https://neterukun1993.github.io/Library/Graph/Tree/HLDecomposition.py

class HLDecomposition:
    def __init__(self, tree):
        self.tree = tree
        self.n = len(tree)
        self.par = [-1] * self.n
        self.size = [1] * self.n
        self.depth = [0] * self.n
        self.preorder = [0] * self.n
        self.head = [i for i in range(self.n)]
        self.k = 0

        for v in range(self.n):
            if self.par[v] == -1:
                self._dfs_pre(v)
                self._dfs_hld(v)

    def getitem(self, v):
        return self.preorder[v]

    def _dfs_pre(self, v):
        tree = self.tree
        stack = [v]
        order = [v]
        while stack:
            v = stack.pop()
            for chi_v in tree[v]:
                if chi_v == self.par[v]:
                    continue
                self.par[chi_v] = v
                self.depth[chi_v] = self.depth[v] + 1
                stack.append(chi_v)
                order.append(chi_v)

        for v in reversed(order):
            tree_v = tree[v]
            if len(tree_v) and tree_v[0] == self.par[v]:
                tree_v[0], tree_v[-1] = tree_v[-1], tree_v[0]
            for idx, chi_v in enumerate(tree_v):
                if chi_v == self.par[v]:
                    continue
                self.size[v] += self.size[chi_v]
                if self.size[chi_v] > self.size[tree_v[0]]:
                    tree_v[idx], tree_v[0] = tree_v[0], tree_v[idx]

    def _dfs_hld(self, v):
        stack = [v]
        while stack:
            v = stack.pop()
            self.preorder[v] = self.k
            self.k += 1
            if len(self.tree[v]) == 0:
                continue
            top = self.tree[v][0]
            for chi_v in reversed(self.tree[v]):
                if chi_v == self.par[v]:
                    continue
                if chi_v == top:
                    self.head[chi_v] = self.head[v]
                else:
                    self.head[chi_v] = chi_v
                stack.append(chi_v)

    def lca(self, u, v):
        while u != -1 and v != -1:
            if self.preorder[u] > self.preorder[v]:
                u, v = v, u
            if self.head[u] == self.head[v]:
                return u
            v = self.par[self.head[v]]
        return -1

    def distance(self, u, v):
        lca_uv = self.lca(u, v)
        if lca_uv == -1:
            return -1
        else:
            return self.depth[u] + self.depth[v] - 2 * self.depth[lca_uv]

    def range_vertex_path(self, u, v):
        while True:
            if self.preorder[u] > self.preorder[v]:
                u, v = v, u
            l = max(self.preorder[self.head[v]], self.preorder[u])
            r = self.preorder[v]
            yield l, r + 1
            if self.head[u] != self.head[v]:
                v = self.par[self.head[v]]
            else:
                return

    def range_edge_path(self, u, v):
        while True:
            if self.preorder[u] > self.preorder[v]:
                u, v = v, u
            if self.head[u] != self.head[v]:
                yield self.preorder[self.head[v]], self.preorder[v] + 1
                v = self.par[self.head[v]]
            else:
                if u != v:
                    yield self.preorder[u] + 1, self.preorder[v] + 1
                break

    def range_subtree(self, u):
        return self.preorder[u], self.preorder[u] + self.size[u]

# ABC202E
n = int(input())
p = [-1]+list(map(lambda x:int(x)-1,input().split()))

edge = [[] for i in range(n)]
for i in range(1,n):
    edge[i].append(p[i])
    edge[p[i]].append(i)

hl = HLDecomposition(edge)

q = int(input())

query = [[] for i in range(n)]
for i in range(q):
    u,d = map(int,input().split())
    u -= 1
    query[d].append((u,i))

for i in range(n):
    query[i].sort(key=lambda x:hl.__getitem__(x[0]))

depth = hl.depth
dist_v = [[] for i in range(n)]
for i in range(n):
    dist_v[depth[i]].append(i)

ans = [0]*q
bit = BIT(n)

# 距離ごと
for i in range(n):
    for j in dist_v[i]:
        bit.add(hl.__getitem__(j),1)

    for u,idx in query[i]:
        l,r = tuple(hl.range_subtree(u))
        ans[idx] = bit.get(l,r)

    for j in dist_v[i]:
        bit.add(hl.__getitem__(j),-1)

print(*ans)