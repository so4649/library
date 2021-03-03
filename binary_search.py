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


# めぐる式二分探索
# f(x) = Trueとなるxの下限あるいは上限を求めるライブラリ
# 参考1：https://twitter.com/meguru_comp/status/697008509376835584
# 参考2：https://qiita.com/drken/items/97e37dd6143e33a64c8c
# 範囲を上に開な半開区間で持つことで+1,-1が不要になり余計なバグを生みづらくなる
# また、範囲を[l, r)でなく[ok, ng)あるいは[ng, ok)のように定義することで
# 上限・下限のいずれを求めたいときも、abs(ok - ng) > 1という同じループ条件で動作させることができる
def binary_search_func(ok, ng, f):
    while(abs(ok - ng) > 1):
        med = (ok + ng) // 2
        if f(med) == True:
            ok = med
        else:
            ng = med
    return ok



# floatの時の,条件Cを満たす二分探索（蟻本）
ok, ng = 0, 10**6
for i in range(100): # while (ng - ok) > 1:
    mid = (ok + ng) / 2
    if f(mid):
        ok = mid
    else:
        ng = mid
print(ok)



# 初めの頃使ってた値探索（しかし、setのinで十分なので不要か？）
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