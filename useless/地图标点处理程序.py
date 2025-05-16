import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ImageAnnotator:
    def __init__(self, root, image_path, pointsfile_path, adjacencyfile_path):
        self.root = root
        self.image_path = image_path
        self.points = []
        self.adjacency_list = {}
        self.selected_points = []
        self.mode = "mark"  # 初始模式为标点模式
        self.pointsfile = pointsfile_path
        self.adjacencyfile = adjacencyfile_path

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
        self.save_button = tk.Button(root, text="Save Data", command=self.save_data)
        self.save_button.grid(row=2, column=0, columnspan=2)

        # 添加切换模式按钮
        self.mode_button = tk.Button(root, text="Switch to Connect Mode", command=self.switch_mode)
        self.mode_button.grid(row=3, column=0, columnspan=2)

        # 配置网格布局权重
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # 初始化拖动变量
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # 加载已有的点数据和邻接表
        self.load_points()
        self.load_adjacency_list()

    def load_points(self):
        """加载已有的点数据并在图片上标注"""
        try:
            with open(self.pointsfile, "r") as file:
                for line in file:
                    x, y = map(float, line.strip().split(","))
                    self.points.append((x, y))
                    # 在图片上标注点
                    self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="red")
            print("Points loaded from points.txt")
        except FileNotFoundError:
            print("No points file found. Starting with an empty list.")

    def load_adjacency_list(self):
        """加载邻接表并绘制连接线"""
        try:
            with open(self.adjacencyfile, "r") as file:
                for line in file:
                    point_str, neighbors_str = line.strip().split(":")
                    point = eval(point_str)
                    neighbors = eval(neighbors_str)
                    self.adjacency_list[point] = neighbors
                    # 绘制连接线
                    for neighbor in neighbors:
                        self.canvas.create_line(point[0], point[1], neighbor[0], neighbor[1], fill="blue")
            print("Adjacency list loaded from adjacency_list.txt")
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

    def connect_points(self, point1, point2):
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
        self.update_adjacency_list_file()

    def update_points_file(self):
        """更新 points.txt 文件"""
        with open(self.pointsfile, "w") as file:
            for point in self.points:
                file.write(f"{point[0]},{point[1]}\n")
        print("Points updated in points.txt")

    def update_adjacency_list_file(self):
        """更新 adjacency_list.txt 文件"""
        with open(self.adjacencyfile, "w") as file:
            for point, neighbors in self.adjacency_list.items():
                file.write(f"{point}: {neighbors}\n")
        print("Adjacency list updated in adjacency_list.txt")

    def save_data(self):
        """保存所有数据到文件"""
        self.update_points_file()
        self.update_adjacency_list_file()
        print("Data saved to points.txt and adjacency_list.txt")

    def switch_mode(self):
        """切换模式"""
        if self.mode == "mark":
            self.mode = "connect"
            self.mode_button.config(text="Switch to Mark Mode")
        else:
            self.mode = "mark"
            self.mode_button.config(text="Switch to Connect Mode")
        print(f"Switched to {self.mode} mode")

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("Image Annotator")

    # 图片路径
    image_path = "翔安校区地图.jpg"  # 替换为你的图片路径
    pointsfile = "the_points.txt"
    adjacencyfile = "the_adjacency.txt"

    # 创建标注器实例
    annotator = ImageAnnotator(root, image_path,pointsfile,adjacencyfile)

    # 运行主循环
    root.mainloop()