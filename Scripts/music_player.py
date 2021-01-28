from pygame import mixer
import time
from threading import Thread
import random

# The Music Player
class MusicPlayer :
    def __init__(self) :
        """Initializing pygame's mixer and starting the main background music."""
        mixer.init()
        self.playing = ""
        self.loop = 0
        self.playlist = ["project_media\\signal.ogg","project_media\\vlog.ogg","project_media\\overdrive.ogg"]
        # starting music
        mixer.music.set_volume(0.2)
        self.music_thread = Thread(target=self.music_control,args=("",),daemon=True)
        self.music_thread.start()

    def music_control(self, playing:str) :
        pos = mixer.music.get_pos()
        if (int(pos) == -1 and self.playing == playing) or self.playing == "" :
            song_index = random.randint(0,2)
            self.playing = self.playlist[song_index]
            playing = self.playing
            mixer.music.load(self.playing)
            try :
                mixer.music.play(0)
            except Exception :
                pass
        elif self.playing != playing :
            mixer.music.load(self.playing)
            playing = self.playing
            mixer.music.play(self.loop)
            self.loop = 0
        time.sleep(0.5)
        self.music_control(playing)

    @staticmethod
    def bg_sounds(s_file:str) :
        sound = mixer.Sound(s_file)
        sound.set_volume(0.2)
        mixer.Channel(1).play(sound,loops=0)

m_player = MusicPlayer()