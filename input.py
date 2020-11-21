# -*- coding: utf-8 -*-
# 整数の入力
a = int(input())

# スペース区切りの整数の入力
b,c = map(int,input().split())　#spilit()は間に挟む文字の指定。初期設定では空白1つ

# リスト入力
a = list(map(int, input().split()))

# 出力
print("{} {}".format(a+b+c, s))

# 縦に並んだ時
a = [input() for i in range(n)]

# 縦横に複数並んだ時。リストにせずfor内でそのまま使うのも手
T,X,Y = [],[],[]
for i in range(n):
    t, x, y = input().split()
    T.append(int(t))
    X.append(int(x))
    Y.append(int(y))
# 参考：一個ずつ使う場合はこのような書き方が一番早いとされている
import sys
# 入力を最後まで一気に読むことで高速化
M = map(int, sys.stdin.read().split())  
txy = zip(M, M, M)
for t, x, y in txy:
    print(t, x, y)

#２次元の文字入力（迷路など）
field = [list(input()) for i in range(n)]

#中いじりたいとき
p = list(map(lambda x: int(x) - 1, input().split()))

# 入力が多いときinputをrdで代用
import sys
rd = sys.stdin.readline

import sys
input = sys.stdin.readline

# おぎー流
import sys
import atexit
 
class Fastio:
    def __init__(self):
        self.ibuf = bytes()
        self.obuf = bytearray()
        self.pil = 0
        self.pir = 0
        self.buf = bytearray(20)
 
    def load(self):
        self.ibuf = self.ibuf[self.pil:]
        self.ibuf += sys.stdin.buffer.read(131072)
        self.pil = 0
        self.pir = len(self.ibuf)
 
    def flush(self):
        sys.stdout.buffer.write(self.obuf)
        self.obuf = bytearray()
 
    def fastin(self):
        if self.pir - self.pil < 32:
            self.load()
        minus = 0
        x = 0
        while self.ibuf[self.pil] < ord('-'):
            self.pil += 1
        if self.ibuf[self.pil] == ord('-'):
            minus = 1
            self.pil += 1
        while self.ibuf[self.pil] >= ord('0'):
            x = x * 10 + (self.ibuf[self.pil] & 15)
            self.pil += 1
        if minus:
            x = -x
        return x
 
    def fastout(self, x, end=b'\n'):
        i = 19
        if x == 0:
            self.buf[i] = 48
            i -= 1
        else:
            if x < 0:
                self.obuf.append(45)
                x = -x
            while x != 0:
                x, r = x // 10, x % 10
                self.buf[i] = 48 + r
                i -= 1
        self.obuf.extend(self.buf[i+1:])
        self.obuf.extend(end)
        if len(self.obuf) > 131072:
            self.flush()
 
fastio = Fastio()
rd = fastio.fastin # int(input())
wtn = fastio.fastout # print
atexit.register(fastio.flush)

N = rd()
a = [0] * N
for i in range(N):
    a[i] = rd()
for i in range(N-1, 0, -1):
    a[i] -= a[i-1]
p = 0
for i in range(1, N):
    p += max(0, a[i])
wtn((a[0] + p + 1) // 2)
Q = rd()
for _ in range(Q):
    l, r, x = rd(), rd(), rd()
    l -= 1
    if l != 0:
        p -= max(a[l], 0)
    a[l] += x
    if l != 0:
        p += max(a[l], 0)
    if r != N:
        p -= max(a[r], 0)
        a[r] -= x
        p += max(a[r], 0)
    wtn((a[0] + p + 1) // 2)