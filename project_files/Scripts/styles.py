from tkinter import *
from tkinter.ttk import Style


# The styles
class Styles(Style) :
    def __init__(self,**kwargs) :
        Style.__init__(self,**kwargs)
        # the styles
        self.configure("var.TFrame",background="#424242")

        self.configure("text_btn.TButton",font=("terminal",15),cursor="@hand2",anchor=CENTER)
        self.map("text_btn.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("skip.TButton",font=("lucida console",23),width=6,height=3,cursor="@hand2",anchor=CENTER)
        self.map("death_pg.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])        

        self.configure("death_pg.TButton",font=("lucida console",15),width=15,height=1,cursor="@hand2",anchor=CENTER)
        self.map("death_pg.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("main.TButton",font=("lucida console",25,"bold"),width=15,height=1,cursor="@hand2")
        self.map("main.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("startpg_verify.TButton",font=("lucida console",20,"bold"),cursor="@hand2",width=18,height=15,anchor=CENTER)
        self.map("startpg_verify.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("start_pg.TButton",font=("lucida console",20,"bold"),cursor="@hand2",width=14,height=50,anchor=CENTER)
        self.map("start_pg.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("mssg.TButton",font=("bahnschrift semilight condensed",21),cursor="@hand2",width=12,height=26,anchor=CENTER)
        self.map("mssg.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("text.TLabel",background="white",font=("lucida console",15),foreground="black")

        self.configure("start_error.TLabel",font= ("bahnschrift semilight condensed",15))

        self.configure("main_pg.TLabel",font= ("bahnschrift semilight condensed",20))

        self.configure("start_text.TLabel",font=("consolas",19))

        self.configure("img.TLabel",background="#424242")

        self.configure("text.TFrame",background="#424242",width=515,height=360)

        self.configure("header.TFrame",background="#424242")

        self.configure("head_label.TLabel",background="#424242",font=("lucida console",20,"bold"))

        self.configure("death.TLabel",font=("lucida console",60,"bold"))
        
        self.configure("ptext1.TLabel",font=("bahnschrift semilight",25))

        self.configure("ptext2.TLabel",background="white",font=("bahnschrift",20),foreground="black")

        self.configure("pimage.TLabel",background="white",foreground="black")