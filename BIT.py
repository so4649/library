# https://juppy.hatenablog.com/entry/2018/11/17/%E8%9F%BB%E6%9C%AC_python_Binary_Indexed_Tree_%E7%AB%B6%E6%8A%80%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0

# 一点加算、更新(0-indexed)
class BIT:
    def __init__(self,init):
        if type(init) == int:
            self.N = init+2
            self.bit = [0]*(init+3)
            self.num = [0]*(init+3)
        else:
            self.N = len(init)+2
            self.bit = [0]*(len(init)+3)
            self.num = [0]*(len(init)+3)
            for i in range(len(init)):
                self.add(i,init[i])
        
    # [A0,Ai]
    # O(log N)
    def query(self,i):
        res = 0
        idx = i+1
        while idx > 0:
            res += self.bit[idx]
            idx -= idx&(-idx)
        return res

    # [Ai,Aj)
    # if j == None return Ai
    def get(self,i,j=None):
        if j == None:
            return self.num[i]
        if j <= i:
            return 0
        return self.query(j-1)-self.query(i-1)

    # Ai += x
    # O(log N)
    def add(self,i,x):
        idx = i+1
        while idx < self.N:
            self.bit[idx] += x
            idx += idx&(-idx)
        self.num[i] += x

    # Ai = x
    # O(log N)
    def update(self,i,x):
        self.add(i,x-self.num[i])
        self.num[i] = x
    
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

bit = BIT(a)

# A0~A2の和 : 6
print(bit.query(2))

# A2~A5の和 : 18
print(bit.query(5)-bit.query(1))
print(bit.get(2,6))

# A2 : 3
print(bit.get(2))

# A3(=4)で初めて和が7以上(10)になる:3
print(bit.lower_left(7))

print(bit.query(-2))
# 0
print(bit.query(-1))
# 0

bit.add(2,10)
print(bit.query(2))
# 16

bit.update(2,10)
print(bit.query(2))
# 13


# 区間加算（蟻本3-3-3)
class rangeBIT:
    def __init__(self,init):
        self.N = init+2
        self.bit0 = [0]*(init+3)
        self.bit1 = [0]*(init+3)

    # 区間[l, r)に x を加算
    def _add(self,data,i,x):
        idx = i+1
        while idx < self.N:
            data[idx] += x
            idx += idx&(-idx)
    def add(self,l,r,x):
        self._add(self.bit0,l,-x*(l-1))
        self._add(self.bit0,r,x*(r-1))
        self._add(self.bit1,l,x)
        self._add(self.bit1,r,-x)

    # 区間[l, r)の和を求める
    def _query(self,data,i):
        res = 0
        idx = i+1
        while idx > 0:
            res += data[idx]
            idx -= idx&(-idx)
        return res
    def query(self,l,r):
        return self._query(self.bit1,r-1)*(r-1)+self._query(self.bit0,r-1)-self._query(self.bit1,l-1)*(l-1)-self._query(self.bit0,l-1)



# 複数のBITを使う時（中のリストが独立な２次元リストなど）
class Bit():
  def __init__(self, N):
    self.__N = N
    self.__arr = [[0] * 26 for _ in range(1 + N)]
    
  def add_(self, x, a, i):
    while(x < self.__N + 1):
      self.__arr[x][i] += a
      x += x & -x
      
  def sum_(self, x, i):
    res = 0
    while(x > 0):
      res += self.__arr[x][i]
      x -= x & -x
    return res
  
  def sub_sum_(self, x, y, i):
    return self.sum_(y, i) - self.sum_(x, i)


# 反転数 O(NlogN)
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
    # """
    sa = sorted(set(A))
    dic = {a:i for i,a in enumerate(sa)}
    A = [dic[i] for i in A]
    # """

    for i,e in enumerate(A):
        res += i-BIT_query(e+1)
        BIT_update(e+1, 1)
    return res

a = [101,53,200,53]
print(invNumCount(a)) # 3


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