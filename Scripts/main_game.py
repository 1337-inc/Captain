import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
from random import randint
from PIL import ImageTk,Image
from threading import Thread
import pickle
from Scripts.client import Client
from Scripts.music_player import m_player
from Scripts.splash_pg import SplashScreen
from Scripts.mybar import MyBar
from Scripts.vid_player import VideoPlayer
from Scripts.styles import Styles
from functools import partial


class GameData(Client) :
    """To Handle Game Data between Server and Client. """

    def __init__(self,parent:object) :
        """Initialize parent class Client in child class GameData."""
        Client.__init__(self)
        self.parent = parent

    def savedata(self) :
        if self.connected == True :
            game.const_num = 0
            game.save()
            self.send("Save Data")
            data_tup = pickle.dumps((game.NAME,game.CODE))
            self.client.send(data_tup)
            re_msg = self.recieve()
            if re_msg :
                if re_msg == "Available" :
                    self.send("Game Data")
                    #game = Game()
                    game_data = pickle.dumps(game)
                    self.client.send(game_data)
                    re_msg = self.recieve()
                    if re_msg == "Success" :
                        self.parent.s_msg("save")
                    else :
                        self.parent.s_msg("fail")
                else :
                    msg = self.parent.s_msg("ask_save")
                    if msg == "yes" :
                        self.send("Game Data")
                        #game = Game()
                        game_data = pickle.dumps(game)
                        self.client.send(game_data)
                        re_msg = self.recieve()
                        if re_msg == "Success" :
                            self.parent.s_msg("save")
                        else :
                            self.parent.s_msg("fail")
                    else :
                        self.send("Don't save")
        else :
            self.parent.s_msg("sconn_fail")

    def wipe_data(self) :
        if self.connected == True :
           self.send("Wipe")

    def load_data(self,name:str,code:str) :
        if self.connected == True :
            self.send("Load")
            self.client.send(pickle.dumps((name,code)))
            available = self.recieve()
            if available == "Present" :
                game_data = self.client.recv(5000)
                return available,game_data
            else :
                return available,None
        else :
            return None, None

    def end_con(self) :
        self.parent.destroy()
        if self.connected == True :
            self.end_conn()

    def check_data(self,name:str,code:str) :
        if self.connected :
            # checks whether player data already exists
            self.send("Check Data")
            data_tup = pickle.dumps((name,code))
            self.client.send(data_tup)
            re_msg = self.recieve()
            if re_msg == "Exists" :
                return "Exists"
            else :
                return "New"
        else :
            return None


class Root(ThemedTk) :
    """ The Tkinter Interface. """

    def __init__(self,**kwargs) :
        """Initialize parent class, ThemedTk, in child class, Root."""
        ThemedTk.__init__(self,theme="black",**kwargs)
        self.withdraw()
        # defining the menubar
        self.menu()
        # setup stuff goes here
        self.configure(bg = "#424242")
        self.columnconfigure(0,weight=1)
        self.title("Captain!!")
        self.iconbitmap("project_pics\\cap_desktop.ico")
        self.window_width = self.winfo_width()
        self.window_height = self.winfo_height()
        # side bar
        self.side_bar = ttk.Frame(self,height=700,width=120,style="var.TFrame")
        # defining the objects for the progress bars
        self.bar1 = MyBar(self.side_bar, shape="project_pics\\research.png", value=50, bg="#424242", trough_color='white', bar_color='gray54')
        self.bar2 = MyBar(self.side_bar, shape="project_pics\\man.png", value=50, bg="#424242", trough_color='lavender', bar_color='gray54')
        self.bar3 = MyBar(self.side_bar, shape="project_pics\\dollar.png", value=50, bg="#424242", trough_color='lavender', bar_color='gray54')
        self.bar4 = MyBar(self.side_bar, shape="project_pics\\sword.png", value=50, bg="#424242", trough_color='lavender', bar_color='gray54')
        # the exit protocol
        self.protocol("WM_DELETE_WINDOW",lambda: self.exit(leave=False))
        self.enter = True
        # Background image of existing page and its Canvas
        self.bg_image = None
        self.canvas_exists = True
        self.bg_canvas = tk.Canvas(self,bg="#424242",width=self.window_width,height=self.window_height)
        self.bg_canvas.bind('<Configure>',self.resizeimage)
        self.bg_img = self.bg_canvas.create_image(0, 0, anchor = tk.NW)

    def clear(self) :
        for widget in self.winfo_children() :
            if widget not in [self.side_bar, self.menubar, self.bg_canvas] :# is not self.side_bar and widget is not self.menubar :
                widget.destroy()
            else :
                widget.grid_forget()

    def resizeimage(self,*args) :
        self.window_width = self.winfo_width()
        self.window_height = self.winfo_height()
        img_size = (self.window_width,self.window_height)
        image = self.bg_image.resize(img_size)
        self.image1 = ImageTk.PhotoImage(image)
        self.bg_canvas.config(width=self.window_width,height=self.window_height)
        self.bg_canvas.itemconfig(self.bg_img,image = self.image1)

    def screen_config(self, width=1366, height=768) :
        setwinwidth = (self.window_width-width)//2
        setwinheight = (self.window_height-height)//2
        return f"{width}x{height}+{setwinwidth}+{setwinheight}"

    def connect_display(self) :
        def connect_server() :
            server_ip = code.get().strip()
            if server_ip != "" :
                connected = g_data.start_socket(server_ip)
            else :
                connected = True
            if connected :
                top_win.destroy()
            else :
                code.delete(0,"end")
                error.config(text="Sorry, please check the code and try again. If this problem persists,\n make sure that the server has been started.")

        top_win = tk.Toplevel(self)
        top_win.geometry("500x200")
        top_win.resizable(0,0)
        top_win.config(bg="#424242")
        # tk.Grid.columnconfigure(top_win,0,weight=1)
        lbl_text = ttk.Label(top_win,
                        text="To establish a connection with the server, please enter\n the code given in the server interface. \nIf you wish to play the game without connecting, \nsimply press the proceed button",
                        style = "creditstext2.TLabel")
        lbl_text.grid(row=0,column=0,columnspan=2,padx=20)
        lbl_entry = ttk.Label(top_win,text="Enter Code :",style="main_pg.TLabel")
        lbl_entry.grid(row=1,column=0,padx=25)
        code = ttk.Entry(top_win,width=16,font=("bahnschrift semilight condensed",20))
        code.grid(row=1,column=1,sticky=tk.W,padx=5)
        code.focus_force()
        error = ttk.Label(top_win,text=None)
        error.grid(row=2,columnspan=2)
        proceed = ttk.Button(top_win,text="Proceed",style="start_pg.TButton",command=connect_server)
        proceed.grid(row=2,columnspan=2,pady=20)

    def play_video(self,vid_file:str,music_file:str,nxt_func:object) :
        self.clear()
        vid_player.player(vid_file,music_file,nxt_func)

    def mssg_box(self) :
        def heaven() :
            # text to be displayed in the window
            img_btn.destroy()
            frame = ttk.Frame(mssgwin,width=width,height=height)
            frame.pack()
            ttk.Label(frame,text="   [System Message...]",style="start_text.TLabel").grid(row=0,column=0,sticky="new")
            ttk.Label(frame,text=f"[Important Message] Player {game.NAME} has \nmanaged to successfully eliminate all \nhuman lifeforms including himself.\n\t     GAME OVER",style="main_pg.TLabel").grid(row=1,column=0,pady=15)
            ttk.Button(mssgwin,text="dammit",command=mssgwin.destroy,style="mssg.TButton").place(relx=0.27,rely=0.78)
        # Toplevel window
        mssgwin = tk.Toplevel(self)
        mssgwin["bg"] = "#424242"
        mssgwin.title("[System Message...]")
        # opening background image
        img = Image.open("project_pics\\mail.png")
        width, height = img.size
        # set window dimentions
        mssgwin.geometry(f"{width+16}x{height}")
        mssgwin.resizable(0,0)
        img = ImageTk.PhotoImage(img)
        # Button
        img_btn = ttk.Button(mssgwin,image=img)
        img_btn.config(command=partial(heaven))
        img_btn.image = img
        img_btn.pack(anchor="nw")

    def menu(self) :
        def menu_help(help_type) :
            def credits_populate(frame):
                """ Putting in the lables in the credits page."""
                tk.Grid.columnconfigure(frame, 0, weight=1)
                # defining the lables and hardcoding in the credits page
                cap_title = ttk.Label(frame,text="Captain!!",style="death.TLabel")
                developed = ttk.Label(frame,text="Developed by 1337 incorporated",style="creditshead1.TLabel")
                team = ttk.Label(frame,text="OUR TEAM",style="creditshead2.TLabel")
                abhi = ttk.Label(frame,text="• Abhinand D Manoj        ",style="creditstext.TLabel")
                david = ttk.Label(frame,text="• David Tony Veliath       ",style="creditstext.TLabel")
                me = ttk.Label(frame,text="• Jovan George Zacharia",style="creditstext.TLabel")
                rahul = ttk.Label(frame,text="• Rahul Dinesh                 ",style="creditstext.TLabel")
                special = ttk.Label(frame,text="SPECIAL THANKS",style="creditshead2.TLabel")
                rinu = ttk.Label(frame,text="Mrs Rinu Mary Joy, our Teacher",style="creditstext.TLabel")
                parents = ttk.Label(frame,text="Our Parents and Friends",style="creditstext.TLabel")
                internet = ttk.Label(frame,text="The Internet",style="creditstext.TLabel")
                websites = ttk.Label(frame,text="WEBSITES",style="creditshead2.TLabel")
                stack = ttk.Label(frame,text="1. stackoverflow.com",style="creditstext.TLabel")
                programiz = ttk.Label(frame,text="2. programiz.com      ",style="creditstext.TLabel")
                reddit = ttk.Label(frame,text="3. reddit.com               ",style="creditstext.TLabel")
                w3school = ttk.Label(frame,text="4. w3school.com         ",style="creditstext.TLabel")
                geeks = ttk.Label(frame,text="5. geeksforgeeks.com",style="creditstext.TLabel")
                youtube = ttk.Label(frame,text="6. youtube.com            ",style="creditstext.TLabel")
                logo = ttk.Label(frame,text="7.Logomakr.com           ",style="creditstext.TLabel")
                music = ttk.Label(frame,text="MUSIC AND SOUND EFFECTS",style="creditshead2.TLabel")
                signal = ttk.Label(frame,text="Signal by drkmnd",style="creditstext.TLabel")
                motion1 = ttk.Label(frame,text="Sad Violin by MOTION ARRAY ",style="creditstext.TLabel")
                motion2 = ttk.Label(frame,text="Glitch sound effects by MOTION ARRAY ",style="creditstext.TLabel")
                star = ttk.Label(frame,text="Star Wars Theme Song By John Williams",style="creditstext.TLabel")
                video = ttk.Label(frame,text="VIDEO",style="creditshead2.TLabel")
                glitch = ttk.Label(frame,text="Game Over Glitch by MOTION ARRAY",style="creditstext.TLabel")
                crawl = ttk.Label(frame,text="Star Wars Intro Creator by Kassel Labs",style="creditstext.TLabel")
                label = ttk.Label(frame,text="   \n")
                grp_name = ttk.Label(frame,text="1337 INCORPORATED",style="creditstext2.TLabel")
                rights = ttk.Label(frame,text="ALL RIGHTS RESERVED",style="creditstext2.TLabel")
                cap = ttk.Label(frame,text="Captain!! IS A TRADEMARK OF 1337 ",style="creditstext2.TLabel")
                license_ = ttk.Label(frame,text="INCORPORATED IN INDIA, USED UNDER",style="creditstext2.TLabel")
                grp = ttk.Label(frame,text="LICENSE BY 1337 INCORPORATED ENTERTAINMENT",style="creditstext2.TLabel")
                # placingthe lables
                cap_title.grid(row=0,column=0,padx=40,pady=15)
                developed.grid(row=1,column=0,pady=10,padx=10)
                team.grid(row=2,column=0,pady=20,sticky=tk.S)
                abhi.grid(row=3,column=0)
                david.grid(row=4,column=0,pady=5)
                me.grid(row=5,column=0,pady=5)
                rahul.grid(row=6,column=0,pady=5)
                special.grid(row=7,column=0,pady=20,sticky=tk.S)
                rinu.grid(row=8,column=0)
                parents.grid(row=9,column=0,pady=5)
                internet.grid(row=10,column=0,pady=5)
                websites.grid(row=11,column=0,pady=20,sticky=tk.S)
                stack.grid(row=12,column=0)
                programiz.grid(row=13,column=0,pady=5)
                reddit.grid(row=14,column=0,pady=5)
                w3school.grid(row=15,column=0,pady=5)
                geeks.grid(row=16,column=0,pady=5)
                youtube.grid(row=17,column=0,pady=5)
                logo.grid(row=18,column=0,pady=5)
                music.grid(row=19,column=0,pady=20,sticky=tk.S)
                signal.grid(row=20,column=0)
                motion1.grid(row=21,column=0,pady=5)
                motion2.grid(row=22,column=0,pady=5)
                star.grid(row=23,column=0,pady=5)
                video.grid(row=24,column=0,pady=20,sticky=tk.S)
                glitch.grid(row=25,column=0)
                crawl.grid(row=26,column=0,pady=5)
                label.grid(row=27,column=0,pady=10)
                grp_name.grid(row=28,column=0,pady=5)
                rights.grid(row=29,column=0,pady=5)
                cap.grid(row=30,column=0,pady=5)
                license_.grid(row=31,column=0,pady=5)
                grp.grid(row=32,column=0,pady=5)

            def about_populate(frame) :
                """Putting in the text box in the about page."""
                tk.Grid.columnconfigure(frame, 0, weight=1)
                cap_title = ttk.Label(frame,text="Captain!!",style="death.TLabel")
                cap_title.grid(row=0,column=0,padx=40,pady=30)
                # the text to display in text box
                text1 = "CAPTAIN IS A FREE TO PLAY, CHOICE-BASED GAME WHERE THE PLAYER HAS 2 CHOICES TO ANSWER THE GIVEN QUESTIONS AND WORK THEIR WAY TO REACH THE FINAL ENDING OF THE GAME, WHILE STAYING IN POWER.THERE ARE ALSO 20+ DIFFERENT ENDINGS THAT YOU CAN ENCOUNTER IN THE GAME, DEPENDING ON THE CHOICES YOU MAKE."
                text2 = "\n\nFIND YOUR WAY THROUGH THE GAME TO REACH THE FINAL ENDING OR UNCOVER DIFFERENT ENDINGS OF THE GAME AS YOU PLAY, WHILE YOU ARE IN POWER."
                text3 = "\n\n\n\nNOTE: CAPTAIN!! REQUIRES YOU TO START THE SERVER APPLICATION, SEPERATELY WITH THE GAME (INSTALLED WITH THE GAME) INORDER TO SAVE YOUR PROGRESS IN THE GAME."
                text4 = "\n\n\n\nHOW TO PLAY:"
                text5 = "\n\n• THE AIM OF THE GAME IS SIMPLE: TO CHOOSE ANY OF THE 2 OPTIONS (THAT YOU THINK IS RIGHT) FOR THE GIVEN QUESTIONS AND TRY TO DISCOVER THE FINAL ENDING AMONG THE DIFFERENT POSSIBLE ENDINGS OF THE GAME."
                text6 = "\n\n• WHILE DECIDING TO CHOOSE AN OPTION FOR A GIVEN QUESTION, THE PLAYER HAS TO KEEP TRACK OF THE PROGRESS METER/BAR METER LOCATED ON THE RIGHT SIDE OF THE GAME."
                text7 = "\n\n• THE PLAYER STATUS TELLS YOU THE NUMBER OF DAYS YOU HAVE BEEN IN POWER.EACH DAY IS CALCULATED PER QUESTION. ONCE YOU DIE AND RESPAWN, YOUR PLAYER STATUS WILL RESTART TO 'DAYS IN POWER: 1'."
                text8 = "\n\nYOUR HIGHSCORE IS CALCULATED BY KEEPING TRACK OF YOUR PLAYER STATUS. SO TRY TO SURVIVE FOR AS LONG AS YOU CAN!"
                text9 = "\n\n\n\nTHE PROGRESS METER/BAR METER KEEPS A TRACK ON HOW WELL YOU ARE SERVING EACH SECTOR OF THE SOCIETY."
                text10 = "\n\nTHE 4 PROGRESS METERS ARE: "
                text11 = "\n\n1) RESEARCH PROGRESS METER"
                text12 = "\n\n2) COMMON PUBLIC PROGRESS METER"
                text13 = "\n\n3) TREASURY/MONEY PROGRESS METER"
                text14 = "\n\n4) ARMY PROGRESS METER"
                text15 = "\n\nTHE PLAYER HAS TO KEEP THE 4 BARS BALANCED WHILE CHOOSING THE APPROPRIATE/LOGICAL OPTIONS FOR A GIVEN QUESTION AND MUST MAKE SURE THAT NONE OF THE BARS BECOME FULL OR EMPTY."
                text16 = "\n\nIN CASE ANY OF THE 4 BARS BECOME FULL OR EMPTY, YOU WILL IMMEDIATELY LOSE THE GAME."
                text17 = "\n\n\n\nTRY TO STAY IN POWER AS LONG AS YOU CAN, DISCOVER THE ULTIMATE ENDING AMONG THE DIFFERENT ENDINGS IN THE GAME, AND SHOW YOUR FELLOW CAPTAINS WHO THE REAL CAPTAIN IS!"
                # adding \n wherever required
                text1 = game.checkstr(text1, 70)
                text2 = game.checkstr(text2, 70)
                text3 = game.checkstr(text3, 70)
                text4 = game.checkstr(text4, 70)
                text5 = game.checkstr(text5, 70)
                text6 = game.checkstr(text6, 70)
                text7 = game.checkstr(text7, 70)
                text8 = game.checkstr(text8, 70)
                text9 = game.checkstr(text9, 70)
                text10 = game.checkstr(text10, 70)
                text11 = game.checkstr(text11, 70)
                text12 = game.checkstr(text12, 70)
                text13 = game.checkstr(text13, 70)
                text14 = game.checkstr(text14, 70)
                text15 = game.checkstr(text15, 70)
                text16 = game.checkstr(text16, 70)
                text17 = game.checkstr(text17, 70)
                # Determining line number of text
                text1_line = "1.0"
                text2_line = str(text1.count("\n") + 2) + ".0"
                text3_line = str(text2.count("\n") + int(float(text2_line))) + ".0"
                text4_line = str(text3.count("\n") + int(float(text3_line))) + ".0"
                text5_line = str(text4.count("\n") + int(float(text4_line))) + ".0"
                text6_line = str(text5.count("\n") + int(float(text5_line))) + ".0"
                text7_line = str(text6.count("\n") + int(float(text6_line))) + ".0"
                text8_line = str(text7.count("\n") + int(float(text7_line))) + ".0"
                text9_line = str(text8.count("\n") + int(float(text8_line))) + ".0"
                text10_line = str(text9.count("\n") + int(float(text9_line))) + ".0"
                text11_line = str(text10.count("\n") + int(float(text10_line))) + ".0"
                text12_line = str(text11.count("\n") + int(float(text11_line))) + ".0"
                text13_line = str(text12.count("\n") + int(float(text12_line))) + ".0"
                text14_line = str(text13.count("\n") + int(float(text13_line))) + ".0"
                text15_line = str(text14.count("\n") + int(float(text14_line))) + ".0"
                text16_line = str(text15.count("\n") + int(float(text15_line))) + ".0"
                text17_line = str(text16.count("\n") + int(float(text16_line))) + ".0"
                # Creating text widget and insterting text into it
                text = tk.Text(frame,bg="#424242",width=108,height=50,relief=tk.FLAT)
                text.insert(text1_line, text1)
                text.insert(text2_line, text2)
                text.insert(text3_line, text3)
                text.insert(text4_line, text4)
                text.insert(text5_line, text5)
                text.insert(text6_line, text6)
                text.insert(text7_line, text7)
                text.insert(text8_line, text8)
                text.insert(text9_line, text9)
                text.insert(text10_line, text10)
                text.insert(text11_line, text11)
                text.insert(text12_line, text12)
                text.insert(text13_line, text13)
                text.insert(text14_line, text14)
                text.insert(text15_line, text15)
                text.insert(text16_line, text16)
                text.insert(text17_line, text17)
                text.grid(sticky="nsew",pady=20)
                # adding tags according to previously determined line numbers
                text.tag_add("1", "1.0", text2_line)
                text.tag_add("2", str(float(text2_line)+1), text3_line)
                text.tag_add("3", str(float(text3_line)+1), text4_line)
                text.tag_add("4", str(float(text4_line)+1), text5_line)
                text.tag_add("5", str(float(text5_line)+1), text6_line)
                text.tag_add("6", str(float(text6_line)+1), text7_line)
                text.tag_add("7", str(float(text7_line)+1), text8_line)
                text.tag_add("8", str(float(text8_line)+1), text9_line)
                text.tag_add("9", str(float(text9_line)+1), text10_line)
                text.tag_add("10", str(float(text10_line)+1), text11_line)
                text.tag_add("11", str(float(text11_line)+1), text12_line)
                text.tag_add("12", str(float(text12_line)+1), text13_line)
                text.tag_add("13", str(float(text13_line)+1), text14_line)
                text.tag_add("14", str(float(text14_line)+1), text15_line)
                text.tag_add("15", str(float(text15_line)+1), text16_line)
                text.tag_add("16", str(float(text16_line)+1), text17_line)
                text.tag_add("17", str(float(text17_line)+1), tk.END)
                # configuring tags
                text_font = ("HP Simplified Hans",18)
                heading_font = ("bahnschrift",18,"underline","bold")
                custom_font1 = ("bahnschrift",18,"bold")
                text.tag_config("1", foreground="white", font=text_font)
                text.tag_config("2", foreground="white", font=text_font)
                text.tag_config("3", foreground="white", font=custom_font1)
                text.tag_config("4", foreground="white", font=heading_font)
                text.tag_config("5", foreground="white", font=text_font)
                text.tag_config("6", foreground="white", font=text_font)
                text.tag_config("7", foreground="white", font=text_font)
                text.tag_config("8", foreground="white", font=text_font)
                text.tag_config("9", foreground="white", font=text_font)
                text.tag_config("10", foreground="white", font=text_font)
                text.tag_config("11", foreground="white", font=custom_font1)
                text.tag_config("12", foreground="white", font=custom_font1)
                text.tag_config("13", foreground="white", font=custom_font1)
                text.tag_config("14", foreground="white", font=custom_font1)
                text.tag_config("15", foreground="white", font=text_font)
                text.tag_config("16", foreground="white", font=custom_font1)
                text.tag_config("17", foreground="white", font=text_font)
                text.configure(state=tk.DISABLED)

            def onFrameConfigure(canvas):
                """Reset the scroll region to encompass the inner frame."""
                canvas.configure(scrollregion=canvas.bbox("all"))

            def on_mousewheel(event):
                """Enables scroll with the mousewheel."""
                shift = (event.state & 0x1) != 0
                scroll = -1 if event.delta > 0 else 1
                if shift:
                    canvas.xview_scroll(scroll, "units")
                else:
                    canvas.yview_scroll(scroll, "units")

            window = tk.Toplevel(self)
            window["bg"] = "#424242"
            window.title("Credits")
            window.resizable(0,0)
            if help_type == "Credits" :
                width, height = 500, 500
            else :
                width, height = 870, 600
            canvas = tk.Canvas(window, background="#424242", width=width, height=height)
            canvas.bind_all("<MouseWheel>", on_mousewheel)
            frame = ttk.Frame(canvas)
            vsb = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=vsb.set)

            vsb.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((4,4), window=frame, anchor="nw")

            frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

            if help_type == "Credits" :
                credits_populate(frame)
            else :
                about_populate(frame)

        def profile() :
            profile = tk.Toplevel(self)
            profile.title("Player Profile")
            profile.resizable(0,0)
            profile.geometry("500x500")
            profile["bg"] = "#424242"
            # Text box
            text_box = Image.open("project_pics\\text_box1.png")
            width,height = text_box.size
            text_box = ImageTk.PhotoImage(text_box)
            frame = ttk.Frame(profile,width=width,height=height,style="pframe.TFrame")
            frame.place(relx=0.5,rely=0.55,anchor=tk.CENTER)
            frame.grid_propagate(False)
            txt_box = ttk.Label(frame,image=text_box)
            txt_box.image = text_box
            txt_box.grid()
            # opening images
            player = Image.open("project_pics\\player.png")
            score = Image.open("project_pics\\score.png")
            highscore = Image.open("project_pics\\High_score.png")
            # converting images into tkinter displayable format
            player = ImageTk.PhotoImage(player)
            score = ImageTk.PhotoImage(score)
            highscore = ImageTk.PhotoImage(highscore)
            # Lables to display images
            player_lbl = ttk.Label(frame,image=player,style="pimage.TLabel")
            score_lbl = ttk.Label(frame,image=score,style="pimage.TLabel")
            highscore_lbl = ttk.Label(frame,image=highscore,style="pimage.TLabel")
            # Saving a reference of the images
            player_lbl.image = player
            score_lbl.image = score
            highscore_lbl.image = highscore
            # Displaying the images
            player_lbl.place(relx=0.1,rely=0.15)
            score_lbl.place(relx=0.1,rely=0.45)
            highscore_lbl.place(relx=0.1,rely=0.75)
            # Texts
            ttk.Label(profile,text="[Player Profile Generating...]",style="ptext1.TLabel").place(relx=0.5,rely=0.1,anchor=tk.CENTER)
            ttk.Label(frame,text=f"Player : {game.NAME}",style="ptext2.TLabel").place(relx=0.35,rely=0.19)
            ttk.Label(frame,text=f"Current Score : {game.score}",style="ptext2.TLabel").place(relx=0.35,rely=0.48)
            ttk.Label(frame,text=f"High Score : {game.high_score}",style="ptext2.TLabel").place(relx=0.35,rely=0.79)

        self.menubar = tk.Menu(self)
        # The Game Menu
        gamebar = tk.Menu(self.menubar,tearoff=0,bg="gray15",fg="white",activebackground="#424242")
        gamebar.add_command(label="Player Profile",command=profile)
        gamebar.add_command(label="Save data",command=partial(self.s_msg,"e_save"))
        gamebar.add_separator()
        gamebar.add_command(label="Quit",command=partial(self.exit,False))
        self.menubar.add_cascade(label="Game",menu=gamebar)
        # The About Menu
        aboutmenu = tk.Menu(self.menubar,tearoff=0,bg="gray15",fg="white",activebackground="#424242")
        aboutmenu.add_command(label="Credits",command=partial(menu_help,help_type="Credits"))
        aboutmenu.add_command(label="About",command=partial(menu_help,help_type="About"))
        self.menubar.add_cascade(label="Help",menu=aboutmenu)
        # The Server Menu
        servermenu = tk.Menu(self.menubar,tearoff=0,bg="gray15",fg="white",activebackground="#424242")
        servermenu.add_command(label="Connect to Server",command=self.connect_display)
        self.menubar.add_cascade(label="Server",menu=servermenu)

    def btn_click(self,nxt_func:object) :
        btn_thread = Thread(target=m_player.music_control,args=("project_media\\button_sound.ogg",False,0,1))
        btn_thread.start()
        btn_thread.join()
        if nxt_func == "Starting_game_again" :
            m_player.music_control("project_media\\signal.ogg",True,-1,0)
            m_player.music_control("project_media\\signal.ogg",False,-1,0)
            nxt_func = self.main_page
        nxt_func()

    def exit(self,leave:bool) :
        if game.saved == True or leave or game.q_done == [] or g_data.connected == False :
            msg = messagebox.askquestion("Thank you for playing","Are you sure you want to exit?")
            if msg == "yes" :
                if g_data.connected == True :
                    g_data.end_conn()
                self.destroy()
        else :
            self.s_msg("exit")

    def load_page(self) :
        self.enter = False
        self.clear()
        self.bg_image = Image.open("project_pics\\start_pg.png")
        bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_canvas.itemconfig(self.bg_img,image=bg_image)
        self.bg_canvas.image = bg_image
        self.resizeimage()
        self.bg_canvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        # frame and text
        frame = ttk.Frame(self,width=500,height=400,style="start.TFrame")
        frame.grid_propagate(0)
        frame.place(relx=0.325,rely=0.2)
        ttk.Label(frame,text="[System Initiating...]",style="start_text.TLabel").grid(row=0,column=0,pady=30,padx=30,sticky="w",columnspan=2)
        ttk.Label(frame,text="[Creating Player Environment...]",style="start_text.TLabel").grid(row=1,column=0,padx=30,sticky="w",columnspan=2)
        ttk.Label(frame,text="Enter player name: ",style="main_pg.TLabel").grid(row=2,column=0,pady=40,padx=30,sticky="w")
        name = ttk.Entry(frame,width=16,font=("bahnschrift semilight condensed",20))
        name.grid(row=2,column=1,sticky="w")
        name.focus_force()
        ttk.Label(frame,text="Enter player pass-code: ",style="main_pg.TLabel").grid(row=3,column=0,padx=30,sticky="w")
        code = ttk.Entry(frame,width=16,font=("bahnschrift semilight condensed",20))
        code.grid(row=3,column=1,sticky="w")

        ttk.Button(self,text="Back",style="start_pg.TButton",command=partial(self.btn_click,self.main_page)).place(relx=0.324,rely=0.76,height=100)
        ttk.Button(self,text="Load",style="start_pg.TButton",command=partial(self.btn_click,partial(game.load,name,code))).place(relx=0.509,rely=0.76,height=100)

    def s_msg(self,mssg_type:str) :
        if mssg_type == "fail" :
            messagebox.showerror("ERROR","Sorry, your game data could not be saved. Please report a bug if you see this")
        elif mssg_type =="ask_save" :
            msg = messagebox.askquestion("Save?","You already have a saved state. Are you sure you want to overwrite this? You previous progress will be lost.")
            return(msg)
        elif mssg_type == "save" :
            messagebox.showinfo("Saved","Your progress has been saved")
        elif mssg_type == "exit" :
            msg = messagebox.askquestion("Warning!","Are you want to leave without saving your progress?")
            if msg == "yes" :
                self.exit(True)
            else :
                msg = messagebox.askquestion("Save?","Save Progress?")
                if msg == "yes" :
                    g_data.savedata()
                    self.exit(True)
        elif mssg_type == "l_fail" :
            msg = messagebox.showerror("ERROR","You do not have a saved state")
        elif mssg_type == "e_save" :
            msg = messagebox.askquestion("Save?","Do you want to save your progress?")
            if msg == "yes"  :
                if game.NAME :
                    g_data.savedata()
                else :
                    self.s_msg("n_state")
        elif mssg_type == "l_tru" :
            msg = messagebox.showinfo("Loaded","Your game state has been loaded. You will be redirected to your reset point")
            if msg == "ok" :
                game.const_qn()
        elif mssg_type == "sconn_fail" :
            msg = messagebox.showerror("ERROR","Sorry, we could not save your data because you are not connected to the server. Please report a bug if you see this")
        elif mssg_type == "lconn_fail" :
            msg = messagebox.showerror("ERROR","Sorry, we could not load your data because you are not connected to the server. Please report a bug if you see this")
        elif mssg_type == "game_over" :
            msg = messagebox.showinfo("Loaded","Congrats! You seem to have already reached your destiny. To try again, please create a new avatar and start a new game")
        elif mssg_type == "n_state" :
            msg = messagebox.showerror("Sorry","Sorry, you do not have a game state yet. Start a new game or load your game state and try again")
        elif mssg_type == "data_exists" :
            msg = messagebox.showerror("Error","You already have a game state with the same name and code. Please load your game data in the load page or enter a new name and code if you wish to start a new game")
        elif mssg_type == "c-conn_fail" :
            msg = messagebox.showwarning("Warning","You are playing offline right now. So your data will be temporary and would not be accessable later")

    def proceed(self,parent:object,name:object,code:object) :    # partial(root.btn_click,partial(game.sequence,sequence="Opening"))
        if name.get() != "" and code.get() != "" : #lambda: vid_player.player("project_media\\starwarscrawl.mp4","project_media\\starwarstrack.ogg",lambda : game.sequence(sequence="Opening"))
            proceed_btn = partial(root.btn_click,lambda: self.play_video("project_media\\starwarscrawl.mp4","project_media\\starwarstrack.ogg",lambda : game.sequence(sequence="Opening")))
            exists = g_data.check_data(name.get(),code.get())
            if exists != "Exists" and exists is not None :
                ttk.Button(self,text="Proceed",style="start_pg.TButton",command=partial(self.btn_click,proceed_btn)).place(relx=0.509,rely=0.76,height=100)
                game.NAME = name.get()
                game.CODE = code.get()
            elif exists is None :
                ttk.Button(self,text="Proceed",style="start_pg.TButton",command=partial(self.btn_click,proceed_btn)).place(relx=0.509,rely=0.76,height=100)
                game.NAME = name.get()
                game.CODE = code.get()
                root.s_msg("c-conn_fail")
            else :
                root.s_msg("data_exists")
        else :
            ttk.Label(parent,text="[Error]... Player must have a name and code",style="main_pg.TLabel").grid(row=4,columnspan=2)

    def start_page(self) :
        self.clear()
        self.enter = False
        # background image
        self.bg_image = Image.open("project_pics\\start_pg.png")
        bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_canvas.itemconfig(self.bg_img,image=bg_image)
        self.bg_canvas.image = bg_image
        self.resizeimage()
        self.bg_canvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        # frame and text
        frame = ttk.Frame(self,width=500,height=400,style="header.TFrame")
        frame.grid_propagate(0)
        frame.place(relx=0.325,rely=0.2)
        ttk.Label(frame,text="[System Initiating...]",style="start_text.TLabel").grid(row=0,column=0,pady=30,padx=30,sticky="w",columnspan=2)
        ttk.Label(frame,text="[Creating Player Environment...]",style="start_text.TLabel").grid(row=1,column=0,padx=30,sticky="w",columnspan=2)
        ttk.Label(frame,text="Enter player name: ",style="main_pg.TLabel").grid(row=2,column=0,pady=40,padx=30,sticky="w")
        ttk.Label(frame,text="\t\t\t",style="start_error.TLabel").grid(row=4,columnspan=2)
        name = ttk.Entry(frame,width=16,font=("bahnschrift semilight condensed",20)) # ,style="entry.TEntry"
        name.grid(row=2,column=1,sticky="w")
        name.focus_force()
        ttk.Label(frame,text="Create player pass-code: ",style="main_pg.TLabel").grid(row=3,column=0,padx=30,sticky="w")
        code = ttk.Entry(frame,width=16,font=("bahnschrift semilight condensed",20))
        code.grid(row=3,column=1,sticky="w")
        # Buttons
        ttk.Button(frame,text="Verify",style="startpg_verify.TButton",command=partial(self.btn_click,partial(self.proceed,frame,name,code))).grid(row=5,column=0,columnspan=2,pady=15,padx=10,ipady=10)
        ttk.Button(self,text="Back",style="start_pg.TButton",command=partial(self.btn_click,self.main_page)).place(relx=0.324,rely=0.76,height=100)

    def main_page(self) :
        if self.canvas_exists == False :
            self.bg_canvas = tk.Canvas(self,width=self.window_width,height=self.window_height,bg="#424242")
            self.bg_canvas.bind('<Configure>',self.resizeimage)
        self.clear()
        self.bg_image = Image.open('project_pics\\main_pg.png')
        bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_canvas.itemconfig(self.bg_img,image=bg_image)
        self.bg_canvas.image = bg_image
        self.resizeimage()
        self.bg_canvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        start_btn = ttk.Button(self,text="Start New Game",style="main.TButton",command=partial(self.btn_click,self.start_page))
        start_btn.place(relx=0.9,rely=0.35,anchor=tk.CENTER,width=386,height=100)
        load_btn = ttk.Button(self,text="Load Game",style="main.TButton",command=partial(self.btn_click,self.load_page))
        load_btn.place(relx=0.9,rely=0.5,anchor=tk.CENTER,width=386,height=100)
        quit_btn = ttk.Button(self,text="Quit",style="main.TButton",command=partial(self.btn_click,partial(self.exit,False)))
        quit_btn.place(relx=0.9,rely=0.65,anchor=tk.CENTER,width=386,height=100)
        if self.enter :
            self.connect_display()

    def game_over_pg(self,d_text:str,d_str:str) :
        print("entered root.game_over_pg")
        self.clear()
        # adding \n wherever required
        d_text = game.checkstr(d_text,30)
        # stopping current music and plying new one
        m_player.music_control("project_media\\signal.ogg",True,-1,0)
        m_player.music_control("project_media\\game_over.ogg",False,-1,0)
        # header frame
        header_frame = ttk.Frame(self,height=30,width=1280,style="header.TFrame")
        header_frame.grid(row=0,columnspan=2,sticky=tk.E+tk.N+tk.W)
        ttk.Label(header_frame,text="Player: Capt. "+game.NAME,style="head_label.TLabel").place(relx=0.12) # 0.15
        ttk.Label(header_frame,text="Player Status: "+str(game.score)+" Days in power",style="head_label.TLabel").place(relx=0.55)
        if d_str != "death_end" :
            # side bar
            self.side_bar.place(relx=0.92,anchor="n")
            # displaying the progress bar widgets on the screen
            self.bar1.place(rely=0.2)
            self.bar2.place(rely=0.4)
            self.bar3.place(rely=0.6)
            self.bar4.place(rely=0.8)
        # logo
        logo_img = Image.open("project_pics\\cap_logo_invert.PNG")
        logo_new = ImageTk.PhotoImage(logo_img)
        logo_image = ttk.Label(self,image=logo_new,style="img.TLabel")
        logo_image.image = logo_new
        logo_image.place(relx=0.01,rely=0.07)
        # text box
        ttk.Label(self,text="YOU DIED..",style="death.TLabel").place(relx=0.33,rely=0.1)
        img = Image.open("project_pics\\text_box1.png")
        img_new = ImageTk.PhotoImage(img)
        text_frame = ttk.Frame(self,style="text.TFrame")
        img_label = ttk.Label(text_frame,image=img_new,style="img.TLabel")
        img_label.image = img_new
        img_label.pack(fill=tk.BOTH)
        ttk.Label(text_frame,text=d_text,style="text.TLabel").place(relx=0.5,rely=0.55,anchor=tk.CENTER)
        text_frame.place(relx=0.35,rely=0.25)
        if d_str != "death_end" :
            nxt_func = game.const_qn
            btn_func = partial(self.play_video,"project_media\\glitch.mp4","project_media\\glitch.ogg",nxt_func)
        else :
            game.game_over = True
            self.canvas_exists = True
            btn_func = "Starting_game_again"
            game.data_reset() # partial(vid_player.player,"project_media\\glitch.mp4","project_media\\glitch.ogg",func)
        ttk.Button(self,text="Continue",style="death_pg.TButton",command=partial(self.btn_click,btn_func)).place(relx=0.6,rely=0.8,width=250,height=80)
        if d_str != "death_end" and g_data.connected :
            g_data.savedata()
        elif d_str == "death_end" :
            self.mssg_box()

    def qn_page(self,char_name:str,qn:str,ans1:str,ans2:str,btn1_func:object,btn2_func:object,bar_dis:bool) :
        print("entered root.qn_page")
        self.clear()
        tk.Grid.columnconfigure(self,0,weight=1)
        # Adding \n to the text to display so as to fit them in the widgets
        ans1 = game.checkstr(text=ans1,index=30)
        ans2 = game.checkstr(text=ans2,index=30)
        qn = game.checkstr(text=qn,index=30)
        # header bar
        header_frame = ttk.Frame(self,height=30,width=1280,style="header.TFrame")
        header_frame.grid(row=0,columnspan=2,sticky=tk.E+tk.N+tk.W)
        ttk.Label(header_frame,text="Player: Capt. "+game.NAME,style="head_label.TLabel").place(relx=0.12) # 0.15
        ttk.Label(header_frame,text="Player Status: "+str(game.score)+" Days in power",style="head_label.TLabel").place(relx=0.5)
        # display game logo on left of screen
        logo_img = Image.open("project_pics\\cap_logo_invert.PNG")
        logo_new = ImageTk.PhotoImage(logo_img)
        logo_image = ttk.Label(self,image=logo_new,style="img.TLabel")
        logo_image.image = logo_new
        logo_image.place(relx=0.01,rely=0.07) # .grid(row=0,column=0,sticky=W+S)
        # open image to display as container for text
        img = Image.open("project_pics\\text_box1.png")
        img_new = ImageTk.PhotoImage(img)
        # create frame to display the container pic and the text
        text_frame = ttk.Frame(self,style="text.TFrame")
        border = ttk.Label(text_frame,image=img_new,style="img.TLabel")
        border.image = img_new
        border.pack(fill=tk.BOTH)
        # condition to display the side bar and image
        if bar_dis == True :
            # placing text frame
            text_frame.place(relx=0.5,rely=0.15)
            # character image
            if char_name == "???" :
                char = "Joe"
            else :
                char = char_name
            img = ImageTk.PhotoImage(image=Image.open(f"project_pics\\char_pics\\{char}.PNG"))
            char_image = ttk.Label(self,image=img,style="img.TLabel")
            char_image.image = img
            char_image.place(relx=0.18,rely=0.25)
            # side bar
            self.side_bar.place(relx=0.92,rely=0.005) # .grid(row=0,columnspan=3,sticky=N+S+E)
            # setting values in the custom progress bars
            self.bar1.value = game.r_cur[1][1]
            self.bar2.value = game.c_cur[1][1]
            self.bar3.value = game.i_cur[1][1]
            self.bar4.value = game.m_cur[1][1]
            # displaying the progress bar widgets on the screen
            self.bar1.place(rely=0.2)
            self.bar2.place(rely=0.4)
            self.bar3.place(rely=0.6)
            self.bar4.place(rely=0.8)
        elif bar_dis == "sequence" :
            self.const_qn()
        else :
            text_frame.place(relx=0.35,rely=0.15)
        # check if char_name to be displayed
        if char_name != None :
            char_name += " :"
        # display text over image
        label1 = ttk.Label(text_frame,text=char_name,style="text.TLabel")
        label1.place(relx=0.5,rely=0.1,anchor=tk.CENTER)
        label2 = ttk.Label(text_frame,text=qn,style="text.TLabel")
        label2.place(relx=0.5,rely=0.55,anchor=tk.CENTER)
        # displaying the buttons on the screen
        if ans1 != "" :
            print("button 1")
            btn1 = ttk.Button(self,text=ans1,style="text_btn.TButton",command=partial(self.btn_click,btn1_func))
            btn1.place(relx=0.17,rely=0.8,anchor=tk.W,width=386,height=150)
        print("button 2")
        print(btn2_func)
        btn2 = ttk.Button(self,text=ans2,style="text_btn.TButton",command=partial(self.btn_click,btn2_func))
        btn2.place(relx=0.81,rely=0.8,anchor=tk.E,width=386,height=150)


class Game :
    """ Game logic and data handle. """

    def __init__(self) :
        """Initialize all game variables."""
        self.NAME = None
        self.CODE = None
        self.m_cur = {1:["death_Military1",55,"death_Military2"]}
        self.c_cur = {1:["death_People1",55,"death_People2"]}
        self.r_cur = {1:["death_Research1",55,"death_Research2"]}
        self.i_cur = {1:["death_Industrial1",55,"death_Industrial2"]}
        self.q_list = ["a"]
        self.q_done = []
        self.qn_num = 0      # qn_num of qn to be displayed
        self.qn_file = 152   # max number of questions in main file
        self.direct_qns = 1  # reference of current qn in direct file
        self.direct_max = 20 # max number of questions in direct file
        self.direct_prev = 0 # reference of previous direct chain
        self.const_num = 0   # qn_num of constant question
        self.seq_num = 0     # qn_num of sequence text
        self.saved = False   # track of whether game has a saved state
        self.score  = 0      # track of your score
        self.high_score = 0  # highscore
        self.dead = 0        # number of times you have died
        self.death_str = ""
        self.game_over = False

    def save(self) :
        self.saved = True

    def main(self):
        root.overrideredirect(False)
        root.config(menu=root.menubar)
        root.window_width = root.winfo_width()
        root.window_height = root.winfo_height()
        root.main_page()

    def load(self,name:object,code:object) :
        global game
        name,code = name.get(),code.get()
        saved,game_data = g_data.load_data(name,code)
        if saved == "Present" :
            game_inst = pickle.loads(game_data)
            game = game_inst
            game.game_over = False
            self.saved = True
            if self.game_over and self.NAME != "jovan" :
                root.s_msg("game_over")
            else :
                root.s_msg("l_tru")
        elif saved is None and game_data is None :
            root.s_msg("lconn_fail")
        else :
            root.s_msg("l_fail")

    def var_check(self,x_cur:dict):
        if x_cur[1][1]<=5 :
            print("entered game.var_check inside first condition")
            print(f"variable death: {x_cur}")
            death_params = self.game_over_dict(x_cur,death_type="first")
            return death_params
        elif x_cur[1][1]>=100 :
            print("entered game.var_check inside second condition")
            print(f"variable death: {x_cur}")
            death_params = self.game_over_dict(x_cur,death_type="second")
            return death_params
        else :
            return None

    def game_over_str(self,x_str:str) :
        print(f"x_str : {x_str}")
        print("entered game.game_over_str")
        iteration = 0
        if self.high_score < self.score :
            self.high_score = self.score
        with open("project_data\\death.txt") as d_file :
            d_list = d_file.readlines()
        for line in d_list :
            iteration += 1
            d_str = line.strip().split("$")[0]
            if d_str == x_str :
                d_num = iteration
                break
        d_text = d_list[d_num-1].strip().split("$")[1]
        # self.game_over_pg(d_text,d_str)
        return d_text

    def game_over_dict(self,x_str:dict,death_type:str) :
        print(f"x_str : {x_str}")
        print("entered game.game_over_dict")
        iteration = 0
        if self.high_score < self.score :
            self.high_score = self.score
        if death_type == "first" :
            x_str = x_str[1][0]
        else :
            x_str = x_str[1][2]
        with open("project_data\\questions_file.txt") as q_file :
            q_list = q_file.readlines()
        print(f"x_str is {x_str}")
        for line in q_list :
            iteration += 1
            q_str = line.strip().split("$")[1]
            print(f"q_str is : {q_str}")
            if q_str == x_str :
                q_num = iteration
                break
        q_text = q_list[q_num-1].strip().split("$")[3]
        q_str  = q_list[q_num-1].strip().split("$")[8]
        q_ans2 = q_list[q_num-1].strip().split("$")[7]
        char_name = q_list[q_num-1].strip().split("$")[2]
        q_ans1 = ""
        print(f"q_text is {q_text}")
        print(f"q_ans2 is : {q_ans2}")
        btn2_func = partial(self.qn_call,q_str,0,None)
        # self.qn_page(char_name,q_text,q_ans1,q_ans2,None,btn2_func,True)
        return char_name, q_text, q_ans1, q_ans2, None, btn2_func, True

    def data_reset(self) :
        #resetting values of the variables
        self.q_list = ["a"]
        self.done = []
        self.qn_num = 0
        self.score = 0
        self.r_cur[1][1] = 50
        self.c_cur[1][1] = 50
        self.i_cur[1][1] = 50
        self.m_cur[1][1] = 50
        # setting values in the custom progress bars
        root.bar1.value = game.r_cur[1][1]
        root.bar2.value = game.c_cur[1][1]
        root.bar3.value = game.i_cur[1][1]
        root.bar4.value = game.m_cur[1][1]

    def var_set(self,nxt_func:object,clicked:bool) :
        print("entered game.var_set")
        with open("project_data\\variables.txt") as v_file :
            #reading values of variables from file
            v_list = v_file.readlines()
            if clicked == 1 :
                self.r_cur[1][1] += int(v_list[self.qn_num-1].strip().split("$")[1])
                self.c_cur[1][1] += int(v_list[self.qn_num-1].strip().split("$")[2])
                self.i_cur[1][1] += int(v_list[self.qn_num-1].strip().split("$")[3])
                self.m_cur[1][1] += int(v_list[self.qn_num-1].strip().split("$")[4])
            elif clicked == 2 :
                self.r_cur[1][1] += int(v_list[self.qn_num-1].strip().split("$")[5])
                self.c_cur[1][1] += int(v_list[self.qn_num-1].strip().split("$")[6])
                self.i_cur[1][1] += int(v_list[self.qn_num-1].strip().split("$")[7])
                self.m_cur[1][1] += int(v_list[self.qn_num-1].strip().split("$")[8])
            else :
                print("HAS NOT BEEN SET!!!")

        print(self.r_cur[1][1])
        print(self.c_cur[1][1])
        print(self.i_cur[1][1])
        print(self.m_cur[1][1])
        #running each variable through game_over to see if you are dead
        death_reached = False
        research_check = self.var_check(self.r_cur)
        common_check = self.var_check(self.c_cur)
        industrial_check = self.var_check(self.i_cur)
        military_check = self.var_check(self.m_cur)
        for i in [research_check,common_check,industrial_check,military_check] :
            if i is not None :
                death_reached = True
                death_params = i
                break
        else :
            nxt_func()
        if death_reached == True :
            root.qn_page(death_params[0],death_params[1],death_params[2],death_params[3],death_params[4],death_params[5],death_params[0])

    def sequence(self,sequence:str,iteration=0) :
        print("in game.sequence")
        if root.canvas_exists :
            print("canvas gone!!")
            root.bg_canvas.destroy()
            root.canvas_exists = False
        iteration += 1
        seq_open = []
        seq_close = []
        with open("project_data\\Sequences.txt") as s_file :
            s_list = s_file.readlines()
        for line in s_list :
            seq = line.strip().split("$")[1]
            if seq == "Opening" :
                seq_open += [line.strip().split("$")]
            else :
                seq_close += [line.strip().split("$")]
        if sequence == "Opening" :
            seq_list = seq_open
            if iteration == 1 :
                self.seq_num = 0
        else :
            seq_list = seq_close
            if iteration == 1 :
                self.seq_num = 0
        s_text = seq_list[self.seq_num][3]
        s_str2 = seq_list[self.seq_num ][7]
        s_str1 = ""
        s_num = seq_list[self.seq_num][9]
        char_name = seq_list[self.seq_num][2]
        self.seq_num += 1
        if s_num != "" :
            btn2_func = partial(self.sequence,sequence=sequence,iteration=iteration)
            root.qn_page(char_name,s_text,s_str1,s_str2,None,btn2_func,False)
        else :
            if sequence == "Opening" :
                self.const_qn()
            else :
                death_text = self.game_over_str(x_str="death_end")
                root.game_over_pg(death_text,"death_end")

    def const_qn(self,iteration=0) :
        iteration += 1
        self.score = 0
        if root.canvas_exists :
            print("canvas gone!!")
            root.bg_canvas.destroy()
            root.canvas_exists = False
        print("entered game.const_qn")
        if self.dead != 0 and iteration == 1 :
            m_player.music_control("project_media\\signal.ogg",False,-1,0)
        with open("project_data\\const_file.txt") as c_file :
            c_list = c_file.readlines()
        c_text = c_list[self.const_num].strip().split("$")[3]
        c_str2 = c_list[self.const_num].strip().split("$")[7]
        c_str1 = ""
        c_num = c_list[self.const_num].strip().split("$")[9]
        char_name = c_list[self.const_num].strip().split("$")[2]
        self.const_num += 1
        print(f"const_num : {self.const_num}")
        if self.direct_qns == self.direct_max and self.const_num == 1 :
            c_str1 = c_str2
            c_str2 = "Screw that."
            btn1_func = partial(self.const_qn,iteration)
            btn2_func = partial(self.sequence,sequence="Closing")
            root.qn_page(None,c_text,c_str1,c_str2,btn1_func,btn2_func,False)
        elif c_num != "" :
            btn2_func = partial(self.const_qn,iteration)
            root.qn_page(char_name,c_text,c_str1,c_str2,None,btn2_func,False)
        else :
            btn2_func = partial(self.qn_call,"a",0,"project_data\\questions_file.txt")
            root.qn_page(char_name,c_text,c_str1,c_str2,None,btn2_func,False)

    def qn_call(self,a_str:str,iteration:int,file:str) :
        print("entered game.qn_call")
        iteration += 1
        dead = False
        if iteration == 1 :
            self.seq_num = 0
            self.const_num = 0
        try :
            a_str = int(a_str)
        except ValueError :
            if iteration == 1 :
                a_str += " " * 6
            print(a_str+"end")
            print("*"*30)
            if a_str[5] == "_" :
                dead = True
        if self.saved == True and iteration == 1 :
            self.saved = False
        if not isinstance(a_str,int) :
            if iteration == 1 and a_str.strip() != "a" and not isinstance(a_str.strip(),int) and a_str.strip() != "" :
                if a_str[5] != "_" :
                    self.q_list += [a_str.strip()]
                    print(f"q_list is {self.q_list}")
                    print("@"*30)
        if isinstance(a_str,int) and file=="project_data\\Direct.txt" and not dead :
            self.qn_num = a_str
            self.qn_func(file)
        elif isinstance(a_str,int) and file=="project_data\\questions_file.txt" and not dead :
            self.qn_num = a_str
            self.qn_func(file)
        elif not isinstance(a_str,int) and not dead :
            random = randint(1,15)
            if random == 1 and self.direct_qns != self.direct_max and ("direct" not in self.q_list) :
                self.score += 1
                print("from direct!!")
                print(f"the direct qn num for next : {self.direct_qns}")
                self.q_list += ["direct"]
                self.qn_num = self.direct_qns
                self.direct_prev = self.direct_qns
                self.qn_func(file="project_data\\Direct.txt")
            else :
                print("from main!!")
                #generating the random number
                self.qn_num = randint(1,self.qn_file)
                print(f"qn_num is {self.qn_num}in main")
                with open("project_data\\questions_file.txt") as q_file :
                    qn_list = q_file.readlines()
                q_str = qn_list[self.qn_num-1].strip().split("$")[1]
                #returning the qn_num if q_str is in the list
                if q_str in self.q_list and (self.qn_num not in self.q_done) and len(self.q_done) != self.qn_file :
                    self.score += 1
                    self.q_done += [self.qn_num]
                    self.qn_func(file="project_data\\questions_file.txt")
                elif len(self.q_done) == self.qn_file :
                    self.q_done = []
                    a_str = a_str.strip()
                    self.qn_call(a_str,iteration=iteration,file=file)
                elif iteration == 700 :
                    self.q_done = []
                    self.qn_call(a_str,iteration=iteration,file=file)
                #else calling qn_call again
                else :
                    self.qn_call(a_str,iteration=iteration,file=file)
        if dead :
            self.death_str = a_str.strip()
        #    self.qn_func(file="project_data\\death.txt")
            self.qn_func("project_data\\death.txt")

    def checkstr(self, text:str, index:int) : #t is the text variable
        if len(text) > index:
            if not text[index-1].isspace():
                ind = index-1
                for i in text[index-1: :-1]:
                    if i.isspace():
                        break
                    ind -= 1
                text = text[:ind] + '\n' + self.checkstr(text[ind+1:],index)
            else:
                text = text[:index-1] + '\n' + self.checkstr(text[index:],index)
        return text

    def qn_func(self,file:str) :
        print("entered game.qn_func")
        if file != "project_data\\death.txt" :
            if file == "project_data\\Direct.txt" :
                self.direct_qns += 1
            with open(file) as q_file :
                #reading the question, options, next qn numbers and the character name from the file
                qn_list = q_file.readlines()
                qn = qn_list[self.qn_num-1].strip().split("$")[3]
                char_name = qn_list[self.qn_num-1].strip().split("$")[2]
                ans1 = qn_list[self.qn_num-1].strip().split("$")[4]
                ans2 = qn_list[self.qn_num-1].strip().split("$")[7]
                a_str1 = qn_list[self.qn_num-1].strip().split("$")[5]
                a_str2 = qn_list[self.qn_num-1].strip().split("$")[8]
                if a_str1 == "" :
                    a_str1 = qn_list[self.qn_num-1].strip().split("$")[6]
                if a_str2 == "" :
                    a_str2 = qn_list[self.qn_num-1].strip().split("$")[9]
            btn1_func = partial(self.var_set,partial(self.qn_call,a_str1,0,file=file),clicked=1)
            btn2_func = partial(self.var_set,partial(self.qn_call,a_str2,0,file=file),clicked=2)
            root.qn_page(char_name,qn,ans1,ans2,btn1_func,btn2_func,True)
        else :
            death_text = self.game_over_str(self.death_str)
            root.game_over_pg(death_text,self.death_str)


# Initialising
root = Root()
game = Game()
vid_player = VideoPlayer(root)
g_data = GameData(root)
style = Styles()
# calling the splash screen
splash = SplashScreen(root,game.main)