#input.py

import pygame
from pygame.locals import *
from collections import deque

class InputEngine(object):
	def __init__(self):
		self.keybindings = {K_w:"Up",K_s:"Down",K_a:"Left",K_d:"Right",K_RETURN:"Accept",K_RSHIFT:"Cancel",K_SPACE:"Inven",K_ESCAPE:"Pause",K_QUOTE:"S1"}
		self.joybindings = {"Axis":{0:"X",1:"Y"},"Button":{2:"Accept",1:"Cancel",10:"Pause",3:"S1"}}
		self.move = [False,False,False,False]
		self.deadzone=.1
		self.resetX=True
		self.resetY=True
		self.dump=False
		
		self.ability=False
		self.abilityTime=0
		self.abilityDire=""
		
		if pygame.joystick.get_count()==0:
			self.joystick = False
			self.debouncer = {"Accept":False,"Cancel":False,"Inven":False,"Pause":False,"Up":None,"Down":None,"Left":None,"Right":None,"S1":None}
		else:
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()
	
	def getMove(self):
		return self.move
	
	def setDump(self,dump):
		if dump:
			self.dump = deque()
		else:
			self.dump = False
		return self.dump
	
	def getDirection(self):
		if not self.joystick:
			vector = [0,0]
			if self.move[0]:
				vector[1]-=1
			if self.move[1]:
				vector[0]+=1
			if self.move[2]:
				vector[1]+=1
			if self.move[3]:
				vector[0]-=1
			return vector
		else:
			return [self.joystick.get_axis(0),self.joystick.get_axis(1)]
	
	def update(self):
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if self.keybindings[event.key] == "Up":
					self.move[0]=True
				if self.keybindings[event.key] == "Right":
					self.move[1]=True
				if self.keybindings[event.key] == "Down":
					self.move[2]=True
				if self.keybindings[event.key] == "Left":
					self.move[3]=True
			if event.type == KEYUP:
				if self.keybindings[event.key] == "Up":
					self.move[0]=False
				if self.keybindings[event.key] == "Right":
					self.move[1]=False
				if self.keybindings[event.key] == "Down":
					self.move[2]=False
				if self.keybindings[event.key] == "Left":
					self.move[3]=False
	
	def getInput(self,tick=None):
		ret = []
		if tick != None:
			if self.abilityTime<=0:
				if self.ability:
					temp="S1"
					if self.abilityDire == "Up":
						temp = "S1U"
					elif self.abilityDire == "Right":
						temp = "S1R"
					elif self.abilityDire == "Down":
						temp = "S1D"
					elif self.abilityDire == "Left":
						temp = "S1L"
					ret.append([temp,"Down"])
					self.debouncer["S1"]=True
					self.ability=False
				self.abilityDire=""
			else:
				self.abilityTime-=tick
		try:
			for event in pygame.event.get():
				if event.type == QUIT:
					ret.append(["Quit"])
				elif event.type == KEYDOWN:
					if self.dump!=False:
						self.dump.append(["Raw_"+pygame.key.name(event.key),"Down"])
					temp = self.keybindings[event.key]
					if self.joystick==False:
						if self.debouncer[temp]==True:
							pass
						else:
							if temp == "S1":
								if self.abilityDire != "":
									if self.abilityDire == "Up":
										temp = "S1U"
									elif self.abilityDire == "Right":
										temp = "S1R"
									elif self.abilityDire == "Down":
										temp = "S1D"
									elif self.abilityDire == "Left":
										temp = "S1L"
									ret.append([temp,"Down"])
									self.debouncer["S1"]=True
								else:
									self.ability=True
									self.abilityTime=.025
							else:
								ret.append([temp,"Down"])
								self.debouncer[temp]=True
					else:
						ret.append([temp,"Down"])
					if temp == "Up":
						self.move[0]=True
						self.abilityTime = .025
						self.abilityDire = "Up"
					elif temp == "Right":
						self.move[1]=True
						self.abilityTime = .025
						self.abilityDire = "Right"
					elif temp == "Down":
						self.move[2]=True
						self.abilityTime = .025
						self.abilityDire = "Down"
					elif temp == "Left":
						self.move[3]=True
						self.abilityTime = .025
						self.abilityDire = "Left"
				elif event.type == KEYUP:
					if self.dump!=False:
						self.dump.append(["Raw_"+pygame.key.name(event.key),"Up"])
					temp = self.keybindings[event.key]
					if self.joystick==False:
						if self.debouncer[temp]==True:
							self.debouncer[temp]=False
					ret.append([temp,"Up"])
					if temp == "Up":
						self.move[0]=False
					elif temp == "Right":
						self.move[1]=False
					elif temp == "Down":
						self.move[2]=False
					elif temp == "Left":
						self.move[3]=False
				elif event.type == JOYAXISMOTION:
					if self.joybindings["Axis"][event.axis]=="X":
						if event.value>self.deadzone:
							if self.resetX:
								ret.append(["Right","Down"])
								self.resetX=False
							self.move[1]=True
							self.move[3]=False
						elif event.value<-self.deadzone:
							if self.resetX:
								ret.append(["Left","Down"])
								self.resetX=False
							self.move[1]=False
							self.move[3]=True
						else:
							self.move[1]=False
							self.move[3]=False
							self.resetX=True
					elif self.joybindings["Axis"][event.axis]=="Y":
						if event.value<-self.deadzone:
							if self.resetY:
								ret.append(["Up","Down"])
								self.resetY=False
							self.move[0]=True
							self.move[2]=False
						elif event.value>self.deadzone:
							if self.resetY:
								ret.append(["Down","Down"])
								self.resetY=False
							self.move[0]=False
							self.move[2]=True
						else:
							self.move[0]=False
							self.move[2]=False
							self.resetY=True
				elif event.type == JOYBUTTONDOWN:
					if self.joybindings["Button"][event.button]=="Accept":
						ret.append(["Accept","Down"])
					elif self.joybindings["Button"][event.button]=="Cancel":
						ret.append(["Cancel","Down"])
		except KeyError:
			pass
		return ret
