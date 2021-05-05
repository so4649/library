# 最短距離でなく最長距離は151D参照

# 2-1-3
from collections import deque

# (sx, sy) から (gx, gy) への最短距離を求める
# 辿り着けないと -1
def bfs():
    # すべての点を -1 で初期化
    d = [[-1] * m for i in range(n)]
    # 移動4方向のベクトル
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    for i in range(n):
        for j in range(m):
            # スタートとゴールの座標を探す
            if maze[i][j] == "S":
                sx = i
                sy = j
            if maze[i][j] == "G":
                gx = i
                gy = j

    # スタート地点をキューに入れ、その点の距離を0にする
    que = deque([])
    que.append((sx, sy))
    d[sx][sy] = 0
    # キューが空になるまでループ
    while que:
        # キューの先頭を取り出す
        p = que.popleft()
        # 取り出してきた状態がゴールなら探索をやめる
        if p[0] == gx and p[1] == gy:
            break
        # 移動4方向をループ
        for i in range(4):
            # 移動した後の点を (nx, ny) とする
            nx = p[0] + dx[i]
            ny = p[1] + dy[i]
            # 移動が可能かの判定とすでに訪れたことがあるかの判定
            # d[nx][ny] != -1 なら訪れたことがある
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] != "#" and d[nx][ny] == -1:
                # 移動できるならキューに入れ、その点の距離を p からの距離 +1 で確定する
                que.append((nx, ny))
                d[nx][ny] = d[p[0]][p[1]] + 1

    return d[gx][gy]

n, m = map(int, input().split())
maze = [list(input()) for i in range(n)]

print(bfs())


# 01BFSの例。ABC176D
from collections import deque

# (sx, sy) から (gx, gy) への最短距離を求める
# 辿り着けないと -1
def bfs():
    # すべての点を -1 で初期化
    d = [[-1] * m for i in range(n)]
    # 移動4方向のベクトル
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    sx = c[0]
    sy = c[1]
    gx = g[0]
    gy = g[1]

    # 周辺25マス移動
    dd = []
    for i in range(-2,3):
        for j in range(-2,3):
            dd.append([i,j])

    # スタート地点をキューに入れ、その点の距離を0にする
    que = deque([])
    que.append((sx, sy))
    d[sx][sy] = 0
    # キューが空になるまでループ
    while que:
        # キューの先頭を取り出す
        p = que.popleft()
        # 取り出してきた状態がゴールなら探索をやめる
        if p[0] == gx and p[1] == gy:
            break
        # 移動4方向をループ
        for i in range(4):
            # 移動した後の点を (nx, ny) とする
            nx = p[0] + dx[i]
            ny = p[1] + dy[i]
            # 移動が可能かの判定とすでに訪れたことがあるかの判定
            # d[nx][ny] != -1 なら訪れたことがある
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == "." and d[nx][ny] > d[p[0]][p[1]]:
                # 移動できるならキューに入れ、その点の距離を p からの距離 +1 で確定する
                que.appendleft((nx, ny))
                d[nx][ny] = d[p[0]][p[1]]
        for i in range(25):
            # 移動した後の点を (nx, ny) とする
            nx = p[0] + dd[i][0]
            ny = p[1] + dd[i][1]
            # 移動が可能かの判定とすでに訪れたことがあるかの判定
            # d[nx][ny] != -1 なら訪れたことがある
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == "." and d[nx][ny] == -1:
                que.append((nx, ny))
                d[nx][ny] = d[p[0]][p[1]]+1

    return d[gx][gy]

n, m = map(int, input().split())
c = list(map(lambda x:int(x)-1,input().split()))
g = list(map(lambda x:int(x)-1,input().split()))
maze = [list(input()) for i in range(n)]

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