import tkinter as tk
import tkinter.ttk as ttk


# The styles
class Styles(ttk.Style) :
    def __init__(self,**kwargs) :
        """Defining all the different widget styles."""
        ttk.Style.__init__(self,**kwargs)
        # the styles
        self.configure("var.TFrame",background="black")

        self.configure("text_btn.TButton",font=("terminal",15),cursor="@hand2",anchor=tk.CENTER,background="black",relief=tk.FLAT)
        self.map("text_btn.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("skip.TButton",font=("lucida console",23),width=6,height=3,cursor="@hand2",anchor=tk.CENTER,background="black",relief=tk.FLAT)
        self.map("skip.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("death_pg.TButton",font=("lucida console",15),width=15,height=1,cursor="@hand2",anchor=tk.CENTER,background="black",relief=tk.FLAT)
        self.map("death_pg.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("main.TButton",font=("lucida console",25,"bold"),width=15,height=1,cursor="@hand2",background="black",relief=tk.FLAT)
        self.map("main.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("startpg_verify.TButton",font=("lucida console",20,"bold"),cursor="@hand2",width=18,height=15,anchor=tk.CENTER,background="black",relief=tk.FLAT)
        self.map("startpg_verify.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("start_pg.TButton",font=("lucida console",20,"bold"),cursor="@hand2",width=14,height=50,anchor=tk.CENTER,background="black",relief=tk.FLAT)
        self.map("start_pg.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("mssg.TButton",font=("bahnschrift semilight condensed",21),cursor="@hand2",width=12,height=26,anchor=tk.CENTER,background="black",relief=tk.FLAT)
        self.map("mssg.TButton",
            foreground=[('pressed', 'black'), ('active', 'white')],
            background=[('pressed', 'black'), ('active', 'gray')])

        self.configure("text.TLabel",background="white",font=("lucida console",15),foreground="black")

        self.configure("start_error.TLabel",font= ("bahnschrift semilight condensed",15),background="black")

        self.configure("main_pg.TLabel",font= ("bahnschrift semilight condensed",20),background="black")

        self.configure("start_text.TLabel",font=("consolas",19),background="black")

        self.configure("img.TLabel",background="black")

        self.configure("text.TFrame",background="black",width=515,height=360)

        self.configure("header.TFrame",background="black")

        self.configure("head_label.TLabel",background="black",font=("lucida console",20,"bold"))

        self.configure("death.TLabel",font=("roboto",60,"bold"),background="black")

        self.configure("ptext1.TLabel",font=("bahnschrift semilight",25),background="black")

        self.configure("ptext2.TLabel",background="white",font=("bahnschrift",20),foreground="black")

        self.configure("pimage.TLabel",background="white",foreground="black")

        self.configure("creditshead1.TLabel",font=("HP Simplified Hans",25,"underline"),background="black")

        self.configure("creditshead2.TLabel",font=("bahnschrift",20,"underline"),background="black")

        self.configure("creditstext.TLabel",font=("bahnschrift",20,"italic"),background="black")

        self.configure("creditstext2.TLabel",font=("HP Simplified Hans",15),background="black")