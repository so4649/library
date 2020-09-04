# https://juppy.hatenablog.com/entry/2018/11/17/%E8%9F%BB%E6%9C%AC_python_Binary_Indexed_Tree_%E7%AB%B6%E6%8A%80%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0

n = 6
a = [1,2,3,4,5,6]

#A1 ... AnのBIT(1-indexed)
BIT = [0]*(n+1)

#A1 ~ Aiまでの和 O(logN)
def BIT_query(idx):
    res_sum = 0
    while idx > 0:
        res_sum += BIT[idx]
        idx -= idx&(-idx)
    return res_sum

#Ai += x O(logN)
def BIT_update(idx,x):
    while idx <= n:
        BIT[idx] += x
        idx += (idx&(-idx))
    return

for i,e in enumerate(a):
   BIT_update(i+1,e)

# すべて1-indexなので注意
#A1~A3の和 : 6
print(BIT_query(3))

#A3~A6の和 : 18
print(BIT_query(6)-BIT_query(2))


# クラスを使う場合(複数のBITを使う時など)
class BIT:
    def __init__(self,len_A):
        self.N = len_A + 10
        self.bit = [0]*(len_A+10)
        
    # sum(A0 ~ Ai)
    # O(log N)
    def query(self,i):
        res = 0
        idx = i+1
        while idx:
            res += self.bit[idx]
            idx -= idx&(-idx)
        return res

    # Ai += x
    # O(log N)
    def update(self,i,x):
        idx = i+1
        while idx < self.N:
            self.bit[idx] += x
            idx += idx&(-idx)
    
    # min_i satisfying {sum(A0 ~ Ai) >= w} (Ai >= 0)
    # O(log N)
    def lower_left(self,w):
        if (w < 0):
            return -1
        x = 0
        k = 1<<(self.N.bit_length()-1)
        while k > 0:
            if x+k < self.N and self.bit[x+k] < w:
                w -= self.bit[x+k]
                x += k
            k //= 2
        return x

n = 6
a = [1,2,3,4,5,6]

bit = BIT(n)
for i,e in enumerate(a):
   bit.update(i+1,e)

# すべて1-indexなので注意
#A1~A3の和 : 6
print(bit.query(3))

#A3~A6の和 : 18
print(bit.query(6)-bit.query(2))

bit.update(3,10)
print(bit.query(3))


# 区間に足し算を行う場合（蟻本3-3-3)


# 反転数 O(NlogN)
import bisect
def invNumCount(A):
    N = len(A)
    res = 0
    #A1 ... AnのBIT(1-indexed)
    BIT = [0]*(N+1)

    #A1 ~ Aiまでの和 O(logN)
    def BIT_query(idx):
        res_sum = 0
        while idx > 0:
            res_sum += BIT[idx]
            idx -= idx&(-idx)
        return res_sum

    #Ai += x O(logN)
    def BIT_update(idx,x):
        while idx <= N:
            BIT[idx] += x
            idx += idx&(-idx)
        return
    
    #Aが座圧されていないとき
    #"""
    B = sorted(A)
    for i,e in enumerate(A):
        A[i] = bisect.bisect_left(B,e)
    #"""

    for i,e in enumerate(A):
        res += i-BIT_query(e+1)
        BIT_update(e+1, 1)
    return res

a = [3,1,4,2]
print(invNumCount(a))


# https://tjkendev.github.io/procon-library/python/range_query/bit.html
# ２次元BIT
class BIT2:
    # H*W
    def __init__(self, h, w):
        self.w = w
        self.h = h
        self.data = [{} for i in range(h+1)]

    # O(logH*logW)
    def sum(self, i, j):
        s = 0
        data = self.data
        while i > 0:
            el = data[i]
            k = j
            while k > 0:
                s += el.get(k, 0)
                k -= k & -k
            i -= i & -i
        return s

    # O(logH*logW)
    def add(self, i, j, x):
        w = self.w; h = self.h
        data = self.data
        while i <= h:
            el = data[i]
            k = j
            while k <= w:
                el[k] = el.get(k, 0) + x
                k += k & -k
            i += i & -i

    # [x0, x1) x [y0, y1)
    def range_sum(self, x0, x1, y0, y1):
        return self.sum(x1, y1) - self.sum(x1, y0) - self.sum(x0, y1) + self.sum(x0, y0)