import numpy as np
import matplotlib.pyplot as plt

# xの範囲を定義（0を除く）
x = np.linspace(0, 1, 400)
# x = 0 を除外
x = x[x != 0]

# y = 1/x を計算
y = 1 / x

# グラフを描画
plt.figure(figsize=(8, 6))
plt.plot(x, y, label="y = 1/x")
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.ylim(00, 100)  # yの表示範囲を制限
plt.xlim(0, 1)
plt.title("y = 1/x")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.show()
