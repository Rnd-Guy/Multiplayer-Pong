Multiplayer Pong!

Modules used: Pygame (GUI)
	      PyInstaller (Compile into .exe)

Font used: Prototype.ttf (Free font)	    




This is my attempt of using sockets to create a multiplayer game that connects over the internet. Game is server-hosted, so the server plays the game and the client gets the information from the server.


Files in this folder:
main.exe 	Run this to play the game
main.py		Source code
Prototype.ttf	Font file. Keep this in the same directory as main.exe or it will not run
Prototype.txt	Text file included with the font
readme.txt	What you are currently reading
git stuff	git stuff




Note to myself:
compile command: pyinstaller -F --noupx main.py
--noupx is needed otherwise the .exe hangs without any response