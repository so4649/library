import heapq
INF = 10**15
def dijkstra(N,start,edge):
    hq = [(0, start,)]
    dist = [INF] * N
    dist[start] = 0
    while hq:
        c, v = heapq.heappop(hq)
        if c > dist[v]:
            continue
        for d, u in edge[v]:
            tmp = d + dist[v]
            if tmp < dist[u]:
                dist[u] = tmp
                heapq.heappush(hq, (tmp, u))
    return dist

n,m = map(int,input().split())
edge = [[] for _ in range(n)]
for _ in range(m):
    a,b,t = map(int,input().split())
    a,b = a-1, b-1
    edge[a].append((t, b))
    edge[b].append((t, a)) # 有向グラフでは削除

d = dijkstra(n,0,edge)
print(d)



# 経路復元
# 前頂点の情報を持たせる
# yosupo judge:Shortest Path

import heapq
INF = 10**15
def dijkstra_root(N,start,edge):
    hq = [(0, start)]
    prev = [-1] * N
    dist = [INF] * N
    dist[start] = 0
    while hq:
        c, v = heapq.heappop(hq)
        if c > dist[v]:
            continue
        for d, u in edge[v]:
            tmp = d + dist[v]
            if tmp < dist[u]:
                dist[u] = tmp
                prev[u] = v
                heapq.heappush(hq, (tmp, u))
    return dist,prev


import sys
input = sys.stdin.readline

n,m,s,t = map(int,input().split())
edge = [[] for i in range(n)]
for i in range(m):
    a,b,c = map(int,input().split())
    edge[a].append((c, b))

dist,prev = dijkstra_root(n,s,edge)
if dist[t] == INF:
    print(-1)
    exit()

ans = [t]
while ans[-1] != s:
    ans.append(prev[ans[-1]])

print(dist[t],len(ans)-1)
for i in range(len(ans)-1):
    print(ans[-i-1],ans[-i-2])