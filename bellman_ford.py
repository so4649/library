# O(EV)
# 負閉路を含むパスがある終点は-INFにする
INF = 10**15
def bellman_ford(s):
    d = [INF]*n # 各頂点への最小コスト
    d[s] = 0

    ok = True
    for i in range(n):
        update = False # 更新が行われたか
        for x, y, z in g:
            if d[y] > d[x] + z:
                d[y] = d[x] + z
                update = True
        if not update:
            break
        # 負閉路が存在
        if i == n - 1:
            ok = False
    if ok:
        return d
    
    # 負閉路を含むパスがある終点の値を-INFにする
    for i in range(n):
        for x, y, z in g:
            if d[y] > d[x] + z:
                d[y] = -INF
    return d

n,m = [int(x) for x in input().split()]
g = []
for _ in range(m):
    x, y, z = [int(x) for x in input().split()] # 始点,終点,コスト
    g.append([x, y, z])
    g.append([y, x, z]) # 有向グラフでは削除
print(bellman_ford(0))