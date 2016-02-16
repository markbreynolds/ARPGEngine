#menus.py

import pygame
from pygame.locals import *

def MainMenu(screen,font,inputEngine):
	selected = False
	sel = 0
	
	while not selected:
		screen.fill((0,0,0))
		if sel == 0:
			screen.blit(font.render("Single Player",True,(255,255,0),(0,0,0)),(120,130))
		else:
			screen.blit(font.render("Single Player",True,(255,255,255),(0,0,0)),(120,130))
		if sel == 1:
			screen.blit(font.render("Multiplayer",True,(255,255,0),(0,0,0)),(125,144))
		else:
			screen.blit(font.render("Multiplayer",True,(255,255,255),(0,0,0)),(125,144))
		if sel == 2:
			screen.blit(font.render("Options",True,(255,255,0),(0,0,0)),(135,158))
		else:
			screen.blit(font.render("Options",True,(255,255,255),(0,0,0)),(135,158))
		if sel ==3 :
			screen.blit(font.render("Exit",True, (255,255,0),(0,0,0)),(145,172))
		else:
			screen.blit(font.render("Exit",True, (255,255,255),(0,0,0)),(145,172))
		
		for event in inputEngine.getInput():
			if event[0] == "Quit":
				return "E"
			if event[1] == "Down":
				if event[0] == "Down":
					if sel == 3:
						sel=0
					else:
						sel+=1
				elif event[0] == "Up":
					if sel == 0:
						sel=3
					else:
						sel-=1
				elif event[0] == "Accept":
					if sel == 0:
						return "S"
					elif sel == 1:
						pass
					elif sel == 2:
						return "O"
					elif sel == 3:
						return "E"
		
		screen.update()
		pygame.display.update()
