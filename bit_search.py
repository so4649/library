# bit探索の型

# 0 から (2^n)-1 までループ
for bit in range(1 << n):
    for i in range(n):
        # bit に i 番目のフラグが立っているかどうか
        if bit & (1 << i):
            # フラグが立っているならば～



# p進数bit全探索
from itertools import product
def iter_p_adic(p, n):
    '''
    連続して増加するp進数をリストとして返す。nはリストの長さ
    return
    ----------
    所望のp進数リストを次々返してくれるiterator
    '''
    tmp = [range(1,p+1)] * n
    return product(*tmp)

for p in iter_p_adic(4, 3):
    print(p)