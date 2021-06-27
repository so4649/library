def mult(A, B):
    n, m, l = len(A), len(B), len(B[0])
    ret = [[0]*l for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(l):
                ret[i][k] = (ret[i][k]+A[i][j]*B[j][k])
    return ret

mod = 10**9+7
def mmult(A, B):
    global mod
    n, m, l = len(A), len(B), len(B[0])
    ret = [[0]*l for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(l):
                ret[i][k] = (ret[i][k]+A[i][j]*B[j][k])%mod
    return ret
    
def mpow(A, n):
    if n == 0: return [[1 if i==j else 0 for j in range(len(A))] for i in range(len(A))]
    if n % 2: return mmult(mpow(A, n-1), A)
    return mpow(mmult(A, A), n//2)



# 行列計算が便利なクラス
# メソッドを定義している
# https://judge.yosupo.jp/submission/45096
# https://judge.yosupo.jp/submission/51063

mod = 998244353
class Matrix():
    def __init__(self, n, m, mat=None):
        self.n = n
        self.m = m
        self.mat = [[0] * self.m for _ in range(self.n)]
        if mat:
            assert len(mat) == n and len(mat[0]) == m
            for i in range(self.n):
                self.mat[i] = mat[i].copy()

    def is_square(self):
        return self.n == self.m

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.mat[key]
        else:
            assert key >= 0
            return self.mat[key]

    def id(n):
        res = Matrix(n, n)
        for i in range(n):
            res[i][i] = 1
        return res

    def __len__(self):
        return len(self.mat)

    def __str__(self):
        return '\n'.join(' '.join(map(str, self[i])) for i in range(self.n))

    def times(self, k):
        res = [[0] * self.m for _ in range(self.n)]
        for i in range(self.n):
            res_i, self_i = res[i], self[i]
            for j in range(self.m):
                res_i[j] = k * self_i[j] % mod
        return Matrix(self.n, self.m, res)

    def __pos__(self):
        return self

    def __neg__(self):
        return self.times(-1)

    def __add__(self, other):
        assert self.n == other.n and self.m == other.m
        res = [[0] * self.m for _ in range(self.n)]
        for i in range(self.n):
            res_i, self_i, other_i = res[i], self[i], other[i]
            for j in range(self.m):
                res_i[j] = (self_i[j] + other_i[j]) % mod
        return Matrix(self.n, self.m, res)

    def __sub__(self, other):
        assert self.n == other.n and self.m == other.m
        res = [[0] * self.m for _ in range(self.n)]
        for i in range(self.n):
            res_i, self_i, other_i = res[i], self[i], other[i]
            for j in range(self.m):
                res_i[j] = (self_i[j] - other_i[j]) % mod
        return Matrix(self.n, self.m, res)

    def __mul__(self, other):
        if other.__class__ == Matrix:
            assert self.m == other.n
            res = [[0] * other.m for _ in range(self.n)]
            for i in range(self.n):
                res_i, self_i = res[i], self[i]
                for k in range(self.m):
                    self_ik, other_k = self_i[k], other[k]
                    for j in range(other.m):
                        res_i[j] += self_ik * other_k[j]
                        res_i[j] %= mod
            return Matrix(self.n, other.m, res)
        else:
            return self.times(other)

    def __rmul__(self, other):
        return self.times(other)

    def __pow__(self, k):
        assert self.is_square()
        tmp = Matrix(self.n, self.n, self.mat)
        res = Matrix.id(self.n)
        while k:
            if k & 1:
                res *= tmp
            tmp *= tmp
            k >>= 1
        return res

    # 行列式
    def determinant(self):
        assert self.is_square()
        res = 1
        tmp = Matrix(self.n, self.n, self.mat)
        for j in range(self.n):
            if tmp[j][j] == 0:
                for i in range(j + 1, self.n):
                    if tmp[i][j]:
                        break
                else:
                    return 0
                tmp.mat[j], tmp.mat[i] = tmp.mat[i], tmp.mat[j]
                res *= -1
            tmp_j = tmp[j]
            inv = pow(tmp_j[j], mod - 2, mod)
            for i in range(j + 1, self.n):
                tmp_i = tmp[i]
                c = -inv * tmp_i[j] % mod
                for k in range(self.n):
                    tmp_i[k] += c * tmp_j[k]
                    tmp_i[k] %= mod
        for i in range(self.n):
            res *= tmp[i][i]
            res %= mod
        return res

    # 逆行列（存在しなければ-1)
    def inverse(self):
        assert self.is_square()
        res = Matrix.id(self.n)
        tmp = Matrix(self.n, self.n, self.mat)
        for j in range(self.n):
            if tmp[j][j] == 0:
                for i in range(j + 1, self.n):
                    if tmp[i][j]:
                        break
                else:
                    return -1
                tmp.mat[j], tmp.mat[i] = tmp.mat[i], tmp.mat[j]
                res.mat[j], res.mat[i] = res.mat[i], res.mat[j]
            tmp_j, res_j = tmp[j], res[j]
            inv = pow(tmp_j[j], mod - 2, mod)
            for k in range(self.n):
                tmp_j[k] *= inv
                tmp_j[k] %= mod
                res_j[k] *= inv
                res_j[k] %= mod
            for i in range(self.n):
                if i == j: continue
                c = tmp[i][j]
                tmp_i, res_i = tmp[i], res[i]
                for k in range(self.n):
                    tmp_i[k] -= tmp_j[k] * c
                    tmp_i[k] %= mod
                    res_i[k] -= res_j[k] * c
                    res_i[k] %= mod
        return res

    # 線形連立方程式
    # dim:解の次元(解なしの場合-1)
    # sol:解の１つ
    # vecs:基底ベクトル
    def linear_equations(self, vec):
        assert self.n == len(vec)
        aug = [self[i] + [vec[i]] for i in range(self.n)]
        rank = 0
        p = []
        q = []
        for j in range(self.m + 1):
            for i in range(rank, self.n):
                if aug[i][j]: break
            else:
                q.append(j)
                continue
            if j == self.m: return -1, [], []
            p.append(j)
            aug[rank], aug[i] = aug[i], aug[rank]
            inv = pow(aug[rank][j], mod - 2, mod)
            aug_rank = aug[rank]
            for k in range(self.m + 1):
                aug_rank[k] *= inv
                aug_rank[k] %= mod
            for i in range(self.n):
                if i == rank: continue
                aug_i = aug[i]
                c = -aug_i[j]
                for k in range(self.m + 1):
                    aug_i[k] += c * aug_rank[k]
                    aug_i[k] %= mod
            rank += 1
        dim = self.m - rank
        sol = [0] * self.m
        for i in range(rank):
            sol[p[i]] = aug[i][-1]
        vecs = [[0] * self.m for _ in range(dim)]
        for i in range(dim):
            vecs[i][q[i]] = 1
        for i in range(dim):
            vecs_i = vecs[i]
            for j in range(rank):
                vecs_i[p[j]] = -aug[j][q[i]] % mod
        return dim, sol, vecs

import sys
input = sys.stdin.buffer.readline

N, M = map(int, input().split())
A = Matrix(N, M, [list(map(int, input().split())) for _ in range(N)])
B = list(map(int, input().split()))

dim, sol, vecs = A.linear_equations(B)

if dim == -1:
    print(-1)

else:
    print(dim)
    print(*sol)
    for v in vecs:
        print(*v)



# 2進数を要素とした1次元配列で表された行列のxor演算した時のrank
def xor_rank(A):
    base = []
    for i in A:
        for j in base:
            i = min(i,i^j)
        if i:
            base.append(i)
    return len(base)