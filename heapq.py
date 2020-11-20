import heapq  # heapqライブラリのimport

a = [1, 6, 8, 0, -1]
heapq.heapify(a)  # リストを優先度付きキューへ
print(a)
# 出力: [-1, 0, 8, 1, 6] (優先度付きキューとなった a)

print(heapq.heappop(a))  # 最小値の取り出し
# 出力: -1 (a の最小値)
print(a)
# 出力: [0, 1, 8, 6] (最小値を取り出した後の a)

heapq.heappush(a, -2)  # 要素の挿入
print(a)
# 出力: [-2, 0, 1, 8, 6]  (-2 を挿入後の a)

#最大値
import heapq
a = [1, 6, 8, 0, -1]
a = list(map(lambda x: x*(-1), a))  # 各要素を-1倍
print(a)

heapq.heapify(a)
print(heapq.heappop(a)*(-1))  # 最大値の取り出し
print(a)


#最大値の場合に便利
import heapq
class Heapq:
    def __init__(self, arr, desc=False):
        if desc:
            arr = [-a for a in arr]
        self.sign = -1 if desc else 1
        self.hq = arr
        heapq.heapify(self.hq)
 
    def pop(self):
        return heapq.heappop(self.hq) * self.sign
 
    def push(self, a):
        heapq.heappush(self.hq, a * self.sign)
 
    def top(self):
        return self.hq[0] * self.sign

#使い方
#まず上のコードをコピペする。ドーン。

#初期化
#q = Heapq(arr, desc) のように書けばいいです

#第1引数 arr は初期化に使う配列です 空っぽから始める場合は []でいいです
#第2引数 desc は大きい順に取り出すなら True、小さい順ならFalse です。Falseは省略可です。
#pop()
#q.pop() のようにすると値が返ります
#一番小さいの or 一番大きいのを集合から取り出します。
#初期化時 desc=Trueを指定していたなら大きい方が出てきます。
#取り出された要素は集合から消えます。

#push()
#q.push(a) のようにすると集合に aを追加します

#top()
#q.top() のようにすると値が返ります
#一番小さいの or 一番大きいのを参照できます
#初期化時 desc=Trueを指定していたなら大きい方が出てきます。
#pop()に似てますが、参照するだけで、集合から値が消えることはありません。
#O(1)でめっちゃ速いです


# https://socha77.hatenablog.com/entry/2020/06/17/012842
# 遅延ヒープ
from collections import defaultdict
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