  
'''The entry point.'''

import Scripts.main_game as main


if __name__ == "__main__" :
    # display the splash screen and start game
    main.splash.display()
    # tkinter mainloop
    main.root.mainloop()