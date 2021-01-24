from pygame import mixer

# The Music Player
class MusicPlayer :
    def __init__(self) :
        """Initializing pygame's mixer and starting the main background music."""
        mixer.init()
        # starting music
        self.music_control("project_media\\signal.ogg",False,-1,0)

    def music_control(self,track_loc:str,stop:bool,loop:int,channel:int) :
        if stop == True :
            mixer.Channel(channel).stop()
        elif stop == None :
            pass
        else:
            sound = mixer.Sound(track_loc)
            sound.set_volume(0.1)
            mixer.Channel(channel).play(sound,loops=loop)

m_player = MusicPlayer()