# 最短距離でなく最長距離は151D参照

# 2-1-3
from collections import deque

# (sx, sy) から (gx, gy) への最短距離を求める
# 辿り着けないと INF
def bfs():
    # すべての点を INF で初期化
    d = [[float("inf")] * m for i in range(n)]
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
            # d[nx][ny] != INF なら訪れたことがある
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] != "#" and d[nx][ny] == float("inf"):
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
# 辿り着けないと INF
def bfs():
    # すべての点を INF で初期化
    d = [[float("inf")] * m for i in range(n)]
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
            # d[nx][ny] != INF なら訪れたことがある
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == "." and d[nx][ny] > d[p[0]][p[1]]:
                # 移動できるならキューに入れ、その点の距離を p からの距離 +1 で確定する
                que.appendleft((nx, ny))
                d[nx][ny] = d[p[0]][p[1]]
        for i in range(25):
            # 移動した後の点を (nx, ny) とする
            nx = p[0] + dd[i][0]
            ny = p[1] + dd[i][1]
            # 移動が可能かの判定とすでに訪れたことがあるかの判定
            # d[nx][ny] != INF なら訪れたことがある
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == "." and d[nx][ny] == float("inf"):
                que.append((nx, ny))
                d[nx][ny] = d[p[0]][p[1]]+1

    return d[gx][gy]

n, m = map(int, input().split())
c = list(map(lambda x:int(x)-1,input().split()))
g = list(map(lambda x:int(x)-1,input().split()))
maze = [list(input()) for i in range(n)]

ans = bfs()
if ans == float("inf"):
    print(-1)
else:
    print(ans)


# 迷路ではない場合
# 以下は0開始としている
from collections import deque
dist = [-1]*N
que = deque([0])
dist[0] = 0
while que:
    v = que.popleft()
    d = dist[v]
    for w in G[v]:
        if dist[w] > -1:
            continue
        dist[w] = d + 1
        que.append(w)


# ワーシャルフロイド（BFSじゃないけどおまけ)
# costの初期値はinf
for i in range(V):
    for j in range(V):
        for k in range(V):
                cost[i][j] = min(cost[i][j], cost[i][k] + cost[k][j])