class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def find(self, x):
        while self.parents[x] >= 0:
            x = self.parents[x]
        return x

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def size(self, x):
        return -self.parents[self.find(x)]

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self):
        return len(self.roots())

    def all_group_members(self):
        self.group = {r:[] for r in self.roots()}
        for i in range(self.n):
            self.group[self.find(i)].append(i)
        return self.group

    def __str__(self):
        return '\n'.join('{}: {}'.format(r, self.all_group_members()[r]) for r in self.roots())

#URL
#https://note.nkmk.me/python-union-find/

uf = UnionFind(6)
print(uf.parents)
# [-1, -1, -1, -1, -1, -1]

print(uf)
# 0: [0]
# 1: [1]
# 2: [2]
# 3: [3]
# 4: [4]
# 5: [5]

uf.union(0, 2)
print(uf.parents)
# [-2, -1, 0, -1, -1, -1]

print(uf)
# 0: [0, 2]
# 1: [1]
# 3: [3]
# 4: [4]
# 5: [5]

print(uf.group_count())
# 5

print(uf.roots())
# [0, 1, 3, 4, 5]

print(uf.size(0))
# 2

print(uf.all_group_members())
# {0: [0, 2], 1: [1], 3: [3], 4: [4], 5: [5]}





# 部分永続Union-Find (partially persistent union-find)
# O(logN)

# N: 頂点数
# p[u]: 頂点uの親頂点
# sz[u]: 現在の親頂点uの木が含む頂点数
# H[u]: 現在の親頂点uの木の高さ
# S[u] = [(t, s), ...]:
#     時刻tに別の頂点をマージした親頂点uの木が含む頂点数s
# T[u]: 頂点uが親頂点でなくなる時刻

from bisect import bisect
INF = 1e18
class PP_UnionFind():
    def __init__(self, N):
        self.N = N
        *self.p, = range(self.N)
        self.sz = [1]*self.N
        self.H = [1]*self.N
        self.S = [[(0, 1)] for i in range(self.N)]
        self.T = [INF]*self.N

    def find(self, x, t):
        while self.T[x] <= t:
            x = self.p[x]
        return x

    def union(self, x, y, t):
        px = self.find(x, t)
        py = self.find(y, t)
        if px == py:
            return 0
        if self.H[py] < self.H[px]:
            self.p[py] = px
            self.T[py] = t
            self.sz[px] += self.sz[py]
            self.S[px].append((t, self.sz[px]))
        else:
            self.p[px] = py
            self.T[px] = t
            self.sz[py] += self.sz[px]
            self.S[py].append((t, self.sz[py]))
            self.H[py] = max(self.H[py], self.H[px]+1)
        return 1

    def size(self, x, t):
        y = self.find(x, t)
        idx = bisect(self.S[y], (t, INF))-1
        print(self.S)
        return self.S[y][idx][1]





# 重み付きUnionfind
# O(logN)

# union(x, y, w):weight(y) = weight(x) + w となるように x と y をマージする
# same(x, y):x と y が同じグループにいるかどうかを判定する
# dist(x, y):x と y とが同じグループにいるとき、weight(y) - weight(x) をリターンする

class W_UnionFind:
    def __init__(self, n):
        self.p=[i for i in range(n)]
        self.r=[0 for i in range(n)]
        self.d=[0 for i in range(n)]

    def root(self,x):
        if self.p[x]==x:
            return x
        else:
            tmp = self.root(self.p[x])
            self.d[x] += self.d[self.p[x]]
            self.p[x] = tmp
            return self.p[x]
    
    def weight(self,x):
        self.root(x)
        return self.d[x]

    def dist(self,x,y):
        if self.root(x)==self.root(y):
            return self.weight(y)-self.weight(x)
        else:
            return '?'

    def union(self,x,y,w):
        w+=self.weight(x)
        w-=self.weight(y)
        x=self.root(x)
        y=self.root(y)
        if(x==y):
            return
        if self.r[x]<self.r[y]:
            self.p[x]=y
            self.d[x]=-w
        else:
            self.p[y]=x
            self.d[y]=w
            if self.r[x]==self.r[y]:
                self.r[x]+=1
    
    def same(self,x,y):
        return self.root(x)==self.root(y)