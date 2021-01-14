# 座圧
a = [20,50,30,50]
sa = sorted(set(a)) # 元の数字に戻すときに使える
dic = {a:i for i,a in enumerate(sa)} # 座圧に変換する用
new_a = [dic[i] for i in a]

print(sa)
print(dic)
print(new_a)

def suffix_array(S):
    assert S[-1] == '$'
    return _sa_is(list(map(ord, S)))

print(suffix_array("abcd$"))


# ソートされた2つの配列をあわせる
def merge(s, t):
  u = list()
  i = 0
  j = 0
  s.append(10 ** 9)
  t.append(10 ** 9)
  while i != len(s) - 1 or j != len(t) - 1:
    if s[i] < t[j]:
      u.append(s[i])
      i += 1
    else:
      u.append(t[j])
      j += 1
  return u