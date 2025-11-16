# 神様が決めるランダム・シャッフル
import numpy as np
N = 26                      # 参加者数が26名の場合
junban = np.arange(N)       # 0 ～ 25 の数字列を作る
np.random.seed(20251122)    # 開催日を乱数の種にする（再現性確保のため）
np.random.shuffle(junban)   # ランダムにシャフルする
print(', '.join([str(i+1) for i in junban]))    # カンマ区切りで印字する