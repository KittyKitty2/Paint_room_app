import tkinter as tk
from tkinter import colorchooser as tkColorChooser
from tkinter import filedialog as tkFileDialog
from PIL import Image, ImageTk

# Создаем класс Paint 
class Paint:
    def __init__(self, master):
        self.master = master
        self.init()

    def init(self):
        self.master.title("Paint")
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack()

        self.color = "black"
        self.brush_size = 5
        self.last_x = None
        self.last_y = None
        self.brush_image = None

        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.continue_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

        self.drawing = False
        self.last_coords = None

        self.create_tools()

    def create_tools(self):

        tools_frame = tk.Frame(self.master)
        tools_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.delete_brush_button = tk.Button(tools_frame, text="Delete Brush", command=self.delete_brush)
        self.delete_brush_button.pack(side=tk.LEFT)

        self.load_brush_button = tk.Button(tools_frame, text="Load Brush", command=self.load_brush)
        self.load_brush_button.pack(side=tk.LEFT)

        color_button = tk.Button(tools_frame, text="Color", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        brush_size_scale = tk.Scale(tools_frame, from_=1, to=300, orient=tk.HORIZONTAL, command=self.set_brush_size)
        brush_size_scale.pack(side=tk.LEFT)

        eraser_button = tk.Button(tools_frame, text="Eraser", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        import_button = tk.Button(tools_frame, text="Import", command=self.import_image)
        import_button.pack(side=tk.LEFT)

        save_button = tk.Button(tools_frame, text="Save", command=self.save_image)
        save_button.pack(side=tk.LEFT)

    def choose_color(self):
        self.color = tkColorChooser.askcolor(color=self.color)[1]

    def set_brush_size(self, size):
        self.brush_size = int(size)

    def on_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=self.brush_size, fill=self.color)
        self.last_x = event.x
        self.last_y = event.y

    def import_image(self):
        try:
            file_path = tkFileDialog.askopenfilename()
            if file_path:
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    imported_image = Image.open(file_path)
                    self.canvas.delete("all")
                    self.canvas.Image = tk.PhotoImage(imported_image)
                    self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas.tk.Image)
                else:
                    print("Выбранный файл не является поддерживаемым изображением.")
        except Exception as e:
            print(f"Ошибка при импорте изображения: {e}")

    def save_image(self):
        file_name = tkFileDialog.asksaveasfilename()
        if file_name:
            self.canvas.postscript(file=f"{file_name}.png")
            print(f"Холст сохранен как {file_name}.png")

    def set_eraser_size(self, size):
        self.eraser_size = int(size)

    def use_eraser(self):
        self.color = "white" 
        self.brush_size = self.eraser_size

    def load_brush(self):
        brush_path = tkFileDialog.askopenfilename(filetypes=[("Image files", "*.png")])
        if brush_path:
            brush_img = Image.open(brush_path)
            self.brush_image = ImageTk.PhotoImage(brush_img)

    def delete_brush(self):
        self.brush_image = None

    def start_drawing(self, event):
        self.drawing = True
        self.last_coords = (event.x, event.y)

    def continue_drawing(self, event):
        if self.drawing and self.brush_image:
            current_coords = (event.x, event.y)
            self.canvas.create_image(current_coords[0], current_coords[1], image=self.brush_image, anchor=tk.CENTER)
            self.last_coords = current_coords

    def end_drawing(self, event):
        self.drawing = False

root = tk.Tk()
app = Paint(root)
root.bind("<ButtonPress-1>", app.on_press)
root.bind("<B1-Motion>", app.on_drag)
root.mainloop()
