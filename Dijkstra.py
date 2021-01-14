# https://nashidos.hatenablog.com/entry/2020/04/07/100508

import heapq
INF = 10**15
def dijkstra(N,s):
    hq = [(0, s)]
    cost = [INF] * N
    cost[s] = 0
    while hq:
        c, v = heapq.heappop(hq)
        if c > cost[v]:
            continue
        for d, u in edge[v]:
            tmp = d + cost[v]
            if tmp < cost[u]:
                cost[u] = tmp
                heapq.heappush(hq, (tmp, u))
    return cost

n,m = map(int,input().split())
edge = [[] for _ in range(n)]
for _ in range(m):
    a,b,t = map(int,input().split())
    a,b = a-1, b-1
    edge[a].append((t, b))
    edge[b].append((t, a)) # 有向グラフでは削除

d = dijkstra(0)
print([dijkstra(i) for i in range(n)])

# 経路が必要な時はhttps://qiita.com/shizuma/items/e08a76ab26073b21c207


# ABC176D
import heapq

def dijkstra(s):
    hq = [(0, s)]
    heapq.heapify(hq) # リストを優先度付きキューに変換
    cost = [float('inf')] * (h*w) # 行ったことのないところはinf
    cost[s] = 0 # 開始地点は0
    while hq:
        c, v = heapq.heappop(hq)
        if c > cost[v]: # コストが現在のコストよりも高ければスルー
            continue
        for d, u in e[v]:
            tmp = d + cost[v]
            if tmp < cost[u]:
                cost[u] = tmp
                heapq.heappush(hq, (tmp, u))
    return cost

h,w = map(int,input().split())
c = list(map(int,input().split()))
d = list(map(int,input().split()))
maze = [list(input()) for i in range(h)]
# eのインデックスはi*w+j
e = [[] for _ in range(h*w)]
for i in range(h):
    for j in range(w):
        if j<w-1 and maze[i][j] == "." and maze[i][j+1] == ".":
            e[i*w+j].append((0, i*w+j+1))
            e[i*w+j+1].append((0, i*w+j)) # 有向グラフでは削除
        if i<h-1 and maze[i][j] == "." and maze[i+1][j] == ".":
            e[i*w+j].append((0, (i+1)*w+j))
            e[(i+1)*w+j].append((0, i*w+j)) # 有向グラフでは削除
        for x in range(-2,3):
            for y in range(-2,3):
                if 0<=i+x<h and 0<=j+y<w and maze[i+x][j+y] == ".":
                    e[i*w+j].append((1, (i+x)*w+j+y))

# print(dijkstra(1))
ans = dijkstra((c[0]-1)*w+(c[1]-1))[(d[0]-1)*w+(d[1]-1)]
if ans == float("inf"):
    print(-1)
    exit()
print(ans)