import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei'] #中文显示设置

# 数据
labels = ['A', 'B', 'C', 'D', 'E', 'F']  # 扇区标签
sizes = [15, 30, 37, 10, 20, 25]       # 扇区大小
explode = (0, 0.1, 0, 0, 0, 0)       # 分离距离（0 表示不分离，0.1 表示分离 10%）

fig, ax = plt.subplots()

number = 1

if number==1:
    ###基础版
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#e377c2', '#00a0b0'],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1})

    # 设置标题
    ax.set_title("高级一点的饼图")

elif number == 2:
    ###进阶版
    wedges, texts, autotexts = ax.pie(
    sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    shadow=False, startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#e377c2', '#00a0b0'],
    pctdistance=1.4,  # 将百分比数字移到饼图外面
    textprops={'fontsize': 12, 'color': 'black'},  # 设置文本样式
    wedgeprops={'edgecolor': 'white', 'linewidth': 1}  # 添加边界线
    )

plt.savefig("饼图.png",dpi=600)
# 显示图形
plt.show()