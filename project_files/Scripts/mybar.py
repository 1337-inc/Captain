from tkinter import *
from PIL import Image, ImageTk


# The Custom Variable Widgets
class MyBar(Canvas) :
    def __init__(self, master, shape, value=0, maximum=100,
                 bg="#231303", trough_color='#8a7852', bar_color='#f7f4bf'):
        # open shape mask with PIL
        im_shape_alpha = Image.open(shape).convert('L')
        # create bar shape image with the choosen backgroound color
        im_shape = Image.new('RGBA', im_shape_alpha.size, bg)
        # apply shape as alpha mask to "cut out" the bar shape
        im_shape.putalpha(im_shape_alpha)
        width, height = im_shape_alpha.size
        # create the canvas
        Canvas.__init__(self, master, bg=trough_color, width=width, height=height, highlightthickness=0)

        self._value = value  # bar value
        self.maximum = maximum  # maximum value

        # bar width and height
        self.height = height
        self.width = width

        # create tkinter image for the shape from the PIL Image
        self.img_trough = ImageTk.PhotoImage(im_shape, master=self)
        # create bar to display the value
        self.create_rectangle(0, height, width, height * (1 - value/self.maximum), width=0, fill=bar_color, tags='pbar')
        # display shape on top
        self.create_image(0, 0, anchor='nw', image=self.img_trough)

    @property
    def value(self):
        """Return bar's value'"""
        return self._value

    @value.setter
    def value(self, value):
        """Set bar's value'"""
        self._value = value
        # adjust bar height to value
        self.coords('pbar', 0, self.height, self.width, self.height*(1 - value/self.maximum))