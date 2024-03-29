# -----------------------------------------------------------
# Bostan-Mori法？O(klogklogN)
# Kth term of Linearly Recurrent Sequence
# https://judge.yosupo.jp/problem/kth_term_of_linearly_recurrent_sequence
# 任意modは835行目から

mod = 998244353
sum_e = (911660635, 509520358, 369330050, 332049552, 983190778, 123842337, 238493703, 975955924, 603855026, 856644456, 131300601, 842657263, 730768835, 942482514, 806263778, 151565301, 510815449, 503497456, 743006876, 741047443, 56250497)
sum_ie = (86583718, 372528824, 373294451, 645684063, 112220581, 692852209, 155456985, 797128860, 90816748, 860285882, 927414960, 354738543, 109331171, 293255632, 535113200, 308540755, 121186627, 608385704, 438932459, 359477183, 824071951)

def sqrt_mod(a):
    a %= mod
    if a < 2:
        return a
    k = (mod - 1) // 2
    if pow(a, k, mod) != 1:
        return -1
    b = 1
    while pow(b, k, mod) == 1:
        b += 1
    m, e = mod - 1, 0
    while m % 2 == 0:
        m >>= 1
        e += 1
    x = pow(a, (m - 1) // 2, mod)
    y = a * x * x % mod
    x *= a
    x %= mod
    z = pow(b, m, mod)
    while y != 1:
        j, t = 0, y
        while t != 1:
            j += 1
            t *= t
            t %= mod
        z = pow(z, 1 << (e - j - 1), mod)
        x *= z
        x %= mod
        z *= z
        z %= mod
        y *= z
        y %= mod
        e = j
    return x
    
def inv_mod(a):
    a %= mod
    if a == 0:
        return 0
    s, t = mod, a
    m0, m1 = 0, 1
    while t:
        u = s // t
        s -= t * u
        m0 -= m1 * u
        s, t = t, s
        m0, m1 = m1, m0
    if m0 < 0:
        m0 += mod // s
    return m0

fac_ = [1, 1]
finv_ = [1, 1]
inv_ = [1, 1]
def fac(i):
    while i >= len(fac_):
        fac_.append(fac_[-1] * len(fac_) % mod)
    return fac_[i]
def finv(i):
    while i >= len(inv_):
        inv_.append((-inv_[mod % len(inv_)]) * (mod // len(inv_)) % mod)
    while i >= len(finv_):
        finv_.append(finv_[-1] * inv_[len(finv_)] % mod)
    return finv_[i]
def inv(i):
    while i >= len(inv_):
        inv_.append((-inv_[mod % len(inv_)]) * (mod // len(inv_)) % mod)
    return inv_[i]

def butterfly(A):
    n = len(A)
    h = (n - 1).bit_length()
    for ph in range(1, h + 1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        now = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = A[i + offset]
                r = A[i + offset + p] * now
                A[i + offset] = (l + r) % mod
                A[i + offset + p] = (l - r) % mod
            now *= sum_e[(~s & -~s).bit_length() - 1]
            now %= mod
    
def butterfly_inv(A):
    n = len(A)
    h = (n - 1).bit_length()
    for ph in range(h, 0, -1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        inow = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = A[i + offset]
                r = A[i + offset + p]
                A[i + offset] = (l + r) % mod
                A[i + offset + p] = (mod + l - r) * inow % mod
            inow *= sum_ie[(~s & -~s).bit_length() - 1]
            inow %= mod
    iz = inv_mod(n)
    for i in range(n):
        A[i] *= iz
        A[i] %= mod
    
def convolution(_A, _B):
    A = _A.copy()
    B = _B.copy()
    n = len(A)
    m = len(B)
    if not n or not m:
        return []
    if min(n, m) <= 60:
        if n < m:
            n, m = m, n
            A, B = B, A
        res = [0] * (n + m - 1)
        for i in range(n):
            for j in range(m):
                res[i + j] += A[i] * B[j]
                res[i + j] %= mod
        return res
    z = 1 << (n + m - 2).bit_length()
    A += [0] * (z - n)
    B += [0] * (z - m)
    butterfly(A)
    butterfly(B)
    for i in range(z):
        A[i] *= B[i]
        A[i] %= mod
    butterfly_inv(A)
    return A[:n + m - 1]

def autocorrelation(_A):
    A = _A.copy()
    n = len(A)
    if not n:
        return []
    if n <= 60:
        res = [0] * (n + n - 1)
        for i in range(n):
            for j in range(n):
                res[i + j] += A[i] * A[j]
                res[i + j] %= mod
        return res
    z = 1 << (n + n - 2).bit_length()
    A += [0] * (z - n)
    butterfly(A)
    for i in range(z):
        A[i] *= A[i]
        A[i] %= mod
    butterfly_inv(A)
    return A[:n + n - 1]


class FormalPowerSeries:
    def __init__(self, poly=[]):
        self.poly = [p % mod for p in poly]
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            res = self.poly[key]
            return FormalPowerSeries(res)
        else:
            if key < 0:
                raise IndexError("list index out of range")
            if key >= len(self.poly):
                return 0
            else:
                return self.poly[key]
    
    def __setitem__(self, key, value):
        if key < 0:
            raise IndexError("list index out of range")
        if key >= len(self.poly):
            self.poly += [0] * (key - len(self.poly) + 1)
        self.poly[key] = value % mod
    
    def __len__(self):
        return len(self.poly)
    
    def resize(self, size):
        if len(self) >= size:
            return self[:size]
        else:
            return FormalPowerSeries(self.poly + [0] * (size - len(self)))
    
    def shrink(self):
        while self.poly and self.poly[-1] == 0:
            self.poly.pop()
        return self
    
    def times(self, n):
        n %= mod
        res = [p * n for p in self.poly]
        return FormalPowerSeries(res)
        
    def __pos__(self):
        return self
    
    def __neg__(self):
        return self.times(-1)
    
    def __add__(self, other):
        if other.__class__ == FormalPowerSeries:
            s = len(self)
            t = len(other)
            n = min(s, t)
            res = [self[i] + other[i] for i in range(n)]
            if s >= t:
                res += self.poly[t:]
            else:
                res += other.poly[s:]
            return FormalPowerSeries(res)
        else:
            return self + FormalPowerSeries([other])
            
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return (-self) + other
    
    def __mul__(self, other):
        if other.__class__ == FormalPowerSeries:
            res = convolution(self.poly, other.poly)
            return FormalPowerSeries(res)
        else:
            return self.times(other)
    
    def __rmul__(self, other):
        return self.times(other)
    
    def __lshift__(self, other):
        return FormalPowerSeries(([0] * other) + self.poly)
    
    def __rshift__(self, other):
        return self[other:]
    
    def square(self):
        res = autocorrelation(self.poly)
        return FormalPowerSeries(res)

    def inv(self, deg=-1):
        if deg == -1:
            deg = len(self) - 1
        r = inv_mod(self[0])
        m = 1
        T = [0] * (deg + 1)
        T[0] = r
        res = FormalPowerSeries(T)
        while m <= deg:
            F = [0] * (2 * m)
            G = [0] * (2 * m)
            for j in range(min(len(self), 2 * m)):
                F[j] = self[j]
            for j in range(m):
                G[j] = res[j]
            butterfly(F)
            butterfly(G)
            for j in range(2 * m):
                F[j] *= G[j]
                F[j] %= mod
            butterfly_inv(F)
            for j in range(m):
                F[j] = 0
            butterfly(F)
            for j in range(2 * m):
                F[j] *= G[j]
                F[j] %= mod
            butterfly_inv(F)
            for j in range(m, min(2 * m, deg + 1)):
                res[j] = -F[j]
            m <<= 1
        return res
    
    #P/Q
    def __truediv__(self, other):
        if other.__class__ == FormalPowerSeries:
            return (self * other.inv())
        else:
            return self * inv_mod(other)
    
    def __rtruediv__(self, other):
        return other * self.inv()
        
    #P,Qを多項式として見たときのPをQで割った商を求める
    def __floordiv__(self, other):
        if other.__class__ == FormalPowerSeries:
            if len(self) < len(other):
                return FormalPowerSeries()
            else:
                m = len(self) - len(other) + 1
                res = (self[-1:-m-1:-1] * other[::-1].inv(m))[m-1::-1]
                return res.shrink()
        else:
            return self * inv_mod(other)

    def __rfloordiv__(self, other):
        return other * self.inv()

    def __mod__(self, other):
        if len(self) < len(other):
            return self[:]
        else:
            res = self[:len(other) - 1] - ((self // other) * other)[:len(other) - 1]
            return res.shrink()
    
    def differentiate(self, deg=-1):
        if deg == -1:
            deg = len(self) - 2
        res = FormalPowerSeries([0] * (deg + 1))
        for i in range(1, min(len(self), deg + 2)):
            res[i - 1] = self[i] * i
        return res
    
    def integrate(self, deg=-1):
        if deg == -1:
            deg = len(self)
        res = FormalPowerSeries([0] * (deg + 1))
        for i in range(min(len(self), deg)):
            res[i + 1] = self[i] * inv(i + 1)
        return res
    
    def log(self, deg=-1):
        if deg == -1:
            deg = len(self) - 1
        return (self.differentiate() * self.inv(deg - 1))[:deg].integrate()
    
    def exp(self, deg=-1):
        if deg == -1:
            deg = len(self) - 1
        T = [0] * (deg + 1)
        T[0] = 1 #T:res^{-1}
        res = FormalPowerSeries(T)
        m = 1
        F = [1]
        while m <= deg:
            G = T[:m]
            butterfly(G)
            FG = [F[i] * G[i] % mod for i in range(m)]
            butterfly_inv(FG)
            FG[0] -= 1
            delta = [0] * (2 * m)
            for i in range(m):
                delta[i + m] = FG[i]
            eps = [0] * (2 * m)
            if m == 1:
                DF = []
            else:
                DF = res.differentiate(m - 2).poly
            DF.append(0)
            butterfly(DF)
            for i in range(m):
                DF[i] *= G[i]
                DF[i] %= mod
            butterfly_inv(DF)
            for i in range(m - 1):
                eps[i] = self[i + 1] * (i + 1) % mod
                eps[i + m] = DF[i] - eps[i]
            eps[m - 1] = DF[m - 1]
            butterfly(delta)
            DH = [0] * (2 * m)
            for i in range(m - 1):
                DH[i] = eps[i]
            butterfly(DH)
            for i in range(2 * m):
                delta[i] *= DH[i]
                delta[i] %= mod
            butterfly_inv(delta)
            for i in range(m, 2 * m):
                eps[i] -= delta[i]
                eps[i] %= mod
            for i in range(2 * m - 1, 0, -1):
                eps[i] = (eps[i - 1] * inv(i) - self[i]) % mod
            eps[0] = -self[0]
            butterfly(eps)
            for i in range(m):
                DH[i] = res[i]
                DH[i + m] = 0
            butterfly(DH)
            for i in range(2 * m):
                eps[i] *= DH[i]
                eps[i] %= mod
            butterfly_inv(eps)
            for i in range(m, min(2 * m, deg + 1)):
                res[i] = -eps[i]
            if 2 * m > deg:
                break
            F = [0] * (2 * m)
            G = [0] * (2 * m)
            for i in range(2 * m):
                F[i] = res[i]
            for i in range(m):
                G[i] = T[i]
            butterfly(F)
            butterfly(G)
            P = [F[i] * G[i] % mod for i in range(2 * m)]
            butterfly_inv(P)
            for i in range(m):
                P[i] = 0
            butterfly(P)
            for i in range(2 * m):
                P[i] *= G[i]
                P[i] %= mod
            butterfly_inv(P)
            for i in range(m, 2 * m):
                T[i] = -P[i]
            m <<= 1
        return res
        
    def __pow__(self, n, deg=-1):
        if deg == -1:
            deg = len(self) - 1
        m = abs(n)
        for d, p in enumerate(self.poly):
            if p:
                break
        else:
            return FormalPowerSeries()
        if d * m >= len(self):
            return FormalPowerSeries()
        G = self[d:]
        G = ((G * inv_mod(p)).log() * m).exp() * pow(p, m, mod)
        res = FormalPowerSeries([0] * (d * m) + G.poly)
        if n >= 0:
            return res[:deg + 1]
        else:
            return res.inv()[:deg + 1]
    
    def sqrt(self, deg=-1):
        if deg == -1:
            deg = len(self) - 1
        if len(self) == 0:
            return FormalPowerSeries()
        if self[0] == 0:
            for d in range(1, len(self)):
                if self[d]:
                    if d & 1:
                        return -1
                    if deg < d // 2:
                        break
                    res = self[d:].sqrt(deg - d // 2)
                    if res == -1:
                        return -1
                    res = res << (d // 2)
                    return res
            return FormalPowerSeries()
        
        sqr = sqrt_mod(self[0])
        if sqr == -1:
            return -1
        T = [0] * (deg + 1)
        T[0] = sqr
        res = FormalPowerSeries(T)
        T[0] = inv_mod(sqr) #T:res^{-1}
        m = 1
        two_inv = (mod + 1) // 2
        F = [sqr]
        while m <= deg:
            for i in range(m):
                F[i] *= F[i]
                F[i] %= mod
            butterfly_inv(F)
            delta = [0] * (2 * m)
            for i in range(m):
                delta[i + m] = F[i] - self[i] - self[i + m]
            butterfly(delta)
            G = [0] * (2 * m)
            for i in range(m):
                G[i] = T[i]
            butterfly(G)
            for i in range(2 * m):
                delta[i] *= G[i]
                delta[i] %= mod
            butterfly_inv(delta)
            for i in range(m, min(2 * m, deg + 1)):
                res[i] = -delta[i] * two_inv
            if 2 * m > deg:
                break
            F = res.poly[:2 * m]
            butterfly(F)
            eps = [F[i] * G[i] % mod for i in range(2 * m)]
            butterfly_inv(eps)
            for i in range(m):
                eps[i] = 0
            butterfly(eps)
            for i in range(2 * m):
                eps[i] *= G[i]
                eps[i] %= mod
            butterfly_inv(eps)
            for i in range(m, 2 * m):
                T[i] = -eps[i]
            m <<= 1
        return res
    
    #各p_i(0<=i<m)についてf(p_i)を求める
    def multipoint_evaluation(self, P):
        m = len(P)
        size = 1 << (m - 1).bit_length()
        G = [FormalPowerSeries([1]) for _ in range(2 * size)]
        for i in range(m):
            G[size + i] = FormalPowerSeries([-P[i], 1])
        for i in range(size - 1, 0, -1):
            G[i] = G[2 * i] * G[2 * i + 1]
        G[1] = self % G[1]
        for i in range(2, size + m):
            G[i] = G[i >> 1] % G[i]
        res = [G[i][0] for i in range(size, size + m)]
        return res
    
    #f(x+a)
    def taylor_shift(self, a):
        a %= mod
        n = len(self)
        t = 1
        F = self[:]
        G = FormalPowerSeries([0] * n)
        for i in range(n):
            F[i] *= fac(i)
        for i in range(n):
            G[i] = t * finv(i)
            t = t * a % mod
        res = (F * G[::-1])[n - 1:]
        for i in range(n):
            res[i] *= finv(i)
        return res

    #Q(P)
    def composition(self, P, deg=-1):
        if deg == -1:
            deg = len(self) - 1
        k = int(deg ** 0.5 + 1)
        d = (deg + k) // k
        X = [FormalPowerSeries([1])]
        for i in range(k):
            X.append((X[i] * P)[:deg + 1])
        Y = [FormalPowerSeries([0] * (deg + 1)) for _ in range(k)]
        for i, y in enumerate(Y):
            for j, x in enumerate(X[:d]):
                if i * d + j > deg:
                    break
                for t in range(deg + 1):
                    if t >= len(x):
                        break
                    y[t] += x[t] * self[i * d + j]
        res = FormalPowerSeries([0] * (deg + 1))
        Z = FormalPowerSeries([1])
        x = X[d]
        for i in range(k):
            Y[i] = (Y[i] * Z)[:deg + 1]
            for j in range(len(Y[i])):
                res[j] += Y[i][j]
            Z = (Z * x)[:deg + 1]
        return res
        
        
    
#[x^n]P/Qを求める(deg(Q) > deg(P))
def poly_coeff(Q, P, n):
    m = 1 << (len(Q) - 1).bit_length()
    P = P + [0] * (2 * m - len(P))
    Q = Q + [0] * (2 * m - len(Q))
    butterfly(P)
    butterfly(Q)
    S = [0] * (2 * m)
    T = [0] * (2 * m)
    w = pow(3, (mod - 1) // (2 * m), mod)
    dw = pow(w, mod - 2, mod)
    btr = [0] * m
    logn = (m - 1).bit_length()
    for i in range(m):
        btr[i] = (btr[i >> 1] >> 1) + ((i & 1) << (logn - 1))
    while n:
        inv2 = (mod + 1) // 2
        S = S[:m]
        T = T[:m]
        for i in range(m):
            T[i] = Q[i << 1 | 0] * Q[i << 1 | 1] % mod
        if n & 1:
            for i in btr:
                S[i] = (P[i << 1 | 0] * Q[i << 1 | 1] - P[i << 1 | 1] * Q[i << 1 | 0]) % mod * inv2 % mod
                inv2 *= dw
                inv2 %= mod
        else:
            for i in range(m):
                S[i] = (P[i << 1 | 0] * Q[i << 1 | 1] + P[i << 1 | 1] * Q[i << 1 | 0]) % mod * inv2 % mod
        P, S = S, P
        Q, T = T, Q
        n >>= 1
        if n < m:
            break
        F = P[:]
        G = Q[:]
        butterfly_inv(F)
        butterfly_inv(G)
        coeff = 1
        for i in range(m):
            F[i] *= coeff
            F[i] %= mod
            G[i] *= coeff
            G[i] %= mod
            coeff *= w
            coeff %= mod
        butterfly(F)
        butterfly(G)
        P += F
        Q += G
    butterfly_inv(P)
    butterfly_inv(Q)
    return (FormalPowerSeries(P) * FormalPowerSeries(Q).inv())[n]
        

def subset_sum(A, limit):
    C = [0] * (limit + 1)
    for a in A:
        C[a] += 1
    res = FormalPowerSeries([0] * (limit + 1))
    for i in range(1, limit + 1):
        for k in range(1, limit // i + 1):
            j = i * k
            res[j] += ((k & 1) * 2 - 1) * C[i] * inv(k)
    return res.exp(limit).poly

def partition_function(n):
    res = FormalPowerSeries([0] * (n + 1))
    res[0] = 1
    for k in range(1, n+1):
        k1 = k * (3 * k + 1 )// 2
        k2 = k * (3 * k - 1) // 2
        if k2 > n:
            break
        if k1 <= n:
            res[k1] += 1 - (k & 1) * 2
        if k2 <= n:
            res[k2] += 1 - (k & 1) * 2
    return res.inv().poly

def bernoulli_number(n):
    n += 1
    Q = FormalPowerSeries([finv(i + 1) for i in range(n)]).inv(n - 1)
    res = [v * fac(i) % mod for i, v in enumerate(Q.poly)]
    return res
    
def stirling_first(n):
    P = []
    a = n
    while a:
        if a & 1:
            P.append(1)
        P.append(0)
        a >>= 1
    res = FormalPowerSeries([1])
    t = 0
    for x in P[::-1]:
        if x:
            res *= FormalPowerSeries([-t, 1])
            t += 1
        else:
            res *= res.taylor_shift(-t)
            t *= 2
    return res.poly

def stirling_second(n):
    F = FormalPowerSeries([0] * (n + 1))
    G = FormalPowerSeries([0] * (n + 1))
    for i in range(n + 1):
        F[i] = pow(i, n, mod) * finv(i)
        G[i] = (1 - (i & 1) * 2) * finv(i)
    return (F * G)[:n + 1].poly

def polynominal_interpolation(X, Y):
    n = len(X)
    size = 1 << (n - 1).bit_length()
    M = [FormalPowerSeries([1]) for _ in range(2 * size)]
    G = [0] * (2 * size)
    for i in range(n):
        M[size + i] = FormalPowerSeries([-X[i], 1])
    for i in range(size - 1, 0, -1):
        M[i] = M[2 * i] * M[2 * i + 1]
    G[1] = M[1].differentiate() % M[1]
    for i in range(2, size + n):
        G[i] = G[i >> 1] % M[i]
    for i in range(n):
        G[size + i] = FormalPowerSeries([Y[i] * inv_mod(G[size + i][0])])
    for i in range(size - 1, 0, -1):
        G[i] = G[2 * i] * M[2 * i + 1] + G[2 * i + 1] * M[2 * i]
    return G[1][:n]


class Mat2:
    def __init__(self, a00=FormalPowerSeries([1]), a01=FormalPowerSeries(),
                       a10=FormalPowerSeries(),    a11=FormalPowerSeries([1])):
        self.a00 = a00
        self.a01 = a01
        self.a10 = a10
        self.a11 = a11
    
    def __mul__(self, other):
        if type(other) == Mat2:
            A00 = self.a00 * other.a00 + self.a01 * other.a10
            A01 = self.a00 * other.a01 + self.a01 * other.a11
            A10 = self.a10 * other.a00 + self.a11 * other.a10
            A11 = self.a10 * other.a01 + self.a11 * other.a11
            A00.shrink()
            A01.shrink()
            A10.shrink()
            A11.shrink()
            return Mat2(A00, A01, A10, A11)
        else:
            b0 = self.a00 * other[0] + self.a01 * other[1]
            b1 = self.a10 * other[0] + self.a11 * other[1]
            b0.shrink()
            b1.shrink()
            return (b0, b1)
    
    def __imul__(self, other):
        A00 = self.a00 * other.a00 + self.a01 * other.a10
        A01 = self.a00 * other.a01 + self.a01 * other.a11
        A10 = self.a10 * other.a00 + self.a11 * other.a10
        A11 = self.a10 * other.a01 + self.a11 * other.a11
        A00.shrink()
        A01.shrink()
        A10.shrink()
        A11.shrink()
        self.a0 = A0
        self.a0 = A0
        self.a0 = A0
        self.a0 = A0

def _inner_naive_gcd(m, p):
    quo = p[0] // p[1]
    rem = p[0] - p[1] * quo
    b10 = m.a00 - m.a10 * quo
    b11 = m.a01 - m.a11 * quo
    rem.shrink()
    b10.shrink()
    b11.shrink()
    b10, m.a10 = m.a10, b10
    b11, m.a11 = m.a11, b11
    b10, m.a00 = m.a00, b10
    b11, m.a01 = m.a01, b11
    return (p[1], rem)

def _inner_half_gcd(p):
    n, m = len(p[0]), len(p[1])
    k = (n + 1) // 2
    if m <= k:
        return Mat2()
    m1 = _inner_half_gcd((p[0] >> k, p[1] >> k))
    p = m1 * p
    if len(p[1]) <= k:
        return m1
    p = _inner_naive_gcd(m1, p)
    if len(p[1]) <= k:
        return m1
    l = len(p[0]) - 1
    j = 2 * k - 1
    p = (p[0] >> j, p[1] >> j)
    return _inner_half_gcd(p) * m1

def _inner_poly_gcd(a, b):
    p = (a, b)
    p[0].shrink()
    p[1].shrink()
    n, m = len(p[0]), len(p[1])
    if n < m:
        mat = _inner_poly_gcd(p[1], p[0])
        mat.a00, mat.a01 = mat.a01, mat.a00
        mat.a10, mat.a11 = mat.a11, mat.a10
        return mat
    
    res = Mat2()
    while 1:
        m1 = _inner_half_gcd(p)
        p = m1 * p
        if len(p[1]) == 0:
            return m1 * res
        p = _inner_naive_gcd(m1, p)
        if len(p[1]) == 0:
            return m1 * res
        res = m1 * res

def poly_gcd(a, b):
    p = (a, b)
    m = _inner_poly_gcd(a, b)
    p = m * p
    if len(p[0]):
        coeff = inv_mod(p[0][-1])
        p[0] *= coeff
    return p[0]

def poly_inv(f, g):
    p = (f, g)
    m = _inner_poly_gcd(f, g)
    _gcd = (m * p)[0]
    if len(_gcd) != 1:
        return -1
    x = (FormalPowerSeries([1]), g)
    res = ((m * x)[0] % g) * inv_mod(_gcd[0])
    res.shrink()
    return res
 
  
import sys
input = sys.stdin.readline

d, k = map(int, input().split())
P = list(map(int, input().split()))
C = tuple(map(int, input().split()))
Q = [0] * (d + 1)
Q[0] = 1
for i, c in enumerate(C, 1):
    Q[i] = -c
P = convolution(P, Q)[:d]
ans = poly_coeff(Q, P, k)
print(ans)


# ----------------------------------------------------------------
# 任意modでやる(smallケースAC済み)
# 上と違ってこちらのコードを参考にしている
# https://judge.yosupo.jp/submission/36635

MOD1 = 167772161
MOD2 = 469762049
MOD3 = 754974721

sum_e1 = [65249968, 137365239, 35921276, 103665800, 89728614, 164955302, 108901219, 163950188, 113252399, 166581688, 59783366, 95476790, 130818126, 39440948, 65800545, 14559656, 3285286, 36462062, 164082627, 9320421, 66343657, 69024390, 38289678, 0, 0, 0, 0, 0, 0, 0]
sum_ie1 = [102522193, 71493608, 26998229, 133555027, 128975965, 16363816, 145463520, 130828795, 26375299, 18078794, 87407453, 28151929, 49401241, 112914531, 118959329, 68815302, 71865958, 21459372, 44393528, 43709352, 30681399, 153195333, 141748999, 0, 0, 0, 0, 0, 0, 0]
sum_e2 = [450151958, 26623616, 25192837, 305390008, 399060560, 78724413, 312251397, 151088193, 437503217, 339869829, 197503427, 460844482, 64795813, 392699793, 323591778, 435162849, 324666788, 397071166, 191521520, 39442863, 102932772, 52822010, 231589706, 155147527, 0, 0, 0, 0, 0, 0]
sum_ie2 = [19610091, 129701348, 104677229, 445839763, 375500824, 451642859, 145445927, 77724141, 367250623, 54456563, 257713867, 444918711, 335270416, 371371281, 307213086, 452878044, 243328637, 152011944, 315423951, 456185089, 218081060, 136058803, 203260256, 412215962, 0, 0, 0, 0, 0, 0]
sum_e3 = [323860177, 709730407, 436702940, 377572811, 498550177, 265767825, 100966039, 179671739, 669698534, 133401683, 473130419, 31725267, 490947959, 457689220, 238049902, 49087920, 531104465, 448493484, 262339740, 717535334, 230862726, 416349974, 0, 0, 0, 0, 0, 0, 0, 0]
sum_ie3 = [431114544, 205430076, 560644912, 287842920, 662221072, 3742006, 250769401, 512611432, 114808946, 480642746, 472385404, 152834416, 131937947, 932118, 246823069, 305783701, 453008707, 746618366, 510123862, 69538303, 659667489, 259138136, 0, 0, 0, 0, 0, 0, 0, 0]


def butterfly1(arr):
    n = len(arr)
    h = (n - 1).bit_length()
    for ph in range(1, h + 1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        now = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = arr[i + offset]
                r = arr[i + offset + p] * now
                arr[i + offset] = (l + r) % MOD1
                arr[i + offset + p] = (l - r) % MOD1
            now *= sum_e1[(~s & -~s).bit_length() - 1]
            now %= MOD1

def butterfly_inv1(arr):
    n = len(arr)
    h = (n - 1).bit_length()
    for ph in range(1, h + 1)[::-1]:
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        inow = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = arr[i + offset]
                r = arr[i + offset + p]
                arr[i + offset] = (l + r) % MOD1
                arr[i + offset + p] = (MOD1 + l - r) * inow % MOD1
            inow *= sum_ie1[(~s & -~s).bit_length() - 1]
            inow %= MOD1

def convolution1(a, b):
    n = len(a)
    m = len(b)
    if not n or not m: return []
    if min(n, m) <= 100:
        if n < m:
            n, m = m, n
            a, b = b, a
        res = [0] * (n + m - 1)
        for i in range(n):
            for j in range(m):
                res[i + j] += a[i] * b[j]
                res[i + j] %= MOD1
        return res
    z = 1 << (n + m - 2).bit_length()
    a += [0] * (z - n)
    b += [0] * (z - m)
    butterfly1(a)
    butterfly1(b)
    for i in range(z):
        a[i] *= b[i]
        a[i] %= MOD1
    butterfly_inv1(a)
    a = a[:n + m - 1]
    iz = pow(z, MOD1 - 2, MOD1)
    for i in range(n + m - 1):
        a[i] *= iz
        a[i] %= MOD1
    return a

def butterfly2(arr):
    n = len(arr)
    h = (n - 1).bit_length()
    for ph in range(1, h + 1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        now = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = arr[i + offset]
                r = arr[i + offset + p] * now
                arr[i + offset] = (l + r) % MOD2
                arr[i + offset + p] = (l - r) % MOD2
            now *= sum_e2[(~s & -~s).bit_length() - 1]
            now %= MOD2

def butterfly_inv2(arr):
    n = len(arr)
    h = (n - 1).bit_length()
    for ph in range(1, h + 1)[::-1]:
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        inow = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = arr[i + offset]
                r = arr[i + offset + p]
                arr[i + offset] = (l + r) % MOD2
                arr[i + offset + p] = (MOD2 + l - r) * inow % MOD2
            inow *= sum_ie2[(~s & -~s).bit_length() - 1]
            inow %= MOD2

def convolution2(a, b):
    n = len(a)
    m = len(b)
    if not n or not m: return []
    if min(n, m) <= 100:
        if n < m:
            n, m = m, n
            a, b = b, a
        res = [0] * (n + m - 1)
        for i in range(n):
            for j in range(m):
                res[i + j] += a[i] * b[j]
                res[i + j] %= MOD2
        return res
    z = 1 << (n + m - 2).bit_length()
    a += [0] * (z - n)
    b += [0] * (z - m)
    butterfly2(a)
    butterfly2(b)
    for i in range(z):
        a[i] *= b[i]
        a[i] %= MOD2
    butterfly_inv2(a)
    a = a[:n + m - 1]
    iz = pow(z, MOD2 - 2, MOD2)
    for i in range(n + m - 1):
        a[i] *= iz
        a[i] %= MOD2
    return a

def butterfly3(arr):
    n = len(arr)
    h = (n - 1).bit_length()
    for ph in range(1, h + 1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        now = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = arr[i + offset]
                r = arr[i + offset + p] * now
                arr[i + offset] = (l + r) % MOD3
                arr[i + offset + p] = (l - r) % MOD3
            now *= sum_e3[(~s & -~s).bit_length() - 1]
            now %= MOD3

def butterfly_inv3(arr):
    n = len(arr)
    h = (n - 1).bit_length()
    for ph in range(1, h + 1)[::-1]:
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        inow = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = arr[i + offset]
                r = arr[i + offset + p]
                arr[i + offset] = (l + r) % MOD3
                arr[i + offset + p] = (MOD3 + l - r) * inow % MOD3
            inow *= sum_ie3[(~s & -~s).bit_length() - 1]
            inow %= MOD3

def convolution3(a, b):
    n = len(a)
    m = len(b)
    if not n or not m: return []
    if min(n, m) <= 100:
        if n < m:
            n, m = m, n
            a, b = b, a
        res = [0] * (n + m - 1)
        for i in range(n):
            for j in range(m):
                res[i + j] += a[i] * b[j]
                res[i + j] %= MOD3
        return res
    z = 1 << (n + m - 2).bit_length()
    a += [0] * (z - n)
    b += [0] * (z - m)
    butterfly3(a)
    butterfly3(b)
    for i in range(z):
        a[i] *= b[i]
        a[i] %= MOD3
    butterfly_inv3(a)
    a = a[:n + m - 1]
    iz = pow(z, MOD3 - 2, MOD3)
    for i in range(n + m - 1):
        a[i] *= iz
        a[i] %= MOD3
    return a

def inv_gcd(a, b):
    a %= b
    if a == 0: return b, 0
    s = b
    t = a
    m0 = 0
    m1 = 1
    while t:
        u = s // t
        s -= t * u
        m0 -= m1 * u
        s, t = t, s
        m0, m1 = m1, m0
    if m0 < 0: m0 += b // s
    return s, m0

def crt(r, m):
    assert len(r) == len(m)
    n = len(r)
    r0 = 0
    m0 = 1
    for i in range(n):
        assert 1 <= m[i]
        r1 = r[i] % m[i]
        m1 = m[i]
        if m0 < m1:
            r0, r1 = r1, r0
            m0, m1 = m1, m0
        if m0 % m1 == 0:
            if r0 % m1 != r1: return 0, 0
            continue
        g, im = inv_gcd(m0, m1)
        u1 = m1 // g
        if (r1 - r0) % g: return 0, 0
        x = (r1 - r0) // g * im % u1
        r0 += x * m0
        m0 *= u1
        if (r0 < 0): r0 += m0
    return r0, m0

def convolution(a, b):
    n = len(a)
    m = len(b)
    c1 = convolution1(a.copy(), b.copy())[:n + m - 1]
    c2 = convolution2(a.copy(), b.copy())[:n + m - 1]
    c3 = convolution3(a.copy(), b.copy())[:n + m - 1]
    res = [0] * (n + m - 1)
    for i, v in enumerate(zip(c1, c2, c3)):
        cr, cm = crt(v, (MOD1, MOD2, MOD3))
        res[i] = cr % mod
    return res

def linear_recurrence(a, c, n):
    d = len(c)-1
    if n < d:
        return a[n]
    q = c.copy()
    p = convolution(a, c)[:d]
    while n:
        # print(p, q)
        r = [mod - v if i & 1 else v for i, v in enumerate(q)]
        p = convolution(p, r.copy())[(n & 1)::2]
        q = convolution(q, r)[::2]
        n >>= 1
    return p[0] % mod

import sys
input = sys.stdin.readline

mod = 998244353

D, K = map(int, input().split())

A = list(map(int, input().split()))
C = [1] + list(map(lambda x: mod - int(x), input().split()))

print(linear_recurrence(A, C, K))