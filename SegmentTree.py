# セグ木(0-indexed)
# init:配列の長さまたは配列
# unitX:単位元
# f:演算
class SegmentTree():
    def __init__(self, init, unitX, f):
        self.f = f # (X, X) -> X
        self.unitX = unitX
        if type(init) == int:
            self.l = init
            self.n = 1 << (self.l - 1).bit_length()
            self.X = [unitX] * (self.n * 2)
        else:
            self.l = len(init)
            self.n = 1 << (self.l - 1).bit_length()
            self.X = [unitX] * self.n + init + [unitX] * (self.n - len(init))
            for i in range(self.n-1, 0, -1):
                self.X[i] = self.f(self.X[i*2], self.X[i*2|1])
        
    def update(self, i, x):
        i += self.n
        self.X[i] = x
        i >>= 1
        while i:
            self.X[i] = self.f(self.X[i*2], self.X[i*2|1])
            i >>= 1
    
    def getvalue(self, i):
        return self.X[i + self.n]
    
    # [l,r)
    def getrange(self, l, r):
        l += self.n
        r += self.n
        al = self.unitX
        ar = self.unitX
        while l < r:
            if l & 1:
                al = self.f(al, self.X[l])
                l += 1
            if r & 1:
                r -= 1
                ar = self.f(self.X[r], ar)
            l >>= 1
            r >>= 1
        return self.f(al, ar)
    
    # Find r s.t. calc(l, ..., r-1) = True and calc(l, ..., r) = False
    def max_right(self, l, z):
        if l >= self.l: return self.l
        l += self.n
        s = self.unitX
        while 1:
            while l % 2 == 0:
                l >>= 1
            if not z(self.f(s, self.X[l])):
                while l < self.n:
                    l *= 2
                    if z(self.f(s, self.X[l])):
                        s = self.f(s, self.X[l])
                        l += 1
                return l - self.n
            s = self.f(s, self.X[l])
            l += 1
            if l & -l == l: break
        return self.l
    
    # Find l s.t. calc(l, ..., r-1) = True and calc(l-1, ..., r-1) = False
    def min_left(self, r, z):
        if r <= 0: return 0
        r += self.n
        s = self.unitX
        while 1:
            r -= 1
            while r > 1 and r % 2:
                r >>= 1
            if not z(self.f(self.X[r], s)):
                while r < self.n:
                    r = r * 2 + 1
                    if z(self.f(self.X[r], s)):
                        s = self.f(self.X[r], s)
                        r -= 1
                return r + 1 - self.n
            s = self.f(self.X[r], s)
            if r & -r == r: break
        return 0
    
    def debug(self):
        print("debug")
        print([self.getvalue(i) for i in range(min(self.n, 20))])


# 前に使っていた方
# https://qiita.com/takayg1/items/c811bd07c21923d7ec69

# セグ木 0-indexed
# 使う操作
#####segfunc#####
def segfunc1(x, y):
    return min(x, y)
#################

#####ide_ele#####
ide_ele1 = float('inf')
#################

class SegTree:
    # init(init_val, ide_ele): 配列init_valで初期化 O(N)
    # update(k, x): k番目の値をxに更新 O(logN)
    # query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)

    def __init__(self, init_val, segfunc, ide_ele):
        n = len(init_val)
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1 << (n - 1).bit_length()
        self.tree = [ide_ele] * 2 * self.num
        # 配列の値を葉にセット
        for i in range(n):
            self.tree[self.num + i] = init_val[i]
        # 構築していく
        for i in range(self.num - 1, 0, -1):
            self.tree[i] = self.segfunc(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, k, x):
        k += self.num
        self.tree[k] = x
        while k > 1:
            self.tree[k >> 1] = self.segfunc(self.tree[k], self.tree[k ^ 1])
            k >>= 1

    def query(self, l, r):
        # 区間[l, r)なので注意
        res = self.ide_ele

        l += self.num
        r += self.num
        while l < r:
            if l & 1:
                res = self.segfunc(res, self.tree[l])
                l += 1
            if r & 1:
                res = self.segfunc(res, self.tree[r - 1])
            l >>= 1
            r >>= 1
        return res

a = [14, 5, 9, 13, 7, 12, 11, 1, 7, 8]

seg = SegTree(a, segfunc1, ide_ele1)
# 初めの設定をせず直接以下のようにしてもいい
# seg = SegTree(a, segfunc=min, ide_ele=float('inf'))
# seg = SegTree(a, min, float('inf'))

print(seg.query(0, 8)) # 1
seg.update(5, 0) # 5番目を0に変更
print(seg.query(0, 8)) # 0


# 使いかた

# １：初期化用のリストを用意する
# なんでもいい
a = [14, 5, 9, 13, 7, 12, 11, 1, 7, 8]

# ２：区間に行う操作を決める
def segfunc(x, y):
    return min(x, y)

# ３：単位元を決める
ide_ele = float('inf')

# ４： オブジェクトを作成、引数は上の3つ
seg = SegTree(a, segfunc, ide_ele)
# 初めの設定をせず直接以下のようにしてもいい
# seg = SegTree(a, segfunc=min, ide_ele=float('inf'))

# ５：各操作を行える
# 1. ある1つの要素の更新
# update(k, x) : k番目の要素をxに更新します。
# 2. ある区間の操作の結果を取得
# query(l, r) : [l, r)(l以上r未満の区間)から値を取得します。

# [0, 8)の最小値を表示
print(seg.query(0, 8)) # 1
# 5番目を0に変更
seg.update(5, 0)
# [0, 8)の最小値を表示
print(seg.query(0, 8)) # 0

# 操作
# 操作	segfunc	単位元
# 最小値	min(x, y)	float('inf')
# 最大値	max(x, y)	-float('inf')
# 区間和	x + y	0
# 区間積	x * y	1
# 最大公約数	math.gcd(x, y)	0
# 種類数    x | y   set()