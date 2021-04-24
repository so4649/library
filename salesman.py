# https://qiita.com/merry1221/items/23a4204aa837122780d0
# 非再帰
v, e = map(int, input().split())

INF = 10**15
cost = [[INF]*v for _ in range(v)]

for i in range(e):
    s, t, d = map(int, input().split())
    cost[s][t] = d

#Dpは全体集合の部分集合Sについて最後がvであるという制約の下で順序を最適化したときのSの中での最小コスト
dp = [[INF]*v for _ in range(1<<v)]
dp[0][0] = 0

#集合（訪れたか訪れていないかを表す二進数）
for x in range(1<<v):
    #最後に訪れたノード
    for y in range(v):
        #最後に訪れた以外のノード
        for z in range(v):
            #1.すでに訪れたかどうか 2.最後に訪れたノードではないか 3. yとzはそもそもつながっているのか
            if x & (1<<y) and y != z and cost[z][y] < 10**6:
                dp[x][y] = min(dp[x][y], dp[x^(1<<y)][z]+cost[z][y])

if dp[-1][0] > 10**6:
    print(-1)
else:
    print(dp[-1][0])


# 0スタート時にまた0に戻ってくる解の関数化
# 無理な場合INFで返る
INF = 10**15
cost = [[INF]*k for _ in range(k)]
for i in range(e):
    s, t, d = map(int, input().split())
    cost[s][t] = d

def salesman():
    # dp[S][v]:部分集合S、最後に訪れた点がvであるときのコスト
    dp = [[INF]*k for _ in range(1<<k)]
    # 開始点
    dp[0][0] = 0

    # 集合
    for x in range(1<<k):
        # 最後に訪れた点
        for y in range(k):
            # 次に行く点
            for z in range(k):
                # 1.yがxに含まれるか 2.最後に訪れた点以外 3.辺があるか
                if x & (1<<y) and y != z and cost[z][y] < INF:
                    dp[x][y] = min(dp[x][y], dp[x^(1<<y)][z]+cost[z][y])

    return dp[-1][0]



# https://kakedashi-engineer.appspot.com/2020/05/21/dpl2a/
V, E = map(int, input().split())
INF = 10**15
cost = [[INF]*V for _ in range(V)] # 重み
for e in range(E):
    s, t, d = map(int,input().split())
    cost[s][t] = d

dp = [[-1] * V for _ in range(1<<V)] # dp[S][v]

def dfs(S, v, dp):
    if dp[S][v] != -1: # 訪問済みならメモを返す
        return dp[S][v]
    if S==(1<<V)-1 and v==0: # 全ての頂点を訪れて頂点0に戻ってきた
        return 0 # もう動く必要はない

    res = INF
    for u in range(V):
        if S>>u & 1 == 0: # 未訪問かどうか
            res = min(res, dfs(S|1<<u, u, dp)+cost[v][u])
    dp[S][v] = res
    return res

ans = dfs(0, 0, dp) # 頂点0からスタートする。ただし頂点0は未訪問とする
if ans == INF:
    print(-1)
else:
    print (ans)