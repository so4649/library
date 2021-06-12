# ai = Σcja(i-j) (mod)となるcを求める
# BMして行列累乗しn項目を求める

mod = 998244353
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

# ai = Σcja(i-j) (mod)となるcを求める
def berlekamp_massey(A):
    n = len(A)
    B, C = [1], [1]
    l, m, p = 0, 1, 1
    for i in range(n):
        d = A[i]
        for j in range(1, l + 1):
            d += C[j] * A[i - j]
            d %= mod
        if d == 0:
            m += 1
            continue
        T = C.copy()
        q = pow(p, mod - 2, mod) * d % mod
        if len(C) < len(B) + m:
            C += [0] * (len(B) + m - len(C))
        for j, b in enumerate(B):
            C[j + m] -= q * b
            C[j + m] %= mod
        if 2 * l <= i:
            B = T
            l, m, p = i + 1 - l, 1, d
        else:
            m += 1
    res = [-c % mod for c in C[1:]]
    return res

# BMして行列累乗しn項目を求める
def a_n(a,n):
    b = berlekamp_massey(a)
    if n < len(b):
        return a[n]
        
    A = [b]
    for i in range(len(b)-1):
        A.append([1 if j==i else 0 for j in range(len(b))])
    B = mpow(A,n-len(b)+1)
    return sum(B[0][i]*a[len(b)-1-i] for i in range(len(b))) % mod