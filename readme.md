###Multiplayer Pong! v0.3.0

Modules used:  
Pygame (GUI)  
	      PyInstaller (Compile into .exe)

Font used: Prototype.ttf (Free font)	    




This is my attempt of using sockets to create a multiplayer game that connects over the internet. Game is server-hosted, so the server plays the game and the client gets the information from the server.

#####Controls:

Singleplayer: Arrow keys to control the paddle.   
Local multiplayer: Arrow keys to control left paddle, WASD keys to control right paddle.   
Online multiplayer: Arrow keys to control the paddle. The host uses the left paddle, while the client uses the right paddle.  

#####Issues:
Exe cannot run on certain computers (unknown why)
If client picks his own ip to connect to, the client immediately crashes (socket tries to connect to itself and fails)

#####Changelog:
0.3.0:	(Finally got it able to debug on one computer)  
	Feature: Multiplayer over internet might actually work now  
	Bug fix: Server calls wrong socket and crashes.  
	Bug fix: Fixed desyncing between server and client (by sending more info from server to client)  
	Bug fix: Eliminated client having a ghost paddle at its default position, automatically returning balls as if there was a paddle there.  
	Bug fix: Client paddle not resetting after someone has scored.  
	Bug fix: Client scores not updating.  
	Issues:  Still need to work out why exe does not run on other computers.  

0.2.0:	Bug fix: Client calls wrong socket and crashes.  

0.1.1:	Added version numbers  

0.1.0:	First upload (so I can download it on a different computer to test the multiplayer)  

#####Preview  
![Main menu](/Images/Main Menu.PNG)
![Preview](/Images/Gameplay.PNG)
