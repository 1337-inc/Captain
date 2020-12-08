from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from ttkthemes import ThemedTk
from random import *
from PIL import ImageTk,Image
from threading import Thread, activeCount
import pickle
import time
from Scripts.client import Client
from Scripts.music_player import m_player
from Scripts.splash_pg import SplashScreen
from Scripts.mybar import MyBar
from Scripts.vid_player import VideoPlayer
from Scripts.styles import Styles
from functools import partial


# To Handle Game Data between Server and Client
class GameData(Client) :
    def __init__(self,parent) :
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
    
    def load_data(self,name,code) :
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

    def check_data(self,name,code) :
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


# The Tkinter Interface
class Root(ThemedTk) :
    def __init__(self,**kwargs) :
        ThemedTk.__init__(self,theme="black",**kwargs)
        # defining the menubar
        self.menu()
        # setup stuff goes here
        self.configure(bg = "#424242")
        self.columnconfigure(0,weight=1)
        self.title("Captain!!")
        self.iconbitmap("project_pics\\cap_icon.ico")
        # side bar
        self.side_bar = Frame(self,height=700,width=120,style="var.TFrame")
        # defining the objects for the progress bars
        self.bar1 = MyBar(self.side_bar, shape="project_pics\\research.png", value=50, bg="#424242", trough_color='white', bar_color='gray54')
        self.bar2 = MyBar(self.side_bar, shape="project_pics\\man.png", value=50, bg="#424242", trough_color='lavender', bar_color='gray54')
        self.bar3 = MyBar(self.side_bar, shape="project_pics\\dollar.png", value=50, bg="#424242", trough_color='lavender', bar_color='gray54')
        self.bar4 = MyBar(self.side_bar, shape="project_pics\\sword.png", value=50, bg="#424242", trough_color='lavender', bar_color='gray54')
        # the exit protocol
        self.protocol("WM_DELETE_WINDOW",lambda: self.exit(leave=False))
        self.enter = True

    def clear(self) :
        for widget in self.winfo_children() :
            if widget is not self.side_bar and widget is not self.menubar :
                widget.destroy()
            else :
                widget.grid_forget()

    def mssg_box(self) :
        def heaven() :
            # text to be displayed in the window
            img_btn.destroy()
            frame = Frame(mssgwin,width=width,height=height)
            frame.pack()
            Label(frame,text="   [System Message...]",style="start_text.TLabel").grid(row=0,column=0,sticky="new")
            Label(frame,text=f"[Important Message] Player {game.NAME} has \nmanaged to successfully eliminate all \nhuman lifeforms including himself.\n\t     GAME OVER",style="main_pg.TLabel").grid(row=1,column=0,pady=15)
            Button(mssgwin,text="dammit",command=mssgwin.destroy,style="mssg.TButton").place(relx=0.27,rely=0.78)
        # Toplevel window
        mssgwin = Toplevel(self)
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
        img_btn = Button(mssgwin,image=img)
        img_btn.config(command=partial(heaven))
        img_btn.image = img
        img_btn.pack(anchor="nw")

    def menu(self) :
        def credits() :
            def populate(frame):
                '''Put in labels'''
                Grid.columnconfigure(frame, 0, weight=1)
                # defining the lables
                cap_title = Label(frame,text="Captain!!",style="death.TLabel")
                developed = Label(frame,text="Developed by 1337 incorporated",style="creditshead1.TLabel")
                team = Label(frame,text="OUR TEAM",style="creditshead2.TLabel")
                abhi = Label(frame,text="• Abhinand D Manoj        ",style="creditstext.TLabel")
                david = Label(frame,text="• David Tony Veliath       ",style="creditstext.TLabel")
                me = Label(frame,text="• Jovan George Zacharia",style="creditstext.TLabel")
                rahul = Label(frame,text="• Rahul Dinesh                 ",style="creditstext.TLabel")
                special = Label(frame,text="SPECIAL THANKS",style="creditshead2.TLabel")
                rinu = Label(frame,text="Mrs Rinu Mary Joy, our Teacher",style="creditstext.TLabel")
                parents = Label(frame,text="Our Parents and Friends",style="creditstext.TLabel")
                internet = Label(frame,text="The Internet",style="creditstext.TLabel")
                websites = Label(frame,text="WEBSITES",style="creditshead2.TLabel")
                stack = Label(frame,text="1. stackoverflow.com",style="creditstext.TLabel")
                programiz = Label(frame,text="2. programiz.com      ",style="creditstext.TLabel")
                reddit = Label(frame,text="3. reddit.com               ",style="creditstext.TLabel")
                w3school = Label(frame,text="4. w3school.com         ",style="creditstext.TLabel")
                geeks = Label(frame,text="5. geeksforgeeks.com",style="creditstext.TLabel")
                youtube = Label(frame,text="6. youtube.com            ",style="creditstext.TLabel")
                logo = Label(frame,text="7.Logomakr.com           ",style="creditstext.TLabel")
                music = Label(frame,text="MUSIC AND SOUND EFFECTS",style="creditshead2.TLabel")
                signal = Label(frame,text="Signal by drkmnd",style="creditstext.TLabel")
                motion1 = Label(frame,text="Sad Violin by MOTION ARRAY ",style="creditstext.TLabel")
                motion2 = Label(frame,text="Glitch sound effects by MOTION ARRAY ",style="creditstext.TLabel")
                star = Label(frame,text="Star Wars Theme Song By John Williams",style="creditstext.TLabel")
                video = Label(frame,text="VIDEO",style="creditshead2.TLabel")
                glitch = Label(frame,text="Game Over Glitch by MOTION ARRAY",style="creditstext.TLabel")
                crawl = Label(frame,text="Star Wars Intro Creator by Kassel Labs",style="creditstext.TLabel")
                label = Label(frame,text="   \n")
                grp_name = Label(frame,text="1337 INCORPORATED",style="creditstext2.TLabel")
                rights = Label(frame,text="ALL RIGHTS RESERVED",style="creditstext2.TLabel")
                cap = Label(frame,text="Captain!! IS A TRADEMARK OF 1337 ",style="creditstext2.TLabel")
                license_ = Label(frame,text="INCORPORATED IN INDIA, USED UNDER",style="creditstext2.TLabel")
                grp = Label(frame,text="LICENSE BY 1337 INCORPORATED ENTERTAINMENT",style="creditstext2.TLabel")
                # placingthe lables
                cap_title.grid(row=0,column=0,padx=40,pady=15)
                developed.grid(row=1,column=0,pady=10,padx=10)
                team.grid(row=2,column=0,pady=20,sticky=S)
                abhi.grid(row=3,column=0)
                david.grid(row=4,column=0,pady=5)
                me.grid(row=5,column=0,pady=5)
                rahul.grid(row=6,column=0,pady=5)
                special.grid(row=7,column=0,pady=20,sticky=S)
                rinu.grid(row=8,column=0)
                parents.grid(row=9,column=0,pady=5)
                internet.grid(row=10,column=0,pady=5)
                websites.grid(row=11,column=0,pady=20,sticky=S)
                stack.grid(row=12,column=0)
                programiz.grid(row=13,column=0,pady=5)
                reddit.grid(row=14,column=0,pady=5)
                w3school.grid(row=15,column=0,pady=5)
                geeks.grid(row=16,column=0,pady=5)
                youtube.grid(row=17,column=0,pady=5)
                logo.grid(row=18,column=0,pady=5)
                music.grid(row=19,column=0,pady=20,sticky=S)
                signal.grid(row=20,column=0)
                motion1.grid(row=21,column=0,pady=5)
                motion2.grid(row=22,column=0,pady=5)
                star.grid(row=23,column=0,pady=5)
                video.grid(row=24,column=0,pady=20,sticky=S)
                glitch.grid(row=25,column=0)
                crawl.grid(row=26,column=0,pady=5)
                label.grid(row=27,column=0,pady=10)
                grp_name.grid(row=28,column=0,pady=5)
                rights.grid(row=29,column=0,pady=5)
                cap.grid(row=30,column=0,pady=5)
                license_.grid(row=31,column=0,pady=5)
                grp.grid(row=32,column=0,pady=5)

            def onFrameConfigure(canvas):
                '''Reset the scroll region to encompass the inner frame'''
                canvas.configure(scrollregion=canvas.bbox("all"))
            
            def on_mousewheel(event):
                shift = (event.state & 0x1) != 0
                scroll = -1 if event.delta > 0 else 1
                if shift:
                    canvas.xview_scroll(scroll, "units")
                else:
                    canvas.yview_scroll(scroll, "units")

            window = Toplevel(self)
            window["bg"] = "#424242"
            window.title("Credits")
            window.resizable(0,0)
            canvas = Canvas(window, background="#424242", width=500, height=550)
            canvas.bind_all("<MouseWheel>", on_mousewheel)
            frame = Frame(canvas)
            vsb = Scrollbar(window, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=vsb.set)

            vsb.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((4,4), window=frame, anchor="nw")

            frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

            populate(frame)

        def profile() :
            profile = Toplevel(self)
            profile.title("Player Profile")
            profile.resizable(0,0)
            profile.geometry("500x500")
            profile["bg"] = "#424242"
            # Text box
            text_box = Image.open("project_pics\\text_box1.png")
            width,height = text_box.size
            text_box = ImageTk.PhotoImage(text_box)
            frame = Frame(profile,width=width,height=height,style="pframe.TFrame")
            frame.place(relx=0.5,rely=0.55,anchor=CENTER)
            frame.grid_propagate(False)
            txt_box = Label(frame,image=text_box)
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
            player_lbl = Label(frame,image=player,style="pimage.TLabel")
            score_lbl = Label(frame,image=score,style="pimage.TLabel")
            highscore_lbl = Label(frame,image=highscore,style="pimage.TLabel")
            # Saving a reference of the images
            player_lbl.image = player
            score_lbl.image = score
            highscore_lbl.image = highscore
            # Displaying the images
            player_lbl.place(relx=0.1,rely=0.15)
            score_lbl.place(relx=0.1,rely=0.45)
            highscore_lbl.place(relx=0.1,rely=0.75)
            # Texts
            Label(profile,text="[Player Profile Generating...]",style="ptext1.TLabel").place(relx=0.5,rely=0.1,anchor=CENTER)
            Label(frame,text=f"Player : {game.NAME}",style="ptext2.TLabel").place(relx=0.35,rely=0.19)
            Label(frame,text=f"Current Score : {game.score}",style="ptext2.TLabel").place(relx=0.35,rely=0.48)
            Label(frame,text=f"High Score : {game.high_score}",style="ptext2.TLabel").place(relx=0.35,rely=0.79)
        
        def coming_soon(win_title) :
            win = Toplevel(self)
            win.title(win_title)
            win.geometry("400x500")
            Label(win,text="Coming Soon").place(relx=0.5,rely=0.5,anchor=CENTER)

        self.menubar = Menu(self)
        # The Game Menu 
        gamebar = Menu(self.menubar,tearoff=0,bg="gray15",fg="white",activebackground="#424242")
        gamebar.add_command(label="Player Profile",command=profile)
        gamebar.add_command(label="Save data",command=partial(self.s_msg,"e_save"))
        gamebar.add_separator()
        gamebar.add_command(label="Quit",command=partial(self.exit,False))
        self.menubar.add_cascade(label="Game",menu=gamebar)
        # The About Menu
        aboutmenu = Menu(self.menubar,tearoff=0,bg="gray15",fg="white",activebackground="#424242")
        aboutmenu.add_command(label="Credits",command=credits)
        aboutmenu.add_command(label="About",command=partial(coming_soon,"About"))
        self.menubar.add_cascade(label="Help",menu=aboutmenu)

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
        if game.saved == True or leave or game.q_done == [] :
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
        bg_image = Image.open("project_pics\\start_pg.png")
        bg_image = ImageTk.PhotoImage(bg_image)
        image_bg = Label(self,image=bg_image) # ,style="img.TLabel"
        image_bg.image = bg_image
        image_bg.grid(sticky="nwse")
        # frame and text
        frame = Frame(self,width=500,height=400,style="start.TFrame")
        frame.grid_propagate(0)
        frame.place(relx=0.325,rely=0.2)
        Label(frame,text="[System Initiating...]",style="start_text.TLabel").grid(row=0,column=0,pady=30,padx=30,sticky="w",columnspan=2)
        Label(frame,text="[Creating Player Environment...]",style="start_text.TLabel").grid(row=1,column=0,padx=30,sticky="w",columnspan=2)
        Label(frame,text="Enter player name: ",style="main_pg.TLabel").grid(row=2,column=0,pady=40,padx=30,sticky="w")
        name = Entry(frame,width=16,font=("bahnschrift semilight condensed",20)) # ,style="entry.TEntry"
        name.grid(row=2,column=1,sticky="w")
        name.focus_force()
        Label(frame,text="Create player pass-code: ",style="main_pg.TLabel").grid(row=3,column=0,padx=30,sticky="w")
        code = Entry(frame,width=16,font=("bahnschrift semilight condensed",20))
        code.grid(row=3,column=1,sticky="w")

        Button(self,text="Back",style="start_pg.TButton",command=partial(self.btn_click,self.main_page)).place(relx=0.324,rely=0.76,height=100)
        Button(self,text="Load",style="start_pg.TButton",command=partial(self.btn_click,partial(game.load,name,code))).place(relx=0.509,rely=0.76,height=100)

    def s_msg(self,type:str) :
        if type == "fail" :
            messagebox.showerror("ERROR","Sorry, your game data could not be saved. Please report a bug if you see this")
        elif type =="ask_save" :
            msg = messagebox.askquestion("Save?","You already have a saved state. Are you sure you want to overwrite this? You previous progress will be lost.")
            return(msg)
        elif type == "save" :
            messagebox.showinfo("Saved","Your progress has been saved")
        elif type == "exit" :
            msg = messagebox.askquestion("Warning!","Are you want to leave without saving your progress?")
            if msg == "yes" :
                self.exit(True)
            else :
                msg = messagebox.askquestion("Save?","Save Progress?")
                if msg == "yes" :
                    g_data.savedata()
                    self.exit(True)
        elif type == "l_fail" :
            msg = messagebox.showerror("ERROR","You do not have a saved state")
        elif type == "e_save" :
            msg = messagebox.askquestion("Save?","Do you want to save your progress?")
            if msg == "yes"  :
                if game.NAME :
                    g_data.savedata()
                else :
                    self.s_msg("n_state")
        elif type == "l_tru" :
            msg = messagebox.showinfo("Loaded","Your game state has been loaded. You will be redirected to your reset point")
            if msg == "ok" :
                game.const_qn()
        elif type == "sconn_fail" :
            msg = messagebox.showerror("ERROR","Sorry, we could not save your data because you are not connected to the server. Please report a bug if you see this")
        elif type == "lconn_fail" :
            msg = messagebox.showerror("ERROR","Sorry, we could not load your data because you are not connected to the server. Please report a bug if you see this")
        elif type == "conn_fail" :
            if self.enter :
                msg = messagebox.showerror("ERROR","Sorry, an error occured while attempting to connect you to the server. Please report a bug if you see this")
        elif type == "game_over" :
            msg = messagebox.showinfo("Loaded","Congrats! You seem to have already reached your destiny. To try again, please create a new avatar and start a new game")
        elif type == "n_state" :
            msg = messagebox.showerror("Sorry","Sorry, you do not have a game state yet. Start a new game or load your game state and try again")
        elif type == "data_exists" :
            msg = messagebox.showerror("Error","You already have a game state with the same name and code. Please load your game data in the load page or enter a new name and code if you wish to start a new game")
        elif type == "c-conn_fail" :
            msg = messagebox.showwarning("Warning","You are playing offline right now. So your data will be temporary and would not be accessable later")

    def proceed(self,parent:object,name:object,code:object) :    # partial(root.btn_click,partial(game.sequence,sequence="Opening"))
        if name.get() != "" and code.get() != "" : #lambda: vid_player.player("project_media\\starwarscrawl.mp4","project_media\\starwarstrack.ogg",lambda : game.sequence(sequence="Opening"))
            proceed_btn = partial(root.btn_click,lambda: vid_player.player("project_media\\starwarscrawl.mp4","project_media\\starwarstrack.ogg",lambda : game.sequence(sequence="Opening")))
            exists = g_data.check_data(name.get(),code.get())
            if exists != "Exists" and exists is not None :
                Button(self,text="Proceed",style="start_pg.TButton",command=partial(self.btn_click,proceed_btn)).place(relx=0.509,rely=0.76,height=100)
                game.NAME = name.get()
                game.CODE = code.get()
            elif exists is None :
                Button(self,text="Proceed",style="start_pg.TButton",command=partial(self.btn_click,proceed_btn)).place(relx=0.509,rely=0.76,height=100)
                game.NAME = name.get()
                game.CODE = code.get()
                root.s_msg("c-conn_fail")
            else :
                root.s_msg("data_exists")
        else :
            Label(parent,text="[Error]... Player must have a name and code",style="main_pg.TLabel").grid(row=4,columnspan=2)

    def start_page(self) :
        self.clear()
        self.enter = False
        # background image
        bg_image = Image.open("project_pics\\start_pg.png")
        bg_image = ImageTk.PhotoImage(bg_image)
        image_bg = Label(self,image=bg_image,style="img.TLabel")
        image_bg.image = bg_image
        image_bg.grid(sticky="nwse")
        # frame and text
        frame = Frame(self,width=500,height=400,style="header.TFrame")
        frame.grid_propagate(0)
        frame.place(relx=0.325,rely=0.2)
        Label(frame,text="[System Initiating...]",style="start_text.TLabel").grid(row=0,column=0,pady=30,padx=30,sticky="w",columnspan=2)
        Label(frame,text="[Creating Player Environment...]",style="start_text.TLabel").grid(row=1,column=0,padx=30,sticky="w",columnspan=2)
        Label(frame,text="Enter player name: ",style="main_pg.TLabel").grid(row=2,column=0,pady=40,padx=30,sticky="w")
        Label(frame,text="\t\t\t",style="start_error.TLabel").grid(row=4,columnspan=2)
        name = Entry(frame,width=16,font=("bahnschrift semilight condensed",20)) # ,style="entry.TEntry"
        name.grid(row=2,column=1,sticky="w")
        name.focus_force()
        Label(frame,text="Create player pass-code: ",style="main_pg.TLabel").grid(row=3,column=0,padx=30,sticky="w")
        code = Entry(frame,width=16,font=("bahnschrift semilight condensed",20))
        code.grid(row=3,column=1,sticky="w")
        # Buttons
        Button(frame,text="Verify",style="startpg_verify.TButton",command=partial(self.btn_click,partial(self.proceed,frame,name,code))).grid(row=5,column=0,columnspan=2,pady=15,padx=10,ipady=10)
        Button(self,text="Back",style="start_pg.TButton",command=partial(self.btn_click,self.main_page)).place(relx=0.324,rely=0.76,height=100)

    def main_page(self) :
        self.clear()
        img = Image.open('project_pics\\main_pg.png')
        img_new = ImageTk.PhotoImage(img)
        label = Label(self,image=img_new,style="img.TLabel")
        label.image = img_new
        label.grid(sticky="nwse")
        start_btn = Button(self,text="Start New Game",style="main.TButton",command=partial(self.btn_click,game.start))
        start_btn.place(relx=0.9,rely=0.35,anchor=CENTER,width=386,height=100)
        load_btn = Button(self,text="Load Game",style="main.TButton",command=partial(self.btn_click,self.load_page))
        load_btn.place(relx=0.9,rely=0.5,anchor=CENTER,width=386,height=100)
        quit_btn = Button(self,text="Quit",style="main.TButton",command=partial(self.btn_click,partial(self.exit,False)))
        quit_btn.place(relx=0.9,rely=0.65,anchor=CENTER,width=386,height=100)
        if g_data.connected == False :
            self.s_msg("conn_fail")

    def game_over_pg(self,d_text:str,d_str:str) :
        print("entered root.game_over_pg")
        self.clear()
        # adding \n wherever required
        d_text = game.checkstr(d_text,30)
        # stopping current music and plying new one
        m_player.music_control("project_media\\signal.ogg",True,-1,0)
        m_player.music_control("project_media\\game_over.ogg",False,-1,0)
        # header frame
        header_frame = Frame(self,height=30,width=1280,style="header.TFrame")
        header_frame.grid(row=0,columnspan=2,sticky=E+N+W)
        Label(header_frame,text="Player: Capt. "+game.NAME,style="head_label.TLabel").place(relx=0.12) # 0.15
        Label(header_frame,text="Player Status: "+str(game.score)+" Days in power",style="head_label.TLabel").place(relx=0.55)
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
        logo_image = Label(self,image=logo_new,style="img.TLabel")
        logo_image.image = logo_new
        logo_image.place(relx=0.01,rely=0.07)
        # text box
        Label(self,text="YOU DIED..",style="death.TLabel").place(relx=0.33,rely=0.1)
        img = Image.open("project_pics\\text_box1.png")
        img_new = ImageTk.PhotoImage(img)
        text_frame = Frame(self,style="text.TFrame")
        img_label = Label(text_frame,image=img_new,style="img.TLabel")
        img_label.image = img_new
        img_label.pack(fill=BOTH)
        Label(text_frame,text=d_text,style="text.TLabel").place(relx=0.5,rely=0.55,anchor=CENTER)
        text_frame.place(relx=0.35,rely=0.25)
        if d_str != "death_end" :
            nxt_func = game.const_qn
            btn_func = partial(vid_player.player,"project_media\\glitch.mp4","project_media\\glitch.ogg",nxt_func)
        else :
            game.game_over = True
            btn_func = "Starting_game_again"
        thread = Thread(target=game.data_reset)
        thread.start()
        thread.join() # partial(vid_player.player,"project_media\\glitch.mp4","project_media\\glitch.ogg",func)
        Button(self,text="Continue",style="death_pg.TButton",command=partial(self.btn_click,btn_func)).place(relx=0.6,rely=0.8,width=250,height=80)
        if d_str != "death_end" :
            root.s_msg("e_save")
        else :
            self.mssg_box()

    def qn_page(self,char_name:str,qn:str,ans1:str,ans2:str,btn1_func:object,btn2_func:object,bar_dis:bool) :
        print("entered root.qn_page")
        self.clear()
        Grid.columnconfigure(self,0,weight=1)
        # Adding \n to the text to display so as to fit them in the widgets
        ans1 = game.checkstr(text=ans1,index=30)
        ans2 = game.checkstr(text=ans2,index=30)
        qn = game.checkstr(text=qn,index=30)
        # header bar
        header_frame = Frame(self,height=30,width=1280,style="header.TFrame")
        header_frame.grid(row=0,columnspan=2,sticky=E+N+W)
        Label(header_frame,text="Player: Capt. "+game.NAME,style="head_label.TLabel").place(relx=0.12) # 0.15
        Label(header_frame,text="Player Status: "+str(game.score)+" Days in power",style="head_label.TLabel").place(relx=0.5)
        # display game logo on left of screen
        logo_img = Image.open("project_pics\\cap_logo_invert.PNG")
        logo_new = ImageTk.PhotoImage(logo_img)
        logo_image = Label(self,image=logo_new,style="img.TLabel")
        logo_image.image = logo_new
        logo_image.place(relx=0.01,rely=0.07) # .grid(row=0,column=0,sticky=W+S)
        # open image to display as container for text
        img = Image.open("project_pics\\text_box1.png")
        img_new = ImageTk.PhotoImage(img)
        # create frame to display the container pic and the text
        text_frame = Frame(self,style="text.TFrame")
        border = Label(text_frame,image=img_new,style="img.TLabel")
        border.image = img_new
        border.pack(fill=BOTH)
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
            char_image = Label(self,image=img,style="img.TLabel")
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
        label1 = Label(text_frame,text=char_name,style="text.TLabel")
        label1.place(relx=0.5,rely=0.1,anchor=CENTER)
        label2 = Label(text_frame,text=qn,style="text.TLabel")
        label2.place(relx=0.5,rely=0.55,anchor=CENTER)
        # displaying the buttons on the screen
        if ans1 != "" :
            print("button 1")
            btn1 = Button(self,text=ans1,style="text_btn.TButton",command=partial(self.btn_click,btn1_func))
            btn1.place(relx=0.17,rely=0.8,anchor=W,width=386,height=150)
        print("button 2")
        print(btn2_func)
        btn2 = Button(self,text=ans2,style="text_btn.TButton",command=partial(self.btn_click,btn2_func))
        btn2.place(relx=0.81,rely=0.8,anchor=E,width=386,height=150)


# Game logic and data handle
class Game :
    def __init__(self) :
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

    def start(self) :
        root.start_page()

    def main(self):
        root.overrideredirect(False)
        root.config(menu=root.menubar)
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
            death_params = self.game_over_dict(x_cur,type="first")
            return death_params
        elif x_cur[1][1]>=105 :
            print("entered game.var_check inside second condition")
            print(f"variable death: {x_cur}")
            death_params = self.game_over_dict(x_cur,type="second")
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

    def game_over_dict(self,x_str:dict,type:str) :
        print(f"x_str : {x_str}")
        print("entered game.game_over_dict")
        iteration = 0
        if self.high_score < self.score :
            self.high_score = self.score
        if type == "first" :
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
                print("$"*30)
                
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
        # print(f"sequence list is : {seq_list}")
        # print(f"sequence is : {sequence}")
        # print(f"seq_num : {self.seq_num}")
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
        if type(a_str) is not int :
            if iteration == 1 and a_str.strip() != "a" and type(a_str.strip()) != int and a_str.strip() != "" :
                if a_str[5] != "_" :
                    self.q_list += [a_str.strip()]
                    print(f"q_list is {self.q_list}")
                    print("@"*30)
        if type(a_str)==int and file=="project_data\\Direct.txt" and not dead :
            self.qn_num = a_str
            self.qn_func(file)
        elif type(a_str)==int and file=="project_data\\questions_file.txt" and not dead :
            self.qn_num = a_str
            self.qn_func(file)
        elif type(a_str)!= int and not dead :
            random = randint(1,10)
            if random == 1 and self.direct_qns != self.direct_max and "direct" not in self.q_list : # to block all directs: and ("a" not in self.q_list) 
                self.score += 1
                print("from direct!!")
                print("##$$%%"*30)
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


# initialising
root = Root()
game = Game()
vid_player = VideoPlayer(root)
g_data = GameData(root)
style = Styles()
# calling the splash screen
splash = SplashScreen(root,game.main)

#driver code
if __name__ == "__main__" :
    splash.display()

    root.mainloop()