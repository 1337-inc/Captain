from pygame import mixer

# The Music Player
class MusicPlayer :
    def __init__(self) :
        mixer.init()
        # starting music
        self.music_control("project_media\\signal.ogg",False,-1,0)
    
    def music_control(self,track_loc,stop,loop,channel) :
        if stop == True :
            mixer.Channel(channel).stop()
        elif stop == None :
            pass
        else:
            sound = mixer.Sound(track_loc)
            sound.set_volume(0.1)
            mixer.Channel(channel).play(sound,loops=loop)
            # pass

m_player = MusicPlayer()