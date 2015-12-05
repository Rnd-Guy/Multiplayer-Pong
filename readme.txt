Multiplayer Pong! v0.2.0

Modules used: Pygame (GUI)
	      PyInstaller (Compile into .exe)

Font used: Prototype.ttf (Free font)	    

Issues:
Cannot debug on just one computer (probably due to sockets)
Exe cannot run on certain computers (unknown why)
Multiplayer over internet may not work properly 
If client picks his own ip to connect to, the client immediately crashes (socket tries to connect to itself and fails)


This is my attempt of using sockets to create a multiplayer game that connects over the internet. Game is server-hosted, so the server plays the game and the client gets the information from the server.


Files in this folder:
main.exe 	Run this to play the game. Compiled using PyInstaller.
main.py		Source code
Prototype.ttf	Font file. Keep this in the same directory as main.exe or it will not run
Prototype.txt	Text file included with the font
readme.txt	What you are currently reading
git stuff	git stuff

Changelog:
0.2.0:	Bug fix: Client calls wrong socket and crashes.
0.1.1:	Added version numbers
0.1.0:	First upload (so I can download it on a different computer to test the multiplayer)