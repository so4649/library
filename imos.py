# imos法毎回考えるのめんどいからまとめた
# 0-indexed
class Imos:
    def __init__(self,A):
        self.N = len(A)
        self.im = [0]*(self.N+1)
        self.im[0] = A[0]
        for i in range(1,self.N):
            self.im[i] = A[i]-A[i-1]
    
    # [l,r)
    def add(self,l,r,x):
        self.im[l] += x
        self.im[r] -= x
    
    # [l,r),O(n)
    def query(self,i):
        return sum(self.im[:i+1])

a = [1,3,5,2,3]
imos = Imos(a)
# a[2]~a[4]に2足す
imos.add(2,5,2)
print(imos.query(1)) # 3
print(imos.query(4)) # 5