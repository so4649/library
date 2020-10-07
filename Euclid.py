# https://note.nkmk.me/python-gcd-lcm/

# 最小公約数
import math
print(math.gcd(a, b))
# 2

# 最小公倍数
import math
def lcm(x, y):
    return x // math.gcd(x, y) * y

print(lcm(a, b))
# 12

# ３つ以上の最大公約数
import math
from functools import reduce

def gcd(*numbers):
    return reduce(math.gcd, numbers)

print(gcd(*[27, 18, 9, 3]))
# 3

# ３つ以上の最小公倍数
import math
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