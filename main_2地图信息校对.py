from include.fileload import *

file_points = "data_processed/points.txt"
file_graph = "data_processed/adjacency.txt"
file_dorm = "data_processed/dorm.txt"
file_build = "data_processed/build.txt"

points = xy(file_points)

graph = tuple_list(file_graph)
graph_list = list(graph.keys())

dorm_dict = xy_string(file_dorm)
dorm_list = list(xy_string(file_dorm).keys())

other_dict = xy_string(file_build)
other_list = list(other_dict.keys())

print(f"{file_points}数据个数:{len(points)}\n{file_graph}数据个数:{len(graph)}")
points_graph = list(set(points)-set(graph_list))
print(f"多余的点(pointsfile独有):{points_graph}")
graph_points = list(set(graph_list)-set(points))
print(f"多余的点(adjacencyfile独有):{graph_points}")

temp = list(set(points)-set(graph_list))
for p in temp:
    if p in dorm_list:
        print(f"({p[0]},{p[1]}) is dorm-node, name is {dorm_dict[p]}")
    elif p in other_list:
        print(f"({p[0]},{p[1]}) is other-node, name is {other_dict[p]}")
    else:
        print(f"({p[0]},{p[1]}) is road-node")

if len(points_graph) != 0:
    operate_code = str(input("Delete these points from pointsfile?(Y/n):"))
    if operate_code == 'Y':
        for i in points_graph:
            points.remove(i)
        with open(file_points, "w") as file:#写入模式，直接清空原有内容
            for point in points:
                file.write(f"{float(point[0])},{float(point[1])}\n")
        print("Points updated in pointsfile")

if len(graph_points) != 0:
    operate_code = str(input("Delete these points from adjacencyfile?(Y/n):"))
    if operate_code == 'Y':
        for i in graph_points:
            del graph[i]
        with open(file_graph, "w") as file:
            for point, neighbors in graph.items():
                neighbors = list(neighbors.keys())
                file.write(f"{point}: {neighbors}\n")
        print("Adjacency list updated in adjacencyfile")