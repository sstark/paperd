
from render import BaseRenderContext
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import random

class RenderContext(BaseRenderContext):
    def __init__(self, drivername, conf):
        print("init tk output module")
        BaseRenderContext.__init__(self, drivername, conf)
        self.draw = ImageDraw.Draw(self.image)
        self.delay = 1000//self.fps
        self.root = tk.Tk()
        self.tkimage = ImageTk.PhotoImage('1', (self.width, self.height))
        self.label = tk.Label(self.root, image=self.tkimage)
        self.label.image = self.tkimage
        self.label.pack()

    def display(self):
        a = random.randint(0,self.width-80)
        self.draw.rectangle((0, 0, self.width, self.height), fill = 255, outline = 255)
        self.draw.ellipse((20+a, 20, 80+a, 80), fill = 0, outline = 0)
        self.tkimage.paste(self.image)
        self.root.after(self.delay, self.display)

    def run(self):
        print("run tk output module")
        self.display()
        self.root.mainloop()
