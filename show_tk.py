
from render import BaseRenderContext
from PIL import Image, ImageTk
import tkinter as tk
import random
import logging

log = logging.getLogger("paperd.show_tk")

class RenderContext(BaseRenderContext):
    def __init__(self, drivername, conf, scale=1):
        log.info("init tk output module")
        super().__init__(drivername, conf, scale)
        self.delay = 1000//self.fps

        self.root = tk.Tk()
        self.tkimage = ImageTk.PhotoImage('1', (self.width, self.height))
        self.label = tk.Label(self.root, image=self.tkimage)
        self.label.image = self.tkimage
        self.label.pack()
        self.root.geometry("%dx%d+150+150" % (self.width, self.height))
        self.root.bind('q', self.closeWindow)

    def closeWindow(self, event):
        self.root.quit()

    def display(self):
        self.tkimage.paste(self.image.resize((self.width, self.height)))
        self.root.after(self.delay, self.display)

    def run(self):
        log.info("run tk output module")
        self.display()
        self.root.mainloop()
