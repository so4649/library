# V: 頂点数
# edge[i] = [w, ...]:有向グラフ上の頂点vから到達できる頂点w

from collections import deque

def Topological_sort(V,edge):
    # 入次数
    indegree = [0]*V
    for e in edge:
        for i in e:
            indegree[i] += 1

    topo = list(i for i in range(V) if indegree[i]==0)
    q = deque(topo)
    used = [0]*V

    while q:
        i = q.popleft()
        for v in edge[i]:
            indegree[v] -= 1
            if indegree[v]==0:
                q.append(v)
                topo.append(v)
    return topo

print(Topological_sort(6,[[1,3],[3],[3,4],[],[5],[]]))