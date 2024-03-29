# 座圧
a = [20,50,30,50]
sa = sorted(set(a)) # 元の数字に戻すときに使える
dic = {a:i for i,a in enumerate(sa)} # 座圧に変換する用
new_a = [dic[i] for i in a]

print(sa)
print(dic)
print(new_a)


# 累積和
# 累積和だけ1-indexedで持つと0-indexed区間和[l,r)がruiseki[r]-ruiseki[l]で求まる
ruiseki = [0]*(n+1)
for i in range(n):
    ruiseki[i+1] = ruiseki[i]+a[i]

# 2次元の場合
# 同様にruisekiだけ1-indexed
ruiseki = [[0]*(n+1) for i in range(n+1)]
for i in range(n):
    for j in range(n):
        ruiseki[i+1][j+1] = ruiseki[i+1][j]+ruiseki[i][j+1]-ruiseki[i][j]+a[i][j]
# 長方形の区間和を求める時 x:[lx,rx),y:[ly,ry)
t = ruiseki[rx][ry]-ruiseki[lx][ry]-ruiseki[rx][ly]+ruiseki[lx][ly]


# ダブリング
ld = d.bit_length()
kgo = [go]
S = go
for k in range(ld):
    T = [-1]*n
    for i in range(n):
        T[i] = S[S[i]]
    kgo.append(T)
    S = T


# powの事前計算
po = [[1]*(l+1) for i in range(17)]
po[0][0] = 0
for i in range(17):
    for j in range(1,l+1):
        po[i][j] = po[i][j-1]*i
        po[i][j] %= mod

# 早いpow
def fast_pow(x, k):
    res = 1
    while k:
        if k & 1:
            res = res * x % mod
        x = x * x % mod
        k >>= 1
    return res


# 10進数をn進数に変換(strで出力)
# なお、n進数を10進数にするのはint(str,n)でできる
def Base_p(num,p):
    if num == 0:
        return "0"
    res = []
    while num:
        res.append(str(num%p))
        num //= p
    return "".join(res[::-1])


# ソートされた2つの配列をあわせる
def merge(s, t):
    u = list()
    i = 0
    j = 0
    s.append(10 ** 9)
    t.append(10 ** 9)
    while i != len(s) - 1 or j != len(t) - 1:
        if s[i] < t[j]:
            u.append(s[i])
            i += 1
        else:
            u.append(t[j])
            j += 1
    return u


# xの立っているビット数をカウントする
# 64bit
def popcount(i):
    i = (i&0x5555555555555555) + ((i>>1)&0x5555555555555555)
    i = (i&0x3333333333333333) + ((i>>2)&0x3333333333333333)
    i = i + (i>>4)&0xF0F0F0F0F0F0F0F
    i = i + (i>>32)&0xFFFFFFFF
    return ((i * 0x1010101) & 0xFFFFFFFF) >> 24
# O(logx)だけどそこそこ早い
def popcount(x):
    return bin(x).count("1")


# 小数で誤差が出そうな問題
# https://docs.python.org/ja/3/library/decimal.html
# pypyではなくpythonで使う
from decimal import *
x,y,r = map(Decimal,input().split())


# 使えそうな関数

# for文を回す時に複数の変数を取るとき
for i,j in zip(a,b):

# 商と余り
syo,amari = divmod(10,3)

s = "abcdefgabcdefg"
# 開始位置を探索。ここではx = 3
x = s.find("def")


# ランダムケーステスト
# oj g/i -c "python a.py" --hack "python b.py" "python generate.py"