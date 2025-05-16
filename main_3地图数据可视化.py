from include.fileload import *
from include.picture import annotate_image

# 文件路径
image_path = "data_origin/翔安校区地图.jpg"  # 原始图片路径
points_file = "data_processed/points.txt"      # 点数据文件
adjacency_file = "data_processed/adjacency.txt"  # 邻接表文件
output_path = "pic/road_result.jpg"    # 输出图片路径

# 加载数据
points = xy(points_file)
adjacency_list = tuple_list(adjacency_file)

# 标注图片并保存
annotate_image(image_path, points, adjacency_list, output_path)