#最大値の場合にも便利
import heapq
class Heapq:
    def __init__(self, arr, desc=False):
        if desc:
            arr = [-a for a in arr]
        self.sign = -1 if desc else 1
        self.hq = arr
        self.len = len(arr)
        heapq.heapify(self.hq)

    def __len__(self):
        return self.len
 
    def pop(self):
        self.len -= 1
        return heapq.heappop(self.hq) * self.sign
 
    def push(self, a):
        self.len += 1
        heapq.heappush(self.hq, a * self.sign)
 
    def top(self):
        return self.hq[0] * self.sign

a = [1,2,3]
hq = Heapq(a)
print(len(hq))
hq.push(0)
print(hq.top(),len(hq))

# https://socha77.hatenablog.com/entry/2020/06/17/012842
# 遅延ヒープ
from collections import defaultdict, deque
import heapq

class LazyHeap():
    def __init__(self, init_arr=[]):
        self.heap = []
        self.lazy = defaultdict(int)
        self.len = 0
        for init_element in init_arr:
            heapq.heappush(self.heap, init_element)
            self.len += 1
 
    def __len__(self):
        return self.len
 
    def push(self, k):
        heapq.heappush(self.heap, k)
        self.len += 1
 
    def pop(self):
        self._clear()
        return heapq.heappop(self.heap)
        
    def top(self):
        self._clear()
        return self.heap[0]
 
    def _clear(self):
        while True:
            cand = self.heap[0]
            if cand in self.lazy and self.lazy[cand] > 0:
                heapq.heappop(self.heap)
                self.lazy[cand] -= 1
 
            else:
                return
 
    def remove(self, k):
        self.lazy[k] += 1
        self.len -= 1

a = [1, 6, 8, 0, -1]
q = LazyHeap(a)
q.remove(-1)
print(q.top())
q.pop()
print(q.top())


# ランダムアクセス、挿入がO(1)のdeque
# https://prd-xxx.hateblo.jp/entry/2020/02/07/114818

class Deque:
    def __init__(self, src_arr=[], max_size=300000):
        self.N = max(max_size, len(src_arr)) + 1
        self.buf = list(src_arr) + [None] * (self.N - len(src_arr))
        self.head = 0
        self.tail = len(src_arr)
    def __index(self, i):
        l = len(self)
        if not -l <= i < l: raise IndexError('index out of range: ' + str(i))
        if i < 0:
            i += l
        return (self.head + i) % self.N
    def __extend(self):
        ex = self.N - 1
        self.buf[self.tail+1 : self.tail+1] = [None] * ex
        self.N = len(self.buf)
        if self.head > 0:
            self.head += ex
    def is_full(self):
        return len(self) >= self.N - 1
    def is_empty(self):
        return len(self) == 0
    def append(self, x):
        if self.is_full(): self.__extend()
        self.buf[self.tail] = x
        self.tail += 1
        self.tail %= self.N
    def appendleft(self, x):
        if self.is_full(): self.__extend()
        self.buf[(self.head - 1) % self.N] = x
        self.head -= 1
        self.head %= self.N
    def pop(self):
        if self.is_empty(): raise IndexError('pop() when buffer is empty')
        ret = self.buf[(self.tail - 1) % self.N]
        self.tail -= 1
        self.tail %= self.N
        return ret
    def popleft(self):
        if self.is_empty(): raise IndexError('popleft() when buffer is empty')
        ret = self.buf[self.head]
        self.head += 1
        self.head %= self.N
        return ret
    def __len__(self):
        return (self.tail - self.head) % self.N
    def __getitem__(self, key):
        return self.buf[self.__index(key)]
    def __setitem__(self, key, value):
        self.buf[self.__index(key)] = value
    def __str__(self):
        return 'Deque({0})'.format(str(list(self)))