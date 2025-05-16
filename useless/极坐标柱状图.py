import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei'] #中文显示设置

# 数据
categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
values = [10, 15, 7, 12, 9, 14, 8, 11]

colors = ['#ff6347', '#50c878', '#e3a857', '#d62728', '#9467bd', '#f9dc24', '#e377c2', '#00a0b0']

# 角度设置
theta = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)  # 将圆分成与类别数相同的角度
width = 2 * np.pi / len(categories)  # 每个柱子的宽度

# 创建极坐标图
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# 设置类别标签
ax.set_xticks(theta)
ax.set_xticklabels(categories)

# 绘制柱状图
bars = ax.bar(theta, values, width=width, bottom=0, color=colors, edgecolor='white')

# 设置标题
plt.title("玫瑰图（极坐标柱状图）", pad=20)

# 显示图形
plt.show()