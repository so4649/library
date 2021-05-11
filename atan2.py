# 各点をatan2でソート O(NlogN)

def atan2_sort(coords):
    class Cmp:
        def __init__(self, obj):
            self.obj = obj

        def __lt__(self, other):
            return self.cmp(self.obj, other.obj) < 0

        def cmp(self, p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            if x1 * y2 - y1 * x2 < 0: return 1
            elif x1 * y2 - y1 * x2 > 0: return -1
            else: return 0

    quadrant = [[] for i in range(4)]
    for x, y in coords:
        if x == 0 and y == 0: quadrant[2].append((x, y))
        elif x <= 0 and y < 0: quadrant[0].append((x, y))
        elif x > 0 and y <= 0: quadrant[1].append((x, y))
        elif x >= 0 and y > 0: quadrant[2].append((x, y)) 
        else: quadrant[3].append((x, y))

    res = []
    for i in range(4):
        quadrant[i].sort(key=Cmp)
        for p in quadrant[i]:
            res.append(p)
    return res


n = int(input())
coords = [list(map(int, input().split())) for i in range(n)]


ans = atan2_sort(coords)
for res in ans:
    print(*res)