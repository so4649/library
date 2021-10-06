# 全方位木DP

# https://neterukun1993.github.io/Library/Graph/Tree/rerooting.py

def rerooting(n, edges, unit, merge, addnode):
    tree = [[] for i in range(n)]
    idxs = [[] for i in range(n)]
    for u, v in edges:
        idxs[u].append(len(tree[v]))
        idxs[v].append(len(tree[u]))
        tree[u].append(v)
        tree[v].append(u)
    sub = [[unit] * len(tree[v]) for v in range(n)]
    noderes = [unit] * n

    # topological sort
    tp_order = []
    par = [-1] * n
    for root in range(n):
        if par[root] != -1:
            continue
        stack = [root]
        while stack:
            v = stack.pop()
            tp_order.append(v)
            for nxt_v in tree[v]:
                if nxt_v == par[v]:
                    continue
                par[nxt_v] = v
                stack.append(nxt_v)

    # tree DP
    for v in reversed(tp_order[1:]):
        res = unit
        par_idx = -1
        for idx, nxt_v in enumerate(tree[v]):
            if nxt_v == par[v]:
                par_idx = idx
                continue
            res = merge(res, sub[v][idx])
        if par_idx != -1:
            sub[par[v]][idxs[v][par_idx]] = addnode(res, v)

    # rerooting DP
    for v in tp_order:
        acc_back = [unit] * len(tree[v])
        for i in reversed(range(1, len(acc_back))):
            acc_back[i - 1] = merge(sub[v][i], acc_back[i])
        acc_front = unit
        for idx, nxt_v in enumerate(tree[v]):
            res = addnode(merge(acc_front, acc_back[idx]), v)
            sub[nxt_v][idxs[v][idx]] = res
            acc_front = merge(acc_front, sub[v][idx])
        noderes[v] = addnode(acc_front, v)
    return noderes

# 辺の重みを頂点情報に変換する時に使う
def edge_to_vertex(n, edges):
    m = len(edges)
    new_edges = []
    vals = [0] * (n + m)
    for i, (u, v, val) in enumerate(edges):
        new_edges.append((u, n + i))
        new_edges.append((n + i, v))
        vals[n + i] = val
    return new_edges, vals


# ABC220

n = int(input())
edges = [list(map(lambda x:int(x)-1,input().split())) for i in range(n-1)]

# (距離合計、部分木の大きさ)
unit = (0,0)

# a,b:子の情報
def merge(a,b):
    return (a[0]+b[0],a[1]+b[1])

# a:子のmerge情報　x:頂点の情報
def addnode(a,x):
    return (a[0]+a[1],a[1]+1)

ans = rerooting(n,edges,unit,merge,addnode)
print(*[i[0] for i in ans])