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