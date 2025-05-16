from include.process import dijkstra
from include.fileload import *
from tqdm import tqdm

def calculate_and_save(graph, points, target_list, filename, desc, compare_with=None):
    """
    通用计算函数
    :param graph: 图数据结构
    :param points: 要计算的点集合
    :param target_list: 目标点列表(whole或dorm_list)
    :param filename: 保存文件名
    :param desc: 进度条描述
    :param compare_with: 用于比较的已有路径数据(任务3/4使用)
    """
    result = dict()
    for point in tqdm(points, desc=desc, total=len(points)):
        road_data_new = dijkstra(graph, point)
        
        if compare_with:
            distance_data = [min(road_data_new[k][0], compare_with[k][0]) for k in target_list]
        else:
            distance_data = [road_data_new[k][0] for k in target_list]
        
        result[point] = sum(distance_data)
    
    with open(filename, "w", encoding="utf-8") as file:
        for k, v in result.items():
            file.write(f"{k}:{v}\n")
    print(f"{desc}映射已保存")

file_points = "data_processed/points.txt"
file_graph = "data_processed/adjacency.txt"
file_dorm = "data_processed/dorm.txt"
file_other = "data_processed/build.txt"

start = (4972,1748)

points = xy(file_points)

graph = tuple_list(file_graph)

dorm_dict = xy_string(file_dorm)
dorm_list = list(dorm_dict.keys())
dorm_name = list(dorm_dict.values())

other_dict = xy_string(file_other)
other_list = list(other_dict.keys())
other_dist = list(other_dict.values())

road_data = dijkstra(graph,start)
print(f"有效数据点的个数：{len(road_data)}")


#接下来是三种情况的遍历计算
operation = [1,2,3,4]
whole = other_list + dorm_list

# 任务1: 全校只有一个医务室，计算寝室+建筑的最短距离之和
if 1 in operation:
    calculate_and_save(graph, points, whole, "data_processed/clinic_one_whole.txt", "任务1进度")

# 任务2: 全校只有一个医务室，计算寝室的最短距离之和
if 2 in operation:
    calculate_and_save(graph, points, dorm_list, "data_processed/clinic_one_dorm.txt", "任务2进度")

# 任务3: 现有医务室不变，加一个新的，计算寝室+建筑的最短距离之和
if 3 in operation:
    calculate_and_save(graph, points, whole, "data_processed/clinic_two_whole.txt", "任务3进度", road_data)

# 任务4: 现有医务室不变，加一个新的，计算寝室的最短距离之和
if 4 in operation:
    calculate_and_save(graph, points, dorm_list, "data_processed/clinic_two_dorm.txt", "任务4进度", road_data)