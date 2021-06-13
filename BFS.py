# 最短距離でなく最長距離は151D参照

# 2-1-3
# (sx, sy) から (gx, gy) への最短距離を求める
from collections import deque

def bfs():
    d = [[-1] * w for i in range(h)]
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    for i in range(h):
        for j in range(w):
            if s[i][j] == "S":
                sx = i
                sy = j
            if s[i][j] == "G":
                gx = i
                gy = j

    que = deque([])
    que.append((sx, sy))
    d[sx][sy] = 0
    while que:
        p = que.popleft()
        if p[0] == gx and p[1] == gy:
            break
        for i in range(4):
            nx = p[0] + dx[i]
            ny = p[1] + dy[i]
            if 0 <= nx < h and 0 <= ny < w and s[nx][ny] != "#" and d[nx][ny] == -1:
                que.append((nx, ny))
                d[nx][ny] = d[p[0]][p[1]] + 1

    return d[gx][gy]

h, w = map(int, input().split())
s = [list(input()) for i in range(h)]

ans = bfs()
print(ans)


# 01BFSの例。ABC176D
# (sx, sy) から (gx, gy) への最短距離を求める
# 辿り着けないと -1
from collections import deque

def bfs():
    d = [[-1] * w for i in range(h)]
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    # 周辺25マス移動
    dd = []
    for i in range(-2,3):
        for j in range(-2,3):
            dd.append([i,j])

    que = deque([])
    que.append((sx, sy))
    d[sx][sy] = 0
    while que:
        p = que.popleft()
        if p[0] == gx and p[1] == gy:
            break
        for i in range(4):
            nx = p[0] + dx[i]
            ny = p[1] + dy[i]
            if 0 <= nx < h and 0 <= ny < w and s[nx][ny] == "." and (d[nx][ny] == -1 or d[nx][ny] > d[p[0]][p[1]]):
                que.appendleft((nx, ny))
                d[nx][ny] = d[p[0]][p[1]]
        for i in range(25):
            nx = p[0] + dd[i][0]
            ny = p[1] + dd[i][1]
            if 0 <= nx < h and 0 <= ny < w and s[nx][ny] == "." and d[nx][ny] == -1:
                que.append((nx, ny))
                d[nx][ny] = d[p[0]][p[1]]+1

    return d[gx][gy]

h, w = map(int, input().split())
sx,sy = map(lambda x:int(x)-1,input().split())
gx,gy = map(lambda x:int(x)-1,input().split())
s = [list(input()) for i in range(h)]

ans = bfs()
if ans == -1:
    print(-1)
else:
    print(ans)



# 迷路ではない場合
# 以下は0開始としている
from collections import deque

def bfs(N,edge,start=0):
    dist = [-1]*N
    que = deque([start])
    dist[start] = 0
    while que:
        v = que.popleft()
        d = dist[v]
        for w in edge[v]:
            if dist[w] > -1:
                continue
            dist[w] = d + 1
            que.append(w)
    return dist

# 親を残す場合（経路復元など）
def bfs(N,edge,start=0):
    dist = [-1]*N
    parent = [-1]*N
    que = deque([start])
    dist[start] = 0
    while que:
        v = que.popleft()
        d = dist[v]
        for w in edge[v]:
            if dist[w] > -1:
                continue
            dist[w] = d + 1
            parent[w] = v
            que.append(w)
    return dist,parent


# ワーシャルフロイド（BFSじゃないけどおまけ)
# k,i,jの順に回すことに注意

n,m = map(int,input().split())

INF = 10**15
edge = [[INF]*n for i in range(n)]
for i in range(n):
    edge[i][i] = 0

for i in range(m):
    a,b,t = map(int,input().split())
    edge[a-1][b-1] = t
    edge[b-1][a-1] = t

for k in range(n):
    for i in range(n):
        for j in range(n):
                edge[i][j] = min(edge[i][j], edge[i][k] + edge[k][j])