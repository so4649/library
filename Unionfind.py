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
# 最新の時刻の結合を加えていき過去の状態も見れるunionfind

# https://neterukun1993.github.io/Library/DataStructure/UnionFind/PartiallyPersistentUnionFind.py

from bisect import bisect_left

class PartiallyPersistentUnionFind:
    def __init__(self, n):
        self.INF = 10 ** 9
        self.parent = [-1] * n
        self.time = [self.INF] * n
        self.size = [[(-1, -1)] for i in range(n)]

    def find(self, t, x):
        while self.time[x] <= t:
            x = self.parent[x]
        return x

    def merge(self, t, x, y):
        x = self.find(t, x)
        y = self.find(t, y)
        if x == y:
            return False
        if self.parent[x] > self.parent[y]:
            x, y = y, x
        self.parent[x] += self.parent[y]
        self.size[x].append((t, self.parent[x]))
        self.parent[y] = x
        self.time[y] = t
        return True

    def same(self, t, x, y):
        return self.find(t, x) == self.find(t, y)

    def size(self, t, x):
        x = self.find(t, x)
        idx = bisect_left(self.size[x], (t, self.INF)) - 1
        return -self.size[x][idx][1]



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



# 巻き戻し可能Union Find
# https://neterukun1993.github.io/Library/DataStructure/UnionFind/UnionFindUndo.py

class UnionFindUndo:
    def __init__(self, n):
        self.parent = [-1] * n
        self.history = []

    def root(self, x):
        if self.parent[x] < 0:
            return x
        else:
            return self.root(self.parent[x])

    def merge(self, x, y):
        x = self.root(x)
        y = self.root(y)
        self.history.append((x, self.parent[x]))
        self.history.append((y, self.parent[y]))
        if x == y:
            return False
        if self.parent[x] > self.parent[y]:
            x, y = y, x
        self.parent[x] += self.parent[y]
        self.parent[y] = x
        return True

    def undo(self):
        if not self.history:
            return False
        for _ in range(2):
            x, par_x = self.history.pop()
            self.parent[x] = par_x
        return True

    def same(self, x, y):
        return self.root(x) == self.root(y)

    def size(self, x):
        return -self.parent[self.root(x)]