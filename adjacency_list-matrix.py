#https://qiita.com/ell/items/2a327fe021fb7dafe07a

#入力 to 隣接リスト

#辺の重みがない場合
n, m = map(int, input().split())
graph = [[] for _ in range(n)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a-1].append(b-1)
    graph[b-1].append(a-1)  # 有向グラフなら消す
print(graph)  # [[2, 3, 5], ..., [1, 3, 4]]

#辺の重みがある場合
n, m = map(int, input().split())
graph = [[] for _ in range(n)]
for _ in range(n):
    u, v, w = map(int, input().split())
    graph[u-1].append([v-1, w])
    graph[v-1].append([u-1, w])  # 有向グラフなら消す
print(graph)  # [[2, 3], [3, 1], [5, 9]], ..., [...]]

#入力 to 隣接行列

#辺の重みがない場合。
n, m = map(int, input().split())
graph = [[0]*n for _ in range(n)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a-1][b-1] = 1
    graph[b-1][a-1] = 1  # 有向グラフなら消す
print(graph)  # [[0, 1, 1, 0, 1], ..., [1, 0, 1, 1, 0]]

#重み有りの場合。
n, m = map(int, input().split())
graph = [[0]*n for _ in range(n)]
for _ in range(m):
    u, v, w = map(int, input().split())
    graph[u-1][v-1] = w
    graph[v-1][u-1] = w  # 有向グラフなら消す
print(graph)  # [[0, 2, 3, 0, 1], ..., [2, 0, 3, 0, 0]


# 隣接リストを用いた例
n, m = map(int, input().split())
graph = [[] for _ in range(n)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a-1].append(b-1)
    graph[b-1].append(a-1)  # 有向グラフなら消す
print(graph)  # [[2, 3, 5], ..., [1, 3, 4]]

color = [0 for i in range(n)]

def dfs(x,c):
    color[x] = c
    for i in range(len(graph[x])):
        if color[graph[x][i]] == c:
            return False
        if color[graph[x][i]] == 0 and not dfs(graph[x][i], -c):
            return False
    return True