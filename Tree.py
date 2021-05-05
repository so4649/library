from collections import deque

n = int(input())
edge = [[] for i in range(n)]
for i in range(n-1):
    x, y = map(int, input().split())
    edge[x-1].append(y-1)
    edge[y-1].append(x-1)
 
parent = [-1] * n
q = deque([0])
while q:
    i = q.popleft()
    for a in edge[i]:
        if a != parent[i]:
            parent[a] = i
            q.append(a)
print(parent)


# 最小共通祖先（ダブリング）
# ABC14D

from collections import deque

def bfs(N,edge,start=0):
    dist = [-1]*N
    que = deque([start])
    dist[start] = 0
    prv = [-1]*N
    while que:
        v = que.popleft()
        d = dist[v]
        for w in edge[v]:
            if dist[w] > -1:
                continue
            dist[w] = d + 1
            prv[w] = v
            que.append(w)
    return dist,prv

import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

n = int(input())
edge = [[] for i in range(n)]
for i in range(n-1):
    x,y = map(lambda x:int(x)-1,input().split())
    edge[x].append(y)
    edge[y].append(x)

LV = (n-1).bit_length()
def construct(prv):
    kprv = [prv]
    S = prv
    for k in range(LV):
        T = [-1]*n
        for i in range(n):
            if S[i] == -1:
                continue
            T[i] = S[S[i]]
        kprv.append(T)
        S = T
    return kprv

def lca(u, v, kprv, depth):
    dd = depth[v] - depth[u]
    if dd < 0:
        u, v = v, u
        dd = -dd

    # assert depth[u] <= depth[v]
    for k in range(LV+1):
        if dd & 1:
            v = kprv[k][v]
        dd >>= 1

    # assert depth[u] == depth[v]
    if u == v:
        return u

    for k in range(LV-1, -1, -1):
        pu = kprv[k][u]; pv = kprv[k][v]
        if pu != pv:
            u = pu; v = pv

    # assert kprv[0][u] == kprv[0][v]
    return kprv[0][u]

depth,prv = bfs(n,edge,0)
kprv = construct(prv)

q = int(input())
for i in range(q):
    a,b = map(lambda x:int(x)-1,input().split())
    u = lca(a,b,kprv,depth)
    ans = depth[a]+depth[b]-depth[u]*2+1
    print(ans)