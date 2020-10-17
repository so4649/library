class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

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
        self.group = {r:[] for r in self.roots()}
        for i in range(self.n):
            self.group[self.find(i)].append(i)
        return '\n'.join('{}: {}'.format(r, self.group[r]) for r in self.roots())

#URL
#https://note.nkmk.me/python-union-find/
# parents
# 各要素の親要素の番号を格納するリスト
# 要素が根（ルート）の場合は-(そのグループの要素数)を格納する
# find(x)
# 要素xが属するグループの根を返す
# union(x, y)
# 要素xが属するグループと要素yが属するグループとを併合する
# size(x)
# 要素xが属するグループのサイズ（要素数）を返す
# same(x, y)
# 要素x, yが同じグループに属するかどうかを返す
# members(x)
# 要素xが属するグループに属する要素をリストで返す
# 関連記事: Pythonリスト内包表記の使い方
# roots()
# すべての根の要素をリストで返す
# group_count()
# グループの数を返す
# all_group_members
# {ルート要素: [そのグループに含まれる要素のリスト], ...}の辞書を返す
# 関連記事: Pythonで辞書を作成するdict()と波括弧、辞書内包表記
# __str__()
# print()での表示用
# ルート要素: [そのグループに含まれる要素のリスト]を文字列で返す

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