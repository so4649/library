# bit探索の型

# 0 から (2^n)-1 までループ
for bit in range(1 << n):
    for i in range(n):
        # bit に i 番目のフラグが立っているかどうか
        if bit & (1 << i):
            # フラグが立っているならば～
