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
    
    # 値を求める。O(n)
    def get(self,i):
        return sum(self.im[:i+1])

    # 最終的な配列を返す。O(n)
    def get_array(self):
        ruiseki = [0]*self.N
        ruiseki[0] = self.im[0]
        for i in range(1,self.N):
            ruiseki[i] = ruiseki[i-1]+self.im[i]
        return ruiseki

a = [1,3,5,2,3]
imos = Imos(a)
# a[2]~a[4]に2足す
imos.add(2,5,2)
print(imos.get(1)) # 3
print(imos.get(4)) # 5
print(imos.get_array()) # [1, 3, 7, 4, 5]