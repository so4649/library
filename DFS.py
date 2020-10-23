#2-1-1
# i までで sum を作って、残り i 以降を調べる
def dfs(i, sum):
    # n 個決め終わったら、今までの和 sum が k と等しいかを返す
    if i == n:
        return sum == k
    # a[i] を使わない場合
    if dfs(i + 1, sum):
        return True
    # a[i] を使う場合
    if dfs(i + 1, sum + a[i]):
        return True
    # a[i] を使う使わないに拘らず k が作れないので False を返す
    return False

n, k = map(int, input().split())
a = list(map(int, input().split()))

if dfs(0, 0):
    print("Yes")
else:
    print("No")

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

#2-5-1
def dfs(x,c):
    color[x] = c
    for i in range(len(graph[x])):
        if color[graph[x][i]] == c:
            return False
        if color[graph[x][i]] == 0 and not dfs(graph[x][i], -c):
            return False
    return True
