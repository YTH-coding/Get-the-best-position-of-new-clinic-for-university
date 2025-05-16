import numpy as np
import matplotlib.pyplot as plt

# 设置角度和半径
theta = np.linspace(0, 2 * np.pi, 100)  # 角度从0到2π
r = np.abs(np.sin(2 * theta))  # 半径，这里使用sin函数来生成玫瑰图的效果

# 创建极坐标图
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# 绘制玫瑰图
ax.plot(theta, r)

# 设置标题
ax.set_title("玫瑰图示例", va='bottom')

# 显示图形
plt.show()