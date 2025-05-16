#模块导入
import matplotlib.pyplot as plt
from include.fileload import *
from include.process import dijkstra
from include.picture import create_horizontal_bar_chart

plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']

#定义函数
def data_save(road_data, the_dict, the_file_path):
    """
    将字典筛选排序之后再存储
    """
    map_dict = {the_dict[p]:road_data[p][0] for p in list(the_dict.keys())}
    sorted_dict = dict(sorted(map_dict.items(), key=lambda item: item[1], reverse=True))

    with open(the_file_path,"w",encoding="utf-8") as file:
        for k,v in sorted_dict.items():
            file.write(f"{k}:{v}\n")
        print("Data has been saved")

#文件导入与数据准备
file_graph = "data_processed/adjacency.txt"
file_dorm = "data_processed/dorm.txt"
file_other = "data_processed/build.txt"

start = (4972,1748)

graph = tuple_list(file_graph)

dorm_dict = xy_string(file_dorm)
dorm_list = list(dorm_dict.keys())

other_dict = xy_string(file_other)
other_list = list(other_dict.keys())

#计算得到全部的距离数据
road_data = dijkstra(graph,start)
print(f"有效数据点的个数：{len(road_data)}")

#数据存储（寝室楼和其他建筑物到医务室的距离）
data_save(road_data, dorm_dict, "data_processed/distance_dorm.txt")
data_save(road_data, other_dict, "data_processed/distance_build.txt")

whole_dict = {**dorm_dict, **other_dict}
data_save(road_data, whole_dict, "data_processed/distance_whole.txt")

#利用数据绘图
name2name = {"yux":"毓秀","zs":"至善","ft":"丰庭","dx":"笃行","gg":"国光","ly":"凌云","bx":"博学","yinx":"映雪","fr":"芙蓉","na":"南安","ng":"南光"}
whole = dorm_list + other_list
dorm_file = "data_processed/distance_dorm.txt"
build_file = "data_processed/distance_build.txt"

#绘制图1
distance = list()
for point in whole:
    distance.append(road_data[point][0])
plt.hist(distance, bins = 30, alpha=0.7, color = "blue", edgecolor = "white")
plt.title("目标地点(宿舍楼群、各学院等)\n到医务室距离直方图")
plt.xlabel("距离(像素点)")
plt.ylabel("频数")
plt.savefig("pic\hist_pixel.png",dpi=600)
print("draw picture 1")
plt.show()

#绘制图2
distance = [i/700*300 for i in distance]
plt.hist(distance, bins = 30, alpha=0.7, color = "blue", edgecolor = "white")
plt.title("目标地点(宿舍楼群、各学院等)\n到医务室距离直方图")
plt.xlabel("距离(m)")
plt.ylabel("频数")
plt.savefig("pic\hist_meter.png",dpi=600)
print("draw picture 2")
plt.show()

#绘制图3
dorm_distance = string_float(dorm_file)
distance_list = list(dorm_distance.values())
name_list = list()
for name_,distance_ in dorm_distance.items():
    flag = 0
    for j in name2name:
        if j in name_:
            flag = 1
            break 
    name_list.append(name_.replace(j, name2name[j]))

fig, ax = create_horizontal_bar_chart(categories=name_list, values=distance_list, title="寝室楼群到医务室的距离", x_label="距离(m)", y_label="寝室楼名",y_ticksize=8)
plt.savefig("pic/dorm.png",dpi=400)
print("draw picture 3")
plt.show()

#绘制图4
build_distance = string_float(build_file)
distance_list = list(build_distance.values())
name_list = list(build_distance.keys())

fig, ax = create_horizontal_bar_chart(categories=name_list, values=distance_list, title="其他建筑到医务室的距离", x_label="距离(m)", y_label="建筑名",y_ticksize=12)
plt.savefig("pic/build.png",dpi=400)
print("draw picture 4")
plt.show()
