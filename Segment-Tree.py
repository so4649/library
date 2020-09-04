# https://qiita.com/takayg1/items/c811bd07c21923d7ec69
# セグ木

#使う操作
#####segfunc#####
def segfunc1(x, y):
    return min(x, y)
#################

#####ide_ele#####
ide_ele1 = float('inf')
#################

class SegTree:
    """
    init(init_val, ide_ele): 配列init_valで初期化 O(N)
    update(k, x): k番目の値をxに更新 O(logN)
    query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
    """
    def __init__(self, init_val, segfunc, ide_ele):
        """
        init_val: 配列の初期値
        segfunc: 区間にしたい操作
        ide_ele: 単位元
        n: 要素数
        num: n以上の最小の2のべき乗
        tree: セグメント木(1-index)
        """
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
        """
        k番目の値をxに更新
        k: index(0-index)
        x: update value
        """
        k += self.num
        self.tree[k] = x
        while k > 1:
            self.tree[k >> 1] = self.segfunc(self.tree[k], self.tree[k ^ 1])
            k >>= 1

    def query(self, l, r):
        """
        [l, r)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
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


# -------------------------------------------------------------------

# https://smijake3.hatenablog.com/entry/2018/11/03/100133

# 普通のセグ木
# Range Minimum Query
N0 = 2**(N-1).bit_length()
INF = 2**31-1
# 0-indexedで管理
data = [INF]*(2*N0)

# k番目の要素の値をxに変更
def update(k, x):
    k += N0-1
    data[k] = x
    while k >= 0:
        k = (k - 1) // 2
        data[k] = min(data[2*k+1], data[2*k+2])

# 区間[l, r)の最小値を求める
def query(l, r):
    L = l + N0; R = r + N0
    s = INF
    # 区間を列挙しながら最小値を求める
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
    update(i,a[i])

# -----------------------------------------------------------------------------

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