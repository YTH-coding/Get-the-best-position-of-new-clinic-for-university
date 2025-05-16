import matplotlib.pyplot as plt

# 示例：绘制道路数据
def plot_roads(file_path):
    with open(file_path, 'r') as f:
        points = [tuple(map(float, line.strip().split(','))) for line in f]
    x, y = zip(*points)
    plt.plot(x, y, 'b-', linewidth=1)  # 蓝色线条表示道路

# 绘制宿舍楼群
def plot_dorm(file_path, color='red'):
    with open(file_path, 'r') as f:
        points = [tuple(map(float, line.strip().split(','))) for line in f]
    x, y = zip(*points)
    plt.scatter(x, y, c=color, s=10, label=file_path.split('_')[-1].split('.')[0])

# 主程序
plt.figure(figsize=(15, 10))
plot_roads('地图数据_道路.txt')
plot_dorm('地图数据_宿舍楼群_芙蓉南安.txt', 'red')
plot_dorm('地图数据_宿舍楼群_映雪国光笃行凌云博学.txt', 'green')
plt.legend()
plt.title('厦门大学翔安校区地图')
plt.xlabel('X 坐标')
plt.ylabel('Y 坐标')
plt.grid(True)
plt.show()