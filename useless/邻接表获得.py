import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

class PointConnector:
    def __init__(self, root, image_path, points):
        self.root = root
        self.image_path = image_path
        self.points = points  # 点的坐标列表
        self.adjacency_list = {point: [] for point in points}  # 邻接表
        self.selected_points = []  # 用于存储用户选择的点

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

        # 绑定鼠标点击事件
        self.canvas.bind("<Button-1>", self.on_click)

        # 添加保存按钮
        self.save_button = tk.Button(root, text="Save Adjacency List", command=self.save_adjacency_list)
        self.save_button.grid(row=2, column=0, columnspan=2)

        # 配置网格布局权重
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # 初始化点的绘制
        self.draw_points()

    def draw_points(self):
        """在图片上绘制点"""
        for (x, y) in self.points:
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="red")

    def on_click(self, event):
        """处理鼠标点击事件"""
        # 获取点击位置的坐标
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

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

    def connect_points(self, point1, point2):
        """连接两个点并更新邻接表"""
        # 在邻接表中添加邻接关系
        if point2 not in self.adjacency_list[point1]:
            self.adjacency_list[point1].append(point2)
        if point1 not in self.adjacency_list[point2]:
            self.adjacency_list[point2].append(point1)

        # 在图片上绘制连接线
        self.canvas.create_line(point1[0], point1[1], point2[0], point2[1], fill="blue")
        print(f"Connected {point1} and {point2}")

    def save_adjacency_list(self):
        """保存邻接表到文件"""
        with open("adjacency_list.txt", "w") as file:
            for point, neighbors in self.adjacency_list.items():
                file.write(f"{point}: {neighbors}\n")
        print("Adjacency list saved to adjacency_list.txt")

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("Point Connector")

    # 图片路径
    image_path = "翔安校区地图.jpg"  # 替换为你的图片路径

    data = []
    with open("points.txt","r") as file:
        for line in file:
            x, y = map(float, line.strip().split(","))  # 使用 float 读取坐标
            data.append((x,y))
    # 点的坐标
    points = data  # 替换为你的点坐标

    # 创建点连接器实例
    connector = PointConnector(root, image_path, points)

    # 运行主循环
    root.mainloop()