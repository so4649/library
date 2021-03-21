# 畳み込み O(nlogn)

mod = 998244353
def primitive_root(m):
    if m == 2: return 1
    if m == 167772161: return 3
    if m == 469762049: return 3
    if m == 754974721: return 11
    if m == 998244353: return 3
    divs = [0] * 20
    divs[0] = 2
    cnt = 1
    x = (m - 1) // 2
    while x % 2 == 0: x //= 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            divs[cnt] = i
            cnt += 1
            while x % i == 0: x //= i
        i += 2
    if x > 1:
        divs[cnt] = x
        cnt += 1
    g = 2
    while True:
        for i in range(cnt):
            if pow(g, (m - 1) // divs[i], m) == 1: break
        else:
            return g
        g += 1
 
def build_ntt():
    root = primitive_root(mod)
    sum_e = [0] * 30
    sum_ie = [0] * 30
    es = [0] * 30
    ies = [0] * 30
    m = mod - 1
    cnt2 = (m & -m).bit_length() - 1
    e = pow(root, m >> cnt2, mod)
    ie = pow(e, mod - 2, mod)
    for i in range(cnt2 - 1)[::-1]:
        es[i] = e
        ies[i] = ie
        e *= e
        e %= mod
        ie *= ie
        ie %= mod
    now = 1
    inow = 1
    for i in range(cnt2 - 2):
        sum_e[i] = es[i] * now % mod
        sum_ie[i] = ies[i] * inow % mod
        now *= ies[i]
        inow *= es[i]
        now %= mod
        inow %= mod
    return sum_e, sum_ie
 
sum_e, sum_ie = build_ntt()
 
def butterfly(arr):
    n = len(arr)
    h = (n - 1).bit_length()
    for ph in range(1, h + 1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        now = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = arr[i + offset]
                r = arr[i + offset + p] * now
                arr[i + offset] = (l + r) % mod
                arr[i + offset + p] = (l - r) % mod
            now *= sum_e[(~s & -~s).bit_length() - 1]
            now %= mod
 
def butterfly_inv(arr):
    n = len(arr)
    h = (n - 1).bit_length()
    for ph in range(1, h + 1)[::-1]:
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        inow = 1
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                l = arr[i + offset]
                r = arr[i + offset + p]
                arr[i + offset] = (l + r) % mod
                arr[i + offset + p] = (mod + l - r) * inow % mod
            inow *= sum_ie[(~s & -~s).bit_length() - 1]
            inow %= mod
 
def convolution(a, b):
    n = len(a)
    m = len(b)
    if not n or not m: return []
    if min(n, m) <= 100:
        if n < m:
            n, m = m, n
            a, b = b, a
        res = [0] * (n + m - 1)
        for i in range(n):
            for j in range(m):
                res[i + j] += a[i] * b[j]
                res[i + j] %= mod
        return res
    z = 1 << (n + m - 2).bit_length()
    a += [0] * (z - n)
    b += [0] * (z - m)
    butterfly(a)
    butterfly(b)
    for i in range(z):
        a[i] *= b[i]
        a[i] %= mod
    butterfly_inv(a)
    a = a[:n + m - 1]
    iz = pow(z, mod - 2, mod)
    for i in range(n + m - 1):
        a[i] *= iz
        a[i] %= mod
    return a



n,m = map(int,input().split())
a = list(map(int,input().split()))
b = list(map(int,input().split()))
ans = convolution(a,b)
print(*ans)

# -----------------------------------------------------------------
# 別コード
class Convolution:
  def __init__(self, mod: int):
    # self.mod = mod
    self.g = self.primitive_root(mod)
    self.first_butterfly = True
    self.first_butterfly_inv = True
    self.sum_e = [0] * 30
    self.sum_ie = [0] * 30
 
  # 原始根の取得
  def primitive_root(self, m: int):
    if (m == 2):
      return 1
    if (m == 167772161):
      return 3
    if (m == 469762049):
      return 3
    if (m == 754974721):
      return 11
    if (m == 998244353):
      return 3
    divs = [0] * 20
    divs[0] = 2
    cnt = 1
    x = (m-1)//2
    while(x % 2 == 0):
      x //= 2
    for i in range(3, x+1, 2):
      if(i**2 > x):
        break
      if(x % i == 0):
        divs[cnt] = i
        cnt += 1
        while(x % i == 0):
          x //= i
    if(x > 1):
      divs[cnt] = x
      cnt += 1
    g = 2
    while(True):
      ok = True
      for i in range(cnt):
        if(pow(g, (m-1)//divs[i], m) == 1):
          ok = False
          break
      if(ok):
        return g
      g += 1
 
    print('error')
    return 0
 
  def butterfly(self, a: list):
    # mod = self.mod
    n = len(a)
    h = (n-1).bit_length()
    if(self.first_butterfly):
      self.first_butterfly = False
      es = [0] * 30
      ies = [0] * 30
      mod_m = mod-1
      cnt2 = (mod_m & -mod_m).bit_length() - 1
      e = pow(self.g, mod_m >> cnt2, mod)
      ie = pow(e, mod-2, mod)
      for i in range(cnt2-2, -1, -1):
        es[i] = e
        ies[i] = ie
        e *= e
        e %= mod
        ie *= ie
        ie %= mod
      now = 1
      for i in range(cnt2-1):
        self.sum_e[i] = (es[i] * now) % mod
        now *= ies[i]
        now %= mod
    for ph in range(1, h+1):
      w = 1 << (ph-1)
      p = 1 << (h-ph)
      now = 1
      for s in range(w):
        offset = s << (h-ph+1)
        for i in range(p):
          l = a[i + offset]
          r = a[i + offset + p] * now
          a[i + offset] = (l+r) % mod
          a[i + offset + p] = (l-r) % mod
        now *= self.sum_e[(~s & -~s).bit_length() - 1]
        now %= mod
 
  def butterfly_inv(self, a: list):
    # mod = self.mod
    n = len(a)
    h = (n-1).bit_length()
    if(self.first_butterfly_inv):
      self.first_butterfly_inv = False
      es = [0] * 30
      ies = [0] * 30
      mod_m = mod-1
      cnt2 = (mod_m & -mod_m).bit_length() - 1
      e = pow(self.g, mod_m >> cnt2, mod)
      ie = pow(e, mod-2, mod)
      for i in range(cnt2-2, -1, -1):
        es[i] = e
        ies[i] = ie
        e *= e
        e %= mod
        ie *= ie
        ie %= mod
      now = 1
      for i in range(cnt2-1):
        self.sum_ie[i] = (ies[i] * now) % mod
        now *= es[i]
        now %= mod
    for ph in range(h, 0, -1):
      w = 1 << (ph-1)
      p = 1 << (h-ph)
      inow = 1
      for s in range(w):
        offset = s << (h-ph+1)
        for i in range(p):
          l = a[i + offset]
          r = a[i + offset + p]
          a[i + offset] = (l+r) % mod
          a[i + offset + p] = ((l - r) * inow) % mod
        inow *= self.sum_ie[(~s & -~s).bit_length() - 1]
        inow %= mod
 
  def convolution(self, a: list, b: list):
    # mod = self.mod
    n = len(a)
    m = len(b)
    if(n == 0) | (m == 0):
      return []
    if(min(n, m) <= 60):
      if(n < m):
        a, b = b, a
        n, m = m, n
      ans = [0] * (n+m-1)
      for i in range(n):
        for j in range(m):
          ans[i+j] += a[i] * b[j]
          ans[i+j] %= mod
      return ans
 
    z = 1 << (n+m-2).bit_length()
    a += [0] * (z-n)
    b += [0] * (z-m)
    self.butterfly(a)
    self.butterfly(b)
    for i in range(z):
      a[i] *= b[i]
      a[i] %= mod
    self.butterfly_inv(a)
    a = a[:(n+m-1)]
    iz = pow(z, mod-2, mod)
    for i in range(n+m-1):
      a[i] *= iz
      a[i] %= mod
    return a