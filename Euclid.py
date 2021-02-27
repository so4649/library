# https://note.nkmk.me/python-gcd-lcm/

# 最小公約数
import math
print(math.gcd(2, 4))

# 最小公倍数
import math
def lcm(x, y):
    return x // math.gcd(x, y) * y

# ３つ以上の最大公約数
import math
from functools import reduce

def gcd(*numbers):
    return reduce(math.gcd, numbers)

print(gcd(*[27, 18, 9, 3]))
# 3

# ３つ以上の最小公倍数
import math
from functools import reduce

def lcm_base(x, y):
    return x // math.gcd(x, y) * y

def lcm(*numbers):
    return reduce(lcm_base, numbers, 1)

print(lcm(27, 18, 9, 3))
# 54

print(lcm(*[27, 9, 3]))
# 27



# 拡張ユークリッドの互除法
# 一次不定方程式ax+by=cが整数解をもつための必要十分条件はcがgcd(a,b)で割り切れることである。
# 以下はax+by=gcd(a,b)となるときのx,yを求める
def gcd_ext(a, b):
    x, y, lastx, lasty = 0, 1, 1, 0
    while b != 0:
        q = a // b
        a, b = b, a % b
        x, y, lastx, lasty = lastx - q * x, lasty - q * y, x, y
    return (lastx, lasty)



# 中国剰余定理
def extgcd(a, b):
    if b:
        d, y, x = extgcd(b, a % b)
        y -= (a // b) * x
        return d, x, y
    return a, 1, 0

# V = [(X_i, Y_i), ...]: X_i (mod Y_i)
# xが答え,dはmodのlcm(最小公倍数)
def remainder(V):
    x = 0; d = 1
    for X, Y in V:
        g, a, b = extgcd(d, Y)
        x, d = (Y*b*x + d*a*X) // g, d*(Y // g)
        x %= d
        
    # 条件をみたす答えが存在しなくても出してしまうので確かめる必要がある
    for X, Y in V:
        if x % Y != X:
            return -1

    return x, d

v = ((5,12),(9,16))
print(remainder(v))
v = ((3,14),(5,14))
print(remainder(v))