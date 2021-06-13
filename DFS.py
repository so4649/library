#2-1-2
# 現在位置 (x, y)
def dfs(x, y):
    # 今いるところを . に置き換える
    field[x][y] = "."
    # 移動する8方向をループ
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            # x, y 方向それぞれに dx, dy 移動した場所を (nx, ny) とする
            nx = x + dx
            ny = y + dy
            # nx と ny が庭の範囲内かどうかと field[nx][ny] が水溜りかどうかを判定
            if 0 <= nx and nx < n and 0 <= ny and ny < m and field[nx][ny] == "W":
                dfs(nx, ny)

n, m = map(int, input().split())
field = [list(input()) for i in range(n)]

res = 0
for i in range(n):
    for j in range(m):
        if field[i][j] == "W":
            # Wが残っているならそこから dfs をはじめる
            dfs(i, j)
            res += 1
print(res)

# 木上のDFS
# ここでは部分木の大きさを求めるDFS
def dfs(i,parent):
    global ans

    res = 1
    for j in edge[i]:
        if j == parent:
            continue
        res += dfs(j,i)

    return res