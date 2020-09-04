# 素数判定
import math
def is_prime(n):
    if n == 1: return False
    if n % 2 == 0 and n != 2:
        return False
    for k in range(2, int(math.sqrt(n)) + 1):
        if n % k == 0:
            return False
    return True

# print(is_prime(11))

# 約数列挙
import math
def make_divisors(n):
    divisors = []
    for i in range(1, int(math.sqrt(n))+1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n//i)

    divisors.sort()
    return divisors
# こっちでもいい
def make_divisors(n):
    lower_divisors , upper_divisors = [], []
    i = 1
    while i*i <= n:
        if n % i == 0:
            lower_divisors.append(i)
            if i != n // i:
                upper_divisors.append(n//i)
        i += 1
    return lower_divisors + upper_divisors[::-1]


# n以下の素数
#----エラトステネスの篩--------
def sieve(n):
    from math import sqrt

    is_prime = [1]*(n+1)
    for i in range(2, int(sqrt(n) + 1)):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = 0
                
    ps = [i for i in range(2,n+1) if is_prime[i]]
    return ps

print(sieve(20)) # [2, 3, 5, 7, 11, 13, 17, 19]


# エラトステネスの篩を用いた高速素因数分解O(logn)
# 素数テーブルを求める前処理O(nlogn)がある
# 1は{1}と出るので注意
import collections

def prime_factor_table(n):
    table = [0] * (n + 1)
    
    for i in range(2, n + 1):
        if table[i] == 0:
            for j in range(i + i, n + 1, i):
                table[j] = i
    
    return table
# ここではcounter型になっている
# key()やvalues()など使える
def prime_factor(n, prime_factor_table):
    prime_count = collections.Counter()
    
    while prime_factor_table[n] != 0:
        prime_count[prime_factor_table[n]] += 1
        n //= prime_factor_table[n]
    prime_count[n] += 1
    
    return prime_count

pft = prime_factor_table(100)
for i in range(1,101):
    print(prime_factor(i, pft))



# 素因数分解O(√n)
def pf(n):
    a = []
    while n % 2 == 0:
        a.append(2)
        n //= 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            a.append(f)
            n //= f
        else:
            f += 2
    if n != 1:
        a.append(n)
    return a

# print(pf(64))