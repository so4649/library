# python3.8以降では逆元はpow(a,-1,mod)により計算できる
# pypyでもフェルマーの小定理よりpow(a,mod-2,mod)により計算できる
# 計算量はO(log a), O(log mod)

# コンビネーション(mod)の高速計算
def cmb(n, r):
    if r < 0 or n < 0 or n < r:
        return 0
    return g1[n] * g2[r] * g2[n-r] % mod
mod = 10**9+7 #出力の制限
N = 5*10**5 #Nの最大値
g1 = [0]*(N+1) #元テーブル(p(n,r))
g1[0] = g1[1] = 1
g2 = [0]*(N+1) #逆元テーブル
g2[0] = g2[1] = 1
inverse = [0]*(N+1) #逆元テーブル計算用テーブル
inverse[0],inverse[1] = 0,1
for i in range(2,N+1):
    g1[i] = (g1[i-1] * i) % mod
    inverse[i] = (-inverse[mod % i] * (mod//i)) % mod
    g2[i] = (g2[i-1] * inverse[i]) % mod

print(cmb(5,2))

# n = 10**9, r <= 10**5とかの時、O(r)で求められる
mod = 10**9+7
def cmb(x, y):
  ret = 1
  for i in range(1, y+1):
    ret = (ret * (x+1-i)) % mod
    ret = (ret * pow(i, mod-2, mod)) % mod
  return ret


def p(n, r):
    if n < 0 or r < 0 or n < r:
        return 0
    res = 1
        for i in range(r):
            res *= n - i
    return res
def c(n, r):
    if n < 0 or r < 0 or n < r:
        return 0
    r = min(r, n - r)
    res = 1
    for i in range(r):
        res = res * (n - i) // (i + 1)
    return res

#itertools
import itertools

# 順列
# permutations(list, n) で list から n 個選んで並べる
for i in itertools.permutations([0, 1, 2], 3):
    print(i)
# (0, 1, 2)
# (0, 2, 1)
# (1, 0, 2)
# (1, 2, 0)
# (2, 0, 1)
# (2, 1, 0)


# 組み合わせ
# combinations(list, n) で list から n 個選ぶ
for i in itertools.combinations([0, 1, 2], 2):
    print(i)
# (0, 1)
# (0, 2)
# (1, 2)