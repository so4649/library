from collections import deque

n = int(input())
edge = [[] for i in range(n)]
for i in range(n-1):
    x, y = map(int, input().split())
    edge[x-1].append(y-1)
    edge[y-1].append(x-1)
 
parent = [-1] * n
q = deque([0])
r = []
while q:
    i = deque.popleft(q)
    r.append(i)
    for a in edge[i]:
        if a != parent[i]:
            parent[a] = i
            deque.append(q, a)
print(parent)
print(r)