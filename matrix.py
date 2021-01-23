def mult(A, B):
    n, m, l = len(A), len(B), len(B[0])
    ret = [[0]*l for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(l):
                ret[i][k] = (ret[i][k]+A[i][j]*B[j][k])
    return ret

mod = 10**9+7
def mmult(A, B):
    global mod
    n, m, l = len(A), len(B), len(B[0])
    ret = [[0]*l for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(l):
                ret[i][k] = (ret[i][k]+A[i][j]*B[j][k])%mod
    return ret
    
def mpow(A, n):
    if n == 0: return [[1 if i==j else 0 for j in range(len(A))] for i in range(len(A))]
    if n % 2: return mmult(mpow(A, n-1), A)
    return mpow(mmult(A, A), n//2)