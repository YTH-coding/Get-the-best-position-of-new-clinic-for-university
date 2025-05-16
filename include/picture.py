import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']

from PIL import Image, ImageDraw

class ImageAnnotator:
    def __init__(self, root, image_path, pointsfile_path, adjacencyfile_path):
        self.root = root
        self.image_path = image_path
        self.points_path = pointsfile_path
        self.adjacency_path = adjacencyfile_path
        self.points = []
        self.adjacency_list = {}
        self.selected_points = []
        self.mode = "mark"  # 初始模式为标点模式
        self.delete_mode = False  # 删除模式开关

        # 加载图片
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # 创建画布和滚动条
        self.canvas = tk.Canvas(root, width=800, height=600, scrollregion=(0, 0, self.image.width, self.image.height))
        self.h_scroll = ttk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.v_scroll = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        # 布局
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")

        # 在画布上显示图片
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)  # 右键删除
        self.canvas.bind("<Control-Button-1>", self.on_ctrl_click)  # Ctrl+左键删除线

        # 添加按钮
        self.save_button = tk.Button(root, text="Save Data", command=self.save_data)
        self.save_button.grid(row=2, column=0, columnspan=2)
        
        self.mode_button = tk.Button(root, text="Switch to Connect Mode", command=self.switch_mode)
        self.mode_button.grid(row=3, column=0, columnspan=2)
        
        self.delete_button = tk.Button(root, text="Enable Delete Mode", command=self.toggle_delete_mode)
        self.delete_button.grid(row=4, column=0, columnspan=2)

        # 配置网格布局权重
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # 初始化拖动变量
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # 加载已有的点数据和邻接表
        self.load_points()
        self.load_adjacency_list()

    def toggle_delete_mode(self):
        """切换删除模式"""
        self.delete_mode = not self.delete_mode
        if self.delete_mode:
            self.delete_button.config(text="Disable Delete Mode", bg="red")
            print("Delete mode enabled")
        else:
            self.delete_button.config(text="Enable Delete Mode", bg="SystemButtonFace")
            print("Delete mode disabled")

    def on_right_click(self, event):
        """右键删除点"""
        if not self.delete_mode:
            return
            
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        # 找到最近的点
        closest_point = self.find_closest_point(x, y)
        if closest_point:
            self.delete_point(closest_point)

    def on_ctrl_click(self, event):
        """Ctrl+左键删除线"""
        if not self.delete_mode:
            return
            
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        # 找到最近的线
        closest_line = self.find_closest_line(x, y)
        if closest_line:
            self.delete_line(closest_line)

    def find_closest_line(self, x, y, threshold=10):
        """找到最近的线"""
        closest_line = None
        min_distance = float('inf')
        
        for point, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                # 计算点到线段的距离
                dist = self.point_to_line_distance((x,y), point, neighbor)
                if dist < threshold and dist < min_distance:
                    min_distance = dist
                    closest_line = (point, neighbor)
        
        return closest_line

    def point_to_line_distance(self, point, line_start, line_end):
        """计算点到线段的距离"""
        # 实现点到线段距离的计算
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        # 线段长度平方
        l2 = (x2-x1)**2 + (y2-y1)**2
        if l2 == 0:  # 线段退化为点
            return ((x-x1)**2 + (y-y1)**2)**0.5
            
        # 计算投影比例，内积除以长度
        t = max(0, min(1, ((x-x1)*(x2-x1) + (y-y1)*(y2-y1)) / l2))
        
        # 投影点
        projection = x1 + t*(x2-x1), y1 + t*(y2-y1)
        
        # 返回点到投影点的距离
        return ((x-projection[0])**2 + (y-projection[1])**2)**0.5

    def delete_point(self, point):
        """删除点及其所有连接线"""
        # 从points列表中移除
        if point in self.points:
            self.points.remove(point)
            
        # 从邻接表中移除所有相关连接
        if point in self.adjacency_list:
            # 先删除其他点到该点的连接
            for other_point in self.adjacency_list[point]:
                if other_point in self.adjacency_list and point in self.adjacency_list[other_point]:
                    self.adjacency_list[other_point].remove(point)
            
            # 再删除该点的所有连接
            del self.adjacency_list[point]
        
        # 重绘画布
        self.redraw_canvas()
        
        # 更新文件
        self.update_points_file()
        self.update_adjacency_file()
        
        print(f"Deleted point: {point}")

    def delete_line(self, line):
        """删除连接线"""
        point1, point2 = line
        
        # 从邻接表中移除连接
        if point1 in self.adjacency_list and point2 in self.adjacency_list[point1]:
            self.adjacency_list[point1].remove(point2)
            
        if point2 in self.adjacency_list and point1 in self.adjacency_list[point2]:
            self.adjacency_list[point2].remove(point1)
        
        # 重绘画布
        self.redraw_canvas()
        
        # 更新文件
        self.update_adjacency_file()
        
        print(f"Deleted line between {point1} and {point2}")

    def redraw_canvas(self):
        """重绘整个画布"""
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        
        # 重绘所有连接线
        for point, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                self.canvas.create_line(point[0], point[1], neighbor[0], neighbor[1], fill="blue")
        
        # 重绘所有点
        for (x, y) in self.points:
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="red")

    # ... (保留原有的 load_points, load_adjacency_list, on_click, find_closest_point, 
    # connect_points, update_points_file, update_adjacency_file, 
    # save_data, switch_mode 等方法不变)
    def load_points(self):
        """加载已有的点数据并在图片上标注"""
        try:
            with open(self.points_path, "r") as file:
                for line in file:
                    x, y = line.strip().split(",")
                    x, y = float(x), float(y)
                    self.points.append((x, y))
                    # 在图片上标注点
                    self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="red")
            print("Points loaded from pointsfile")
        except FileNotFoundError:
            print("No points file found. Starting with an empty list.")

    def load_adjacency_list(self):
        """加载邻接表并绘制连接线"""
        try:
            with open(self.adjacency_path, "r") as file:
                for line in file:
                    point_str, neighbors_str = line.strip().split(":")
                    point = eval(point_str)
                    neighbors = eval(neighbors_str)
                    self.adjacency_list[point] = neighbors
                    # 绘制连接线
                    for neighbor in neighbors:
                        self.canvas.create_line(point[0], point[1], neighbor[0], neighbor[1], fill="blue")
            print("Adjacency list loaded from list_adjacency.txt")
        except FileNotFoundError:
            print("No adjacency list file found. Starting with an empty list.")

    def on_click(self, event):
        """处理鼠标点击事件"""
        # 获取点击位置的坐标
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if self.mode == "mark":
            # 在点击的位置画一个点
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="red")

            # 记录点的位置
            self.points.append((x, y))
            print(f"Point marked at: ({x}, {y})")

            # 更新 points.txt 文件
            self.update_points_file()

        elif self.mode == "connect":
            # 找到最近的点
            closest_point = self.find_closest_point(x, y)
            if closest_point:
                self.selected_points.append(closest_point)
                print(f"Selected point: {closest_point}")

                # 如果选择了两个点，连接它们
                if len(self.selected_points) == 2:
                    self.connect_points(self.selected_points[0], self.selected_points[1])
                    self.selected_points = []  # 清空已选点

    def find_closest_point(self, x, y):
        """找到离点击位置最近的点"""
        min_distance = float("inf")
        closest_point = None
        for (px, py) in self.points:
            distance = (px - x) ** 2 + (py - y) ** 2
            if distance < min_distance:
                min_distance = distance
                closest_point = (px, py)
        return closest_point

    def connect_points(self, point1: tuple[float, float], point2: tuple[float, float]) -> None:
        """连接两个点并更新邻接表"""
        # 在邻接表中添加邻接关系
        if point2 not in self.adjacency_list.get(point1, []):
            if point1 not in self.adjacency_list:
                self.adjacency_list[point1] = []
            self.adjacency_list[point1].append(point2)

        if point1 not in self.adjacency_list.get(point2, []):
            if point2 not in self.adjacency_list:
                self.adjacency_list[point2] = []
            self.adjacency_list[point2].append(point1)

        # 在图片上绘制连接线
        self.canvas.create_line(point1[0], point1[1], point2[0], point2[1], fill="blue")
        print(f"Connected {point1} and {point2}")

        # 更新 adjacency_list.txt 文件
        self.update_adjacency_file()

    def update_points_file(self):
        """更新 points.txt 文件"""
        with open(self.points_path, "w") as file:#写入模式，直接清空原有内容
            for point in self.points:
                file.write(f"{point[0]},{point[1]}\n")
        print("Points updated in pointsfile")

    def update_adjacency_file(self):
        """更新 list_adjacency.txt 文件"""
        with open(self.adjacency_path, "w") as file:
            for point, neighbors in self.adjacency_list.items():
                file.write(f"{point}: {neighbors}\n")
        print("Adjacency list updated in adjacencyfile")

    def save_data(self):
        """保存所有数据到文件"""
        self.update_points_file()
        self.update_adjacency_file()
        print("Data saved to points.txt and adjacency.txt")

    def switch_mode(self):
        """切换模式"""
        if self.mode == "mark":
            self.mode = "connect"
            self.mode_button.config(text="Switch to Mark Mode")
        else:
            self.mode = "mark"
            self.mode_button.config(text="Switch to Connect Mode")
        print(f"Switched to {self.mode} mode")

def create_horizontal_bar_chart(categories, values, title="横向条形统计图", 
                               x_label="数值", y_label="类别",y_ticksize = 12,
                               colors="blue", show_values=True, 
                               figsize=(10, 15), save_path=None):
    # 创建图表
    fig, ax = plt.subplots(figsize=figsize)
    
    # 设置条形位置和宽度
    y_pos = np.arange(len(categories))
    bar_width = 0.6
    
    # 绘制条形图
    bars = ax.barh(y_pos, values, bar_width, 
                  align='center', color=colors, alpha=0.8)
    
    # 设置y轴刻度和标签
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=y_ticksize)
    
    # 设置标题和标签
    ax.set_title(title, fontsize=15, pad=15)
    ax.set_xlabel(x_label, fontsize=12, labelpad=10)
    ax.set_ylabel(y_label, fontsize=12, labelpad=10)
    
    # 添加网格线
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # 在条形上显示数值
    if show_values:
        for bar, value in zip(bars, values):
            ax.text(bar.get_width() + max(values) * 0.01, 
                    bar.get_y() + bar.get_height()/2,
                    f'{value:.2f}',
                    ha='left', va='center',
                    fontsize=10)
    
    # 调整x轴范围，使条形和数值显示更美观
    ax.set_xlim(0, max(values) * 1.1)
    
    # 添加背景颜色
    ax.set_facecolor('#f8f9fa')
    
    # 美化图表
    plt.tight_layout()
    
    # 保存图表
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax

def annotate_image(image_path, points, adjacency_list, output_path, point_color="red", line_color="blue", point_radius=3, line_width=2):
    """
    在图片上标注点和连接线并保存新图片
    :param image_path: 原始图片路径
    :param points: 点的坐标列表，格式为 [(x1, y1), (x2, y2), ...]
    :param adjacency_list: 邻接表，格式为 { (x1,y1): [(x2,y2), ...], ... }
    :param output_path: 保存新图片的路径
    :param point_color: 点的颜色，默认为红色
    :param line_color: 连接线的颜色，默认为蓝色
    :param point_radius: 点的半径，默认为 3 像素
    :param line_width: 连接线的宽度，默认为 2 像素
    """
    # 打开图片
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # 绘制连接线
    for point, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            draw.line([point, neighbor], fill=line_color, width=line_width)

    # 绘制点
    for (x, y) in points:
        draw.ellipse(
            [(x - point_radius, y - point_radius), 
             (x + point_radius, y + point_radius)],
            fill=point_color,
            outline=point_color
        )
        biggersize = 8
        color_temp = "red"
        if x==1419 and y==1996:
            draw.ellipse(
            [(x - point_radius*biggersize, y - point_radius*biggersize), 
             (x + point_radius*biggersize, y + point_radius*biggersize)],
            fill=color_temp,
            outline=color_temp
            )
            
    # 保存新图片
    image.save(output_path)
    print(f"Annotated image saved to {output_path}")

def draw_circles_on_image(image_path,data:dict,savepath,title,bestpoint):
    # 读取图片
    image_path = 'pic\graph_getting.jpg'
    img = Image.open(image_path)
    img_array = np.array(img)

    # 创建图形和轴
    fig, ax = plt.subplots()
    ax.imshow(img_array)

    # 在图片上覆盖一层有透明度的白色
    white_layer = np.ones_like(img_array) * 255
    white_layer = white_layer.astype(np.uint8)
    alpha = 0.5
    overlay = np.uint8(alpha * white_layer + (1 - alpha) * img_array)
    ax.imshow(overlay)

    # 归一化距离，用于颜色映射
    distances = list(data.values())
    min_distance = min(distances)
    max_distance = max(distances)
    norm = plt.Normalize(min_distance, max_distance)
    cmap = plt.get_cmap('RdYlGn_r')

    # 在对应的像素坐标位置画圆圈
    for (x, y), distance in data.items():
        color = cmap(norm(distance))
        circle = Circle((x, y), radius=10, color=color)
        ax.add_patch(circle)

    circle = Circle(bestpoint,radius = 20, color = "blue")
    ax.add_patch(circle)
    
    # 添加颜色条配置
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    # 设置可映射的数据范围
    sm.set_array(distances)

    # 创建颜色条并配置
    cbar_ax = fig.add_axes([0.88, 0.12, 0.02, 0.76])  # [左, 下, 宽, 高]
    cbar = fig.colorbar(sm, cax=cbar_ax)

    # 配置颜色条标签和刻度
    cbar.set_label('距离值（像素距离）', fontsize=8, fontweight='bold')
    cbar.ax.tick_params(labelsize=4)
    min_dist = min(distances)
    max_dist = max(distances)
    # 添加颜色条刻度标记
    ticks = np.linspace(min_dist, max_dist, 5)
    cbar.set_ticks(ticks)
    cbar.set_ticklabels([f'{t:.2f}' for t in ticks])

    # 添加颜色条标题
    cbar_ax.text(0.5, 1.05, title, transform=cbar_ax.transAxes,
                 ha='center', va='bottom', fontsize=8, fontweight='bold')

    # plt.title('最优点查找情况', fontsize=12, y=1.02)

    # 隐藏坐标轴
    ax.axis('off')
    plt.savefig(savepath, dpi=400)
    plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Annotator with Delete Function")
    
    image_path = "data\翔安校区地图.jpg"
    annotator = ImageAnnotator(root, image_path)
    root.mainloop()