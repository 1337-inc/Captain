# CAPTAIN!!

![Header](project_pics/captain_logo.png)

The project_files folder contains all the files necessary for running the game.
The server folder contains files necessary for hosting a server on your local network.
The game can be played with or without the server but your data cant be saved or loaded if played without the server.

## About
- ‘Captain!!’ is a sci-fi choice-based game inspired by similar games such as
  reigns. The player plays as the titular Captain of a space colony and is
  required to make various decisions while keeping in mind the consequences
  of his actions. The captain must maintain the balance between scientists,
  the military, everyday citizens, and his finances without dying in the
  process.
- The server program facilitates saving/loading of data and allows the user to
  play from any compatible device connected to the server. The Server is
  capable of supporting several players at the same time.
- The main program basically semi-randomly selects a question and displays
  it. The player can choose a response, based on which variables representing
  different factions get affected. The player loses if any variable hits 0 
  or 100 or dies randomly in between upon which a “game over” screen is displayed 
  and the player can try again for a higher score.

## Installation
- You can download the installer for the game [here](https://github.com/1337-inc/Captain/releases). To install, double-click the installation package and follow the instructions presented.
- Check the create shortcut box to create a shortcut to the game on your desktop.


## Requirements
### Server
- The server application is a support application the game requires for complete functionality. Even without the server you can play the game but you wont be able to save or load your game state. 
-  The server application connects to your router's IP, starts a server on an open port, and listens for connections from clients. Once the server program has been started, you'll be able to save and load your game states.
- You can download the installer for the server application [here](https://github.com/1337-inc/Server/releases)

NOTE: The game is meant only for Windows and has only been tested on Windows 10
