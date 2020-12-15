from tkinter import *
from PIL import Image, ImageTk


class Layout :
   def __init__(self,master) :
      self.master = master


   def loadbackground(self,image_loc) :
      self.background_image = Image.open(f'project_pics\\{image_loc}')
      self.image_copy = self.background_image.copy()
      self.background = ImageTk.PhotoImage(self.background_image)
      self.label = Label(self.master, image = self.background)
      # self.label.focus_set()
      self.master.bind('<Configure>',self.resizeimage)
      self.label.pack(fill='both', expand='yes')


   def resizeimage(self,event) :
      image = self.image_copy.resize((self.master.winfo_width(),self.master.winfo_height()))
      self.image1 = ImageTk.PhotoImage(image)
      self.label.config(image = self.image1)