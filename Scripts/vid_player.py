from tkinter import *
from tkinter.ttk import Button
from PIL import Image, ImageTk
import time
import cv2 as cv2
from threading import Thread
from Scripts.music_player import m_player
from Scripts.styles import Styles


# The Video Player
class VideoPlayer :
    def __init__(self,parent) :
        self.parent = parent
        self.play = False

    def player(self,vid_file,m_file,nxt_func):
        def get_frame():
            ret,frame = vid.read()
            if ret and self.play :
                return(ret,cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            else :
                return(ret,None)
        def update() :
            ret,frame = get_frame()
            if ret and self.play :
                img = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=img)
                photo.image=img
                self.canvas.itemconfig(self.vid_frame,image=photo)
                self.canvas.image=photo
                self.parent.after(delay,lambda : update())
            else :
                time.sleep(0.01)
                # stopping vid_music and starting game music
                m_player.music_control(m_file,True,-1,0)
                m_player.music_control("project_media\\signal.ogg",False,-1,0)
                nxt_func()

        def skip() :
            self.play = False

        self.parent.clear()
        self.play = True

        # starting music
        m_player.music_control("project_media\\signal.ogg",True,-1,0)
        m_player.music_control(m_file,False,-1,0)
        
        vid = cv2.VideoCapture(vid_file)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas = Canvas(self.parent, width = width, height = height)
        self.canvas.place(relx=0.5,rely=0.5,anchor=CENTER)
        self.vid_frame = self.canvas.create_image(0, 0, anchor = NW)

        # Skip button
        if vid_file != "project_media\\glitch.mp4" :
            skip_thread = Thread(target=skip)
            skip = Button(self.parent,text="Skip",command=skip_thread.start,style="skip.TButton")
            skip.place(relx=0.88,rely=0.04)

        delay = 5
        update()