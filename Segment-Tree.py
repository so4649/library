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


# 別パターン
class SegmentTree():
    def __init__(self, init, unitX, f):
        self.f = f # (X, X) -> X
        self.unitX = unitX
        self.f = f
        if type(init) == int:
            self.n = init
            self.n = 1 << (self.n - 1).bit_length()
            self.X = [unitX] * (self.n * 2)
        else:
            self.n = len(init)
            self.n = 1 << (self.n - 1).bit_length()
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
        if l >= self.n: return self.n
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
        return self.n
    
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




# 遅延評価セグメント木 RMQ(最小値) and RUQ(値の更新)
INF = 2**31-1

LV = (N-1).bit_length()
N0 = 2**LV
data = [INF]*(2*N0)
lazy = [None]*(2*N0)

# 伝搬される区間のインデックス(1-indexed)を全て列挙するgenerator
def gindex(l, r):
    L = l + N0; R = r + N0
    lm = (L // (L & -L)) >> 1
    rm = (R // (R & -R)) >> 1
    while L < R:
        if R <= rm:
            yield R
        if L <= lm:
            yield L
        L >>= 1; R >>= 1
    while L:
        yield L
        L >>= 1

# 1-indexedで単調増加のインデックスリストを渡す
def propagates(*ids):
    for i in reversed(ids):
        v = lazy[i-1]
        if v is None:
            continue
        lazy[2*i-1] = data[2*i-1] = lazy[2*i] = data[2*i] = v
        lazy[i-1] = None

def update(l, r, x):
    *ids, = gindex(l, r)
    # 1. トップダウンにlazyの値を伝搬
    propagates(*ids)
 
    # 2. 区間[l, r)のdata, lazyの値を更新
    L = N0 + l; R = N0 + r
    while L < R:
        if R & 1:
            R -= 1
            lazy[R-1] = data[R-1] = x
        if L & 1:
            lazy[L-1] = data[L-1] = x
            L += 1
        L >>= 1; R >>= 1

    # 3. 伝搬させた区間について、ボトムアップにdataの値を伝搬する
    for i in ids:
        data[i-1] = min(data[2*i-1], data[2*i])

def query(l, r):
    # 1. トップダウンにlazyの値を伝搬
    propagates(*gindex(l, r))
    L = N0 + l; R = N0 + r

    # 2. 区間[l, r)の最小値を求める
    s = INF
    while L < R:
        if R & 1:
            R -= 1
            s = min(s, data[R-1])
        if L & 1:
            s = min(s, data[L-1])
            L += 1
        L >>= 1; R >>= 1
    return s

# 恐らく以下のようにして対象を入れる
for i in range(N):
    update(i,i+1,a[i])

# ---------------------------------------------------------------------

# 遅延評価セグメント木 RMQ(最小値) and RAQ(値の加算)
INF = 2**31-1

LV = (N-1).bit_length()
N0 = 2**LV
data = [0]*(2*N0)
lazy = [0]*(2*N0)

def gindex(l, r):
    L = l + N0; R = r + N0
    lm = (L // (L & -L)) >> 1
    rm = (R // (R & -R)) >> 1
    while L < R:
        if R <= rm:
            yield R
        if L <= lm:
            yield L
        L >>= 1; R >>= 1
    while L:
        yield L
        L >>= 1

def propagates(*ids):
    for i in reversed(ids):
        v = lazy[i-1]
        if not v:
            continue
        lazy[2*i-1] += v; lazy[2*i] += v
        data[2*i-1] += v; data[2*i] += v
        lazy[i-1] = 0

def update(l, r, x):
    # 2. 区間[l, r)のdata, lazyの値を更新
    L = N0 + l; R = N0 + r
    while L < R:
        if R & 1:
            R -= 1
            lazy[R-1] += x; data[R-1] += x
        if L & 1:
            lazy[L-1] += x; data[L-1] += x
            L += 1
        L >>= 1; R >>= 1

    # 3. 更新される区間を部分的に含んだ区間のdataの値を更新 (lazyの値を考慮)
    for i in gindex(l, r):
        data[i-1] = min(data[2*i-1], data[2*i]) + lazy[i-1]

def query(l, r):
    # 1. トップダウンにlazyの値を伝搬
    propagates(*gindex(l, r))
    L = N0 + l; R = N0 + r

    # 2. 区間[l, r)の最小値を求める
    s = INF
    while L < R:
        if R & 1:
            R -= 1
            s = min(s, data[R-1])
        if L & 1:
            s = min(s, data[L-1])
            L += 1
        L >>= 1; R >>= 1
    return s

# 恐らく以下のようにして対象を入れる
for i in range(N):
    update(i,i+1,a[i])


# https://tjkendev.github.io/procon-library/python/range_query/rsq_ruq_segment_tree_lp.html
# RSQ and RUQ (区間の合計と区間の値の更新)

# N: 処理する区間の長さ
LV = (N-1).bit_length()
N0 = 2**LV
data = [0]*(2*N0)
lazy = [None]*(2*N0)

def gindex(l, r):
    L = (l + N0) >> 1; R = (r + N0) >> 1
    lc = 0 if l & 1 else (L & -L).bit_length()
    rc = 0 if r & 1 else (R & -R).bit_length()
    for i in range(LV):
        if rc <= i:
            yield R
        if L < R and lc <= i:
            yield L
        L >>= 1; R >>= 1

# 遅延伝搬処理
def propagates(*ids):
    for i in reversed(ids):
        v = lazy[i-1]
        if v is None:
            continue
        lazy[2*i-1] = lazy[2*i] = data[2*i-1] = data[2*i] = v >> 1
        lazy[i-1] = None

# 区間[l, r)をxに更新
def update(l, r, x):
    *ids, = gindex(l, r)
    propagates(*ids)

    L = N0 + l; R = N0 + r
    v = x
    while L < R:
        if R & 1:
            R -= 1
            lazy[R-1] = data[R-1] = v
        if L & 1:
            lazy[L-1] = data[L-1] = v
            L += 1
        L >>= 1; R >>= 1; v <<= 1
    for i in ids:
        data[i-1] = data[2*i-1] + data[2*i]

# 区間[l, r)内の合計を求める
def query(l, r):
    propagates(*gindex(l, r))
    L = N0 + l; R = N0 + r

    s = 0
    while L < R:
        if R & 1:
            R -= 1
            s += data[R-1]
        if L & 1:
            s += data[L-1]
            L += 1
        L >>= 1; R >>= 1
    return s




# ACLBCのEでの提出。遅延セグ木一般化

# op_X:演算
# e_X:演算の単位元
# mapping:作用素を反映させる関数
# compose:作用素同士をマージさせる関数
# id_M:composeの単位元
class LazySegmentTree:
    def __init__(self, op_X, e_X, mapping, compose, id_M, N, array=None):
        __slots__ = ["op_X","e_X","mapping","compose","id_M","N","log","N0","data","lazy"]
        #  それぞれ Xの演算、単位元、f(x),  f\circ g, Xの恒等変換
        self.e_X = e_X; self.op_X = op_X; self.mapping = mapping; self.compose = compose; self.id_M = id_M
        self.N = N
        self.log = (N-1).bit_length()
        self.N0 = 1<<self.log
        self.data = [e_X]*(2*self.N0)
        self.lazy = [id_M]*self.N0
        if array is not None:
            assert N == len(array)
            self.data[self.N0:self.N0+self.N] = array
            for i in range(self.N0-1,0,-1): self.update(i)
 
    # 1点更新
    def point_set(self, p, x):
        p += self.N0
        for i in range(self.log, 0,-1):
            self.push(p>>i)
        self.data[p] = x
        for i in range(1, self.log + 1):
            self.update(p>>i)
 
    # 1点取得
    def point_get(self, p):
        p += self.N0
        for i in range(self.log, 0, -1):
            self.push(p>>i)
        return self.data[p]
 
    # 半開区間[L,R)をopでまとめる
    def prod(self, l, r):
        if l == r: return self.e_X
        l += self.N0
        r += self.N0
        for i in range(self.log, 0, -1):
            if (l>>i)<<i != l:
                self.push(l>>i)
            if (r>>i)<<i != r:
                self.push(r>>i)
 
        sml = smr = self.e_X
        while l < r:
            if l & 1: 
                sml = self.op_X(sml, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.op_X(self.data[r], smr)
            l >>= 1
            r >>= 1
        return self.op_X(sml, smr)
 
    # 全体をopでまとめる
    def all_prod(self): return self.data[1]
 
    # 1点作用
    def apply(self, p, f):
        p += self.N0
        for i in range(self.log, 0, -1):
            self.push(p>>i)
        self.data[p] = self.mapping(f, self.data[p])
        for i in range(1, self.log + 1):
            self.update(p>>i)
 
    # 区間作用
    def apply(self, l, r, f):
        if l == r: return
        l += self.N0
        r += self.N0
        for i in range(self.log, 0, -1):
            if (l>>i)<<i != l:
                self.push(l>>i)
            if (r>>i)<<i != r:
                self.push((r-1)>>i)
 
        l2, r2 = l, r
        while l < r:
            if l & 1: 
                self.all_apply(l, f)
                l += 1
            if r & 1:
                r -= 1
                self.all_apply(r, f)
            l >>= 1
            r >>= 1
 
        l, r = l2, r2
        for i in range(1, self.log + 1):
            if (l>>i)<<i != l:
                self.update(l>>i)
            if (r>>i)<<i != r:
                self.update((r-1)>>i)
     
    """
    始点 l を固定
    f(x_l*...*x_{r-1}) が True になる最大の r 
    つまり TTTTFFFF となるとき、F となる最小の添え字
    存在しない場合 n が返る
    f(e_M) = True でないと壊れる
    """
    def max_right(self, l, g):
        if l == self.N: return self.N
        l += self.N0
        for i in range(self.log, 0, -1): self.push(l>>i)
        sm = self.e_X
        while True:
            while l&1 == 0:
                l >>= 1
            if not g(self.op_X(sm, self.data[l])):
                while l < self.N0:
                    self.push(l)
                    l *= 2
                    if g(self.op_X(sm, self.data[l])):
                        sm = self.op_X(sm, self.data[l])
                        l += 1
                return l - self.N0
            sm = self.op_X(sm, self.data[l])
            l += 1
            if l&-l == l: break
        return self.N
 
    """
    終点 r を固定
    f(x_l*...*x_{r-1}) が True になる最小の l
    つまり FFFFTTTT となるとき、T となる最小の添え字
    存在しない場合 r が返る
    f(e_M) = True でないと壊れる
    """
    def min_left(self, r, g):
        if r == 0: return 0
        r += self.N0
        for i in range(self.log, 0, -1): self.push((r-1)>>i)
        sm = self.e_X
        while True:
            r -= 1
            while r>1 and r&1:
                r >>= 1
            if not g(self.op_X(self.data[r], sm)):
                while r < self.N0:
                    self.push(r)
                    r = 2*r + 1
                    if g(self.op_X(self.data[r], sm)):
                        sm = self.op_X(self.data[r], sm)
                        r -= 1
                return r + 1 - self.N0
            sm = self.op_X(self.data[r], sm)
            if r&-r == r: break
        return 0
        
    # 以下内部関数
    def update(self, k):
        self.data[k] = self.op_X(self.data[2*k], self.data[2*k+1])
    
    def all_apply(self, k, f):
        self.data[k] = self.mapping(f, self.data[k])
        if k < self.N0:
            self.lazy[k] = self.compose(f, self.lazy[k])
 
    def push(self, k): #propagate と同じ
        if self.lazy[k] is self.id_M: return
        self.data[2*k  ] = self.mapping(self.lazy[k], self.data[2*k])
        self.data[2*k+1] = self.mapping(self.lazy[k], self.data[2*k+1])
        if 2*k < self.N0:
            self.lazy[2*k]   = self.compose(self.lazy[k], self.lazy[2*k])
            self.lazy[2*k+1] = self.compose(self.lazy[k], self.lazy[2*k+1])
        self.lazy[k] = self.id_M
 
###################################################################
 
e_X = 0
id_M = 0
def op_X(X,Y):
    x1,d1 = X>>32,X&MASK
    x2,d2 = Y>>32,Y&MASK
    return (((x1*p10[d2]+x2)%MOD)<<32) + d1+d2    
 
def compose(f,g):
    return f
 
def mapping(f,X):
    if f==0:
        return X
    else:
        x,d = X>>32, X&MASK
        return (((p10[d]-1)*inv9*f%MOD)<<32) + d
        
 
import sys
readline = sys.stdin.readline
 
MOD = 998244353
MASK = (1<<32) - 1
inv9 = 443664157
 
n,q = map(int, readline().split())
 
p10 = [1]*(n+2)
for i in range(1,n+2):
    p10[i] = p10[i-1]*10%MOD
 
a = [(1<<32) + 1]*n
seg = LazySegmentTree(op_X, e_X, mapping, compose, id_M, n, array=a)
 
#print(seg.all_prod()>>32)
#print([i>>32 for i in seg.data])
 
for _ in range(q):
    l,r,d = map(int, readline().split())
    seg.apply(l-1,r,d)
    print(seg.all_prod()>>32)