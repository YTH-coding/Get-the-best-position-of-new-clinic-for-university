import tkinter as tk
from include.picture import ImageAnnotator

root = tk.Tk()
root.title("Image Annotator with Delete Function")

image_path = "data_origin/翔安校区地图.jpg"
points_path = "data_processed/points.txt"
adjacency_path = "data_processed/adjacency.txt"
annotator = ImageAnnotator(root, image_path,points_path, adjacency_path)
root.mainloop()