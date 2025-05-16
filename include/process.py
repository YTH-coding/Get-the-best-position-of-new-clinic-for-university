import math
from heapq import heappush, heappop

def dijkstra_o(graph:dict, start:tuple):
    road_data = {point:[math.inf, (0,0)] for point in graph.keys()}
    road_data[start][0] = 0
    visted = set()

    #print(graph)
    while visted < set(graph.keys()):
        min_dist = math.inf
        min_node = None
        for node in graph: #遍历所有点，得到未访问的点中距离最小的点
            if node not in visted and road_data[node][0] < min_dist:
                min_dist = road_data[node][0]
                min_node = node
        
        visted.add(min_node)

        for neigh, dist in graph[min_node].items():
            new_dist = road_data[min_node][0] + dist
            if new_dist < road_data[neigh][0]:
                road_data[neigh][0] = new_dist
                road_data[neigh][1] = min_node
    return road_data

def dijkstra(graph: dict, start: tuple) -> dict[tuple, list[float, list[tuple]]]:
    road_data = {
        point: [math.inf, []]  # 格式: [距离, 路径列表]
        for point in graph.keys()
    }
    road_data[start] = [0, [start]]  # 起点距离为0，路径包含自己
    heap = []
    heappush(heap, (0, start))  # 优先队列: (距离, 节点)

    while heap:
        current_dist, min_node = heappop(heap)
        if current_dist > road_data[min_node][0]:
            continue  # 已找到更短路径，跳过

        for neigh, dist in graph[min_node].items():
            new_dist = current_dist + dist
            if new_dist < road_data[neigh][0]:
                road_data[neigh][0] = new_dist
                road_data[neigh][1] = road_data[min_node][1] + [neigh]  # 更新路径
                heappush(heap, (new_dist, neigh))

    return road_data