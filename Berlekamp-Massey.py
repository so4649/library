# ai = Σcja(i-j) (mod)となるcを求める


mod = 998244353

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


import sys
input = sys.stdin.readline

n = int(input())
A = tuple(map(int, input().split()))
ans = berlekamp_massey(A)
print(len(ans))
print(*ans)



# Aに対して第n項を求める
# ABC198F

def mult(A, B):
    n, m, l = len(A), len(B), len(B[0])
    ret = [[0]*l for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(l):
                ret[i][k] = (ret[i][k]+A[i][j]*B[j][k])
    return ret

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
    if n % 2: return mult(mpow(A, n-1), A)
    return mpow(mult(A, A), n//2)

x = int(input())
x -= 6
if x <= 14:
    ans = [1, 1, 3, 5, 10, 15, 29, 41, 68, 98, 147, 202, 291, 386, 528][x]
    print(ans)
    exit()

A = [[1,2,0,-2,-4,1,3,3,1,-4,-2,0,2,1,-1]]
for i in range(14):
    A.append([1 if j==i else 0 for j in range(15)])


a = [1, 1, 3, 5, 10, 15, 29, 41, 68, 98, 147, 202, 291, 386, 528][::-1]
B = mpow(A,x-14)

ans = sum(B[0][i]*a[i] for i in range(15)) % mod
print(ans)