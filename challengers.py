from itertools import permutations

# 先攻、後攻のデッキ内容
deck1 = [1,1,1,2,3,4]
deck2 = [1,1,1,2,3,4]
# 各カードの数字
power = [0,1,2,3,4]

# 全探索時の先攻、後攻の勝ち数
win = [0,0]
for g1 in permutations(deck1):
    for g2 in permutations(deck2):
        # デッキ内のカードの並び順（後ろが先に出てくる）
        d = [list(g1),list(g2)]
        # ベンチのカード
        bench = [{},{}]
        # 場に出ているカード
        stack = [[d[0].pop()],[]]
        # 手番
        turn = 1
        # 0:先攻勝ち、1:後攻勝ち
        w = -1
        while w == -1:
            # 場に出ているカードの数字合計
            s = 0
            # フラグカードの数字
            flag = power[stack[turn^1][-1]]

            # フラグより大きくなるまでカードを出す
            while s < flag:
                if len(d[turn]) == 0:
                    w = turn^1
                    break

                x = d[turn].pop()
                stack[turn].append(x)
                s += power[x]

            if w != -1:
                break

            # 相手の場のカードをベンチに送る
            while stack[turn^1]:
                x = stack[turn^1].pop()
                if not x in bench[turn^1]:
                    bench[turn^1][x] = 0
                bench[turn^1][x] += 1

            # ベンチが6種類超えたら負け
            if len(bench[turn^1]) > 6:
                w = turn
            
            turn ^= 1
        
        win[w] += 1

print(*win)