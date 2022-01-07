from collections import defaultdict, deque

# ループのあるゲームの遷移なので、後退解析というアルゴリズムを使う

# 金銀のベクトル
kin = [(1,-1),(0,-1),(-1,-1),(1,0),(-1,0),(1,0)]
gin = [(1,-1),(-1,-1),(1,1),(0,1),(-1,1)]

# いけるマス
edge1 = defaultdict(list)
# これるマス
edge2 = defaultdict(list)
# 出次数
outdeg = defaultdict(int)

# (a,b):金の位置 (c,d):銀の位置
for a in range(1,10):
    for b in range(1,10):
        for c in range(1,10):
            for d in range(1,10):
                for x,y in kin:
                    if 1 <= a+x <= 9 and 1 <= b+y <= 9:
                        edge1[(0,a,b,c,d)].append((1,a+x,b+y,c,d))
                        edge2[(1,a+x,b+y,c,d)].append((0,a,b,c,d))
                        outdeg[(0,a,b,c,d)] += 1
                for x,y in gin:
                    if 1 <= c+x <= 9 and 1 <= d+y <= 9:
                        edge1[(1,a,b,c,d)].append((0,a,b,c+x,d+y))
                        edge2[(0,a,b,c+x,d+y)].append(((1,a,b,c,d)))
                        outdeg[(1,a,b,c,d)] += 1

# 0:未定、1:負け、2:勝ち
win = defaultdict(int)

# その人にとって負け確の状態を決める
q = deque([])
for a in range(1,10):
    for b in range(1,10):
        for c in range(1,10):
            for d in range(1,10):
                if b == 1:
                    win[(1,a,b,c,d)] = 1
                    q.append((1,a,b,c,d))
                elif d == 9:
                    win[(0,a,b,c,d)] = 1
                    q.append((0,a,b,c,d))
                elif (a,b) == (c,d):
                    win[(0,a,b,c,d)] = 1
                    win[(1,a,b,c,d)] = 1
                    q.append((0,a,b,c,d))
                    q.append((1,a,b,c,d))

# 負け確の頂点から遷移
while q:
    i = q.popleft()
    for j in edge2[i]:
        if win[j] == 0:
            win[j] = 2
            for k in edge2[j]:
                # 出次数から勝ちにいけるものを引く
                outdeg[k] -= 1
                if win[k] == 0 and outdeg[k] == 0: # 周り全てが勝ちの時
                    win[k] = 1
                    q.append(k)

dic = {0:"引き分け",1:"負け",2:"勝ち"}

ans1 = win[(0,5,9,5,1)]
ans2 = win[(0,4,9,4,2)]
print("先手番で金が59,銀が51にいる時",dic[ans1])
print("先手番で金が49,銀が42にいる時",dic[ans2])