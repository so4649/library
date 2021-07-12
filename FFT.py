# 畳み込み O(nlogn)
# 元配列に対して破壊的なので注意

mod = 998244353
def primitive_root(m):
    if m == 2: return 1
    if m == 167772161: return 3
    if m == 469762049: return 3
    if m == 754974721: return 11
    if m == 998244353: return 3
    divs = [0] * 20
    divs[0] = 2
    cnt = 1
    x = (m - 1) // 2
    while x % 2 == 0: x //= 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            divs[cnt] = i
            cnt += 1
            while x % i == 0: x //= i
        i += 2
    if x > 1:
        divs[cnt] = x
        cnt += 1
    g = 2
    while True:
        for i in range(cnt):
            if pow(g, (m - 1) // divs[i], m) == 1: break
        else:
            return g
        g += 1
 
def build_ntt():
    root = primitive_root(mod)
    sum_e = [0] * 30
    sum_ie = [0] * 30
    es = [0] * 30
    ies = [0] * 30
    m = mod - 1
    cnt2 = (m & -m).bit_length() - 1
    e = pow(root, m >> cnt2, mod)
    ie = pow(e, mod - 2, mod)
    for i in range(cnt2 - 1)[::-1]:
        es[i] = e
        ies[i] = ie
        e *= e
        e %= mod
        ie *= ie
        ie %= mod
    now = 1
    inow = 1
    for i in range(cnt2 - 2):
        sum_e[i] = es[i] * now % mod
        sum_ie[i] = ies[i] * inow % mod
        now *= ies[i]
        inow *= es[i]
        now %= mod
        inow %= mod
    return sum_e, sum_ie
 
sum_e, sum_ie = build_ntt()
 
def butterfly(arr):
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
                arr[i + offset] = (l + r) % mod
                arr[i + offset + p] = (l - r) % mod
            now *= sum_e[(~s & -~s).bit_length() - 1]
            now %= mod
 
def butterfly_inv(arr):
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
                arr[i + offset] = (l + r) % mod
                arr[i + offset + p] = (mod + l - r) * inow % mod
            inow *= sum_ie[(~s & -~s).bit_length() - 1]
            inow %= mod
 
def convolution(a, b):
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
                res[i + j] %= mod
        return res
    z = 1 << (n + m - 2).bit_length()
    a += [0] * (z - n)
    b += [0] * (z - m)
    butterfly(a)
    butterfly(b)
    for i in range(z):
        a[i] *= b[i]
        a[i] %= mod
    butterfly_inv(a)
    a = a[:n + m - 1]
    iz = pow(z, mod - 2, mod)
    for i in range(n + m - 1):
        a[i] *= iz
        a[i] %= mod
    return a



n,m = map(int,input().split())
a = list(map(int,input().split()))
b = list(map(int,input().split()))
ans = convolution(a,b)
print(*ans)




# -----------------------------------------------------------------

# 任意mod畳み込み
# https://judge.yosupo.jp/submission/46587

import sys
input = sys.stdin.buffer.readline


M1, R1 = 167772161, 3
M2, R2 = 469762049, 3
M3, R3 = 1224736769, 3


def MOD1(): return M1
def ROOT1(): return R1
def MOD2(): return M2
def ROOT2(): return R2
def MOD3(): return M3
def ROOT3(): return R3


def _ntt(a, h, MOD, ROOT):
    roots = [pow(ROOT(), (MOD() - 1) >> i, MOD()) for i in range(h + 1)]
    for i in range(h):
        m = 1 << (h - i - 1)
        for j in range(1 << i):
            w = 1
            j *= 2 * m
            for k in range(m):
                a[j + k], a[j + k + m] = \
                    (a[j + k] + a[j + k + m]) % MOD(), \
                    (a[j + k] - a[j + k + m]) * w % MOD()
                w *= roots[h - i]
                w %= MOD()


def _intt(a, h, MOD, ROOT):
    roots = [pow(ROOT(), (MOD() - 1) >> i, MOD()) for i in range(h + 1)]
    iroots = [pow(r, MOD() - 2, MOD()) for r in roots]
    for i in range(h):
        m = 1 << i
        for j in range(1 << (h - i - 1)):
            w = 1
            j *= 2 * m
            for k in range(m):
                a[j + k], a[j + k + m] = \
                    (a[j + k] + a[j + k + m] * w) % MOD(), \
                    (a[j + k] - a[j + k + m] * w) % MOD()
                w *= iroots[i + 1]
                w %= MOD()
    inv = pow(1 << h, MOD() - 2, MOD())
    for i in range(1 << h):
        a[i] *= inv
        a[i] %= MOD()


def ntt_convolve(a, b, MOD, ROOT):
    n = 1 << (len(a) + len(b) - 1).bit_length()
    h = n.bit_length() - 1
    a = list(a) + [0] * (n - len(a))
    b = list(b) + [0] * (n - len(b))

    _ntt(a, h, MOD, ROOT), _ntt(b, h, MOD, ROOT)
    a = [va * vb % MOD() for va, vb in zip(a, b)]
    _intt(a, h, MOD, ROOT)
    return a


def arbitrary_mod_convolve(a, b, mod):
    x = ntt_convolve(a, b, MOD1, ROOT1)
    y = ntt_convolve(a, b, MOD2, ROOT2)
    z = ntt_convolve(a, b, MOD3, ROOT3)

    inv1_2 = pow(MOD1(), MOD2() - 2, MOD2())
    inv12_3 = pow(MOD1() * MOD2(), MOD3() - 2, MOD3())
    mod12 = MOD1() * MOD2() % mod
    
    res = [0] * len(x)
    for i in range(len(x)):
        v1 = (y[i] - x[i]) * inv1_2 % MOD2()
        v2 = (z[i] - (x[i] + MOD1() * v1) % MOD3()) * inv12_3 % MOD3()
        res[i] = (x[i] + MOD1() * v1 + mod12 * v2) % mod
    return res


n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
MOD = 10 ** 9 + 7


print(*arbitrary_mod_convolve(a, b, MOD)[:n + m - 1])



# 任意mod畳み込み別コード
# 以下のコードからautocorrelationを抜いている
# https://judge.yosupo.jp/submission/24282

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
        res[i] += cr
    return res

import sys
input = sys.stdin.buffer.readline

MOD = 1000000007

N, M = map(int, input().split())
A = list(map(int, input().split()))
B = list(map(int, input().split()))

C = convolution(A, B)
C = (c % MOD for c in C)

print(*C)