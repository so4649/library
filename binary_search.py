def binary_search(data, value):
    left = 0            # 探索する範囲の左端を設定
    right = len(data) - 1            # 探索する範囲の右端を設定
    while left <= right:
        mid = (left + right) // 2            # 探索する範囲の中央を計算
        if data[mid] == value:
            # 中央の値と一致した場合は位置を返す
            return mid
        elif data[mid] < value:
            # 中央の値より大きい場合は探索範囲の左を変える
            left = mid + 1
        else:
            # 中央の値より小さい場合は探索範囲の右を変える
            right = mid - 1
    return -1            # 見つからなかった場合


# https://qiita.com/ta7uw/items/d6d8f0ddb215c3677cd3
# 二分探索木
import bisect

A = [1, 2, 3, 3, 3, 4, 4, 6, 6, 6, 6]
print(A)
index = bisect.bisect_left(A, 3) # 2 最も左(前)の挿入箇所が返ってきている
A.insert(index, 3)
print(A) # [1, 2, 3, 3, 3, 3, 4, 4, 6, 6, 6, 6]

# 探索範囲を絞り込む
A = [1, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0]
index = bisect.bisect_left(A, 3, 0, 5)
print(index)# 2

A = [1, 2, 3, 3, 3, 4, 4, 6, 6, 6, 6]
index = bisect.bisect_right(A, 3) # 5



# floatの時の,条件Cを満たす二分探索（蟻本）
lb, ub = 0, 10**6
while ub - lb > 1:#for i in range(100)みたいな時もある
    mid = (lb + ub) / 2
    if C(mid):
        lb = mid
    else:
        ub = mid
print(lb)