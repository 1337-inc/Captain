import tkinter as tk
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from ttkthemes import ThemedTk

class SplashScreen :
    def __init__(self,parent,nxt_func) :
        """Initialize main background image and set widow size."""
        self.parent = parent
        self.parent.overrideredirect(True)
        self.nxt_func = nxt_func
        self.splash()
        self.window()

    def splash(self) :
        self.image1 = Image.open('project_pics\\splash.png')

    def window(self) :
        width, height = self.image1.size
        setwinwidth = (self.parent.winfo_screenwidth()-width)//2
        setwinheight = (self.parent.winfo_screenheight()-height)//2
        self.parent.geometry(f"{width}x{height}+{setwinwidth}+{setwinheight}")

    def proceed(self) :
        self.nxt_func()

    def display(self) :
        self.parent.deiconify()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        splash_canvas = tk.Canvas(self.parent,width=screen_width,height=screen_height)
        splash_canvas.pack()
        self.tkimage = ImageTk.PhotoImage(self.image1)
        splash_canvas.create_image(0,0,image=self.tkimage,anchor="nw")
        splash_canvas.create_text(200,34,text="[LOADING]...PLEASE WAIT",font=("small fonts",20),fill="white")
        progressbar = ttk.Progressbar(orient=tk.HORIZONTAL, length=900, mode='determinate',style="Horizontal.TProgressbar")
        progressbar.place(x=450,y=25)
        progressbar.start()
        if self.nxt_func != None :
            self.parent.after(5050,self.proceed)


if __name__ == '__main__' :
    root = ThemedTk("black")
    root["bg"] = "gray21"
    style = ttk.Style()
    style.configure("Horizontal.TProgressbar", foreground='gray21')
    app = SplashScreen(root,None)
    app.display()
    root.after(5050,root.destroy)
    root.mainloop()