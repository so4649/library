# 計算量O(n)
# sとs[i:|s|−1]の最長共通接頭辞のリストを出力

def z_algo(s):
    n = len(s)
    A = [0]*n
    i = 1; j = 0
    A[0] = l = len(s)
    while i < l:
        while i+j < l and s[j] == s[i+j]:
            j += 1
        if not j:
            i += 1
            continue
        A[i] = j
        k = 1
        while l-i > k < j - A[k]:
            A[i+k] = A[k]
            k += 1
        i += k; j -= k
    return A