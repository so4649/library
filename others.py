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
        ruiseki[i+1][j+1] = ruiseki[i+1][j]+ruiseki[i][j+1]+ruiseki[i][j]+a[i][j]
# 長方形の区間和を求める時 x:[lx,rx),y:[ly,ry)
t = ruiseki[rx][ry]-ruiseki[lx][ry]-ruiseki[rx][ly]+ruiseki[lx][ly]


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


# xの立っているビット数をカウントする関数
def popcount(x):
    '''xの立っているビット数をカウントする関数
    (xは64bit整数)'''

    # 2bitごとの組に分け、立っているビット数を2bitで表現する
    x = x - ((x >> 1) & 0x5555555555555555)

    # 4bit整数に 上位2bit + 下位2bit を計算した値を入れる
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)

    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f # 8bitごと
    x = x + (x >> 8) # 16bitごと
    x = x + (x >> 16) # 32bitごと
    x = x + (x >> 32) # 64bitごと = 全部の合計
    return x & 0x0000007f