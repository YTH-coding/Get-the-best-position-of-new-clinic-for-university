from include.fileload import *
import math
import matplotlib.pyplot as plt
from include.picture import draw_circles_on_image

plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']

file_path = ["data_processed/clinic_one_dorm.txt", "data_processed/clinic_one_whole.txt", "data_processed/clinic_two_dorm.txt", "data_processed/clinic_two_whole.txt"]
title = ["单医务室最优位置\n考虑寝室","单医务室最优位置\n考虑全部","双医务室最优位置\n考虑寝室","双医务室最优位置\n考虑全部"]
for i in range(4):
    dist_list = tuple_float(file_path[i])

    min_value = math.inf
    min_point = [0,0]

    for k,v in dist_list.items():
        if v<min_value:
            min_point[0], min_point[1] = k[0], k[1]
            min_value = v
    final_pic_path = file_path[i].replace("data_processed/","").replace("txt","png")
    draw_circles_on_image("pic/road_result.jpg",dist_list,f"pic/heatmap_{final_pic_path}",title[i],min_point)
    print(f"{file_path[i]}最优点为：",min_value,min_point)
    
