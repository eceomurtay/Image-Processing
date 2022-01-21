from tkinter import *
from PIL import ImageTk


class Crop:

    def __init__(self, screen, img, width, height, box):

        self.x = self.y = 0
        self.screen = screen
        self.box = box
        self.area = Canvas(screen, width=width, height=height, cursor="cross")
        self.area.pack(side="top", fill="both", expand=True)
        self.area.bind("<ButtonPress-1>", self.on_button_press)
        self.area.bind("<B1-Motion>", self.on_move_press)
        self.area.bind("<ButtonRelease-1>", self.on_button_release)
        self.area.bind_all('<Escape>', self.on_esc_press)
        ok_button = Button(screen, text="OK", command=self.get_rect_area,
                           bg="#e0e0e0", fg='green', font=('calibre', 15, 'bold'))
        ok_button.pack(side=BOTTOM, fill="both")

        self.rect = None

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.resized_image = img.resize((width, height))
        self.tk_img = ImageTk.PhotoImage(self.resized_image)
        self.area.create_image(0, 0, anchor="nw", image=self.tk_img)

    def __repr__(self):
        return self.box

    def on_button_press(self, event):

        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y
        # create rectangle if not yet exist
        self.rect = self.area.create_rectangle(self.x, self.y, 1, 1, fill="#e0e0e0", stipple='gray25')

    def on_move_press(self, event):

        self.end_x = event.x
        self.end_y = event.y
        # expand rectangle as you drag the mouse
        self.area.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        pass

    def on_esc_press(self, event):

        self.area.delete(self.rect)

    def get_rect_area(self):

        self.box = self.area.coords(self.rect)
        self.screen.destroy()

