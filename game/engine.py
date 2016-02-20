import math

import pygame
import random

import config
from mask import maskFromSurface

class GameEngine(object):
	def __init__(self,loadNewAreaFunc,battleFunc,player=None,level=None,physics=True):
		if level != None:
			self.loadLevel(level)
		self.level = level
		self.loadNewAreaFunc = loadNewAreaFunc
		self.physics=physics
		self.actors = []
		self.NPCs = []
		self.player = player
		self.party = []
		self.triggers = []
		self.boundaries = None
		self.savedStates = {}
		
		self.battleFunc = battleFunc
		self.timeToBattle = 5*random.random()+5
		self.enemies = []
		self.battleBG = []
	
	def loadLevel(self,level):
		self.level = level
		if self.savedStates.keys().__contains__(self.level):
			for key in self.savedStates[self.level].keys():
				for actor in self.actors:
					if actor.ID == key:
						if type(actor)==Pushable:
							actor.setState(self.savedStates[self.level][key][0])
							actor.setPos(self.savedStates[self.level][key][1])
						else:
							actor.setState(self.savedStates[self.level][key])
	
	## Sets the list of battle backgrounds that can be picked from.
	def setBattleBG(self,battleBG):
		self.battleBG = battleBG
	
	## Sets the list of enemies that can be picked from in random enemy encounters.
	def setEnemies(self,enemies):
		self.enemies = enemies
	
	## Sets the boundaries for this level.
	#
	#  @param mask The path to the image that describes the boundaries of this level.
	def setMask(self,mask):
		if self.physics:
			if mask != None:
				try:
					self.boundaries = maskFromSurface(mask)
				except pygame.error:
					self.boundaries = None
			else:
				self.boundaries = None
		else:
			self.boundaries=None
	
	def addActor(self,actor):
		self.actors.append(actor)
	
	def addNPC(self,NPC):
		self.NPCs.append(NPC)
	
	def clearNPCs(self):
		self.NPCs = []
	
	def clearActors(self):
		self.savedStates[self.level]={}
		for actor in self.actors:
			if actor.rememberState:
				if type(actor)==Pushable:
					self.savedStates[self.level][actor.ID]=[actor.getState(),actor.getPos()]
				else:
					self.savedStates[self.level][actor.ID]=actor.getState()
					
		self.actors = []
	
	def clearTriggers(self):
		self.triggers = []
	
	def addTrigger(self,trigger):
		self.triggers.append(trigger)
	
	def setPlayer(self,player):
		self.player = player
	
	def getParty(self):
		return self.party
	
	def interact(self,interactor):
		for trigger in self.triggers:
			if trigger.getType() == "Action":
				if trigger.getArea().collidepoint(interactor.getCenter()):
					if trigger.getEffect() == "Area Change":
						self.loadNewAreaFunc(trigger.getNewAreaXML(),trigger.getNewArea())
						self.player.setPos(trigger.getPlayerPos())
					elif trigger.getEffect() == "Battle":
						if not trigger.trigger():
							self.battle(trigger.getEnemies(),trigger.getBG(),trigger.getBGFar(),trigger.getRandom())
					else:
						trigger.trigger(interactor,self.actors)
		if interactor.getID()=="Player":
			for NPC in self.NPCs:
				if NPC.getGameObject().getDistance(interactor)<20:
					interactor.setTalking(NPC)
					NPC.setTalking(True)
					NPC.getGameObject().setMoving(False)
					NPC.setState("Idle")
					interactor.graphicObject.setState("Idle")
					NPC.lookAt(interactor)
			for actor in self.actors:
				if actor.isPushable():
					if interactor.getPushing() != None:
						if interactor.getPushing() == actor:
							interactor.getPushing().togglePushed()
							interactor.setPushing(None)
					else:
						dx = actor.getMask().overlap_area(interactor.getMask(),(interactor.getX()-actor.getX()+1,interactor.getY()-actor.getY())) - actor.getMask().overlap_area(interactor.getMask(),(interactor.getX()-actor.getX()-1,interactor.getY()-actor.getY()))
						dy = actor.getMask().overlap_area(interactor.getMask(),(interactor.getX()-actor.getX(),interactor.getY()-actor.getY()+1)) - actor.getMask().overlap_area(interactor.getMask(),(interactor.getX()-actor.getX(),interactor.getY()-actor.getY()-1))
						if dx!=0:
							actor.togglePushed()
							interactor.setPushing(actor)
							interactor.setPushDir([True,False])
						elif dy!=0:
							actor.togglePushed()
							interactor.setPushing(actor)
							interactor.setPushDir([False,True])
	
	def moveCheck(self,mask,pos,vel):
		ret = [True,True]
		if mask!=None:
			if self.boundaries!=None:
				if self.boundaries.overlap(mask,pos):
					dx = self.boundaries.overlap_area(mask,(pos[0]+1,pos[1])) - self.boundaries.overlap_area(mask,(pos[0]-1,pos[1]))
					dy = self.boundaries.overlap_area(mask,(pos[0],pos[1]+1)) - self.boundaries.overlap_area(mask,(pos[0],pos[1]-1))
					
					if dx!=0 and vel[0]!=0:
						if dx/abs(dx)==vel[0]/abs(vel[0]):
							ret[0]=False
					if dy!=0 and vel[1]!=0:
						if dy/abs(dy)==vel[1]/abs(vel[1]):
							ret[1]=False
			for actor in self.actors:
				if actor.getMask() != None:
					if actor.getMask().overlap(mask,[pos[0]-actor.getX(),pos[1]-actor.getY()]):
						dx = actor.getMask().overlap_area(mask,(pos[0]-actor.getX()+1,pos[1]-actor.getY())) - actor.getMask().overlap_area(mask,(pos[0]-actor.getX()-1,pos[1]-actor.getY()))
						dy = actor.getMask().overlap_area(mask,(pos[0]-actor.getX(),pos[1]-actor.getY()+1)) - actor.getMask().overlap_area(mask,(pos[0]-actor.getX(),pos[1]-actor.getY()-1))
					
						if dx!=0 and vel[0]!=0:
							if dx/abs(dx)==vel[0]/abs(vel[0]):
								ret[0]=False
						if dy!=0 and vel[1]!=0:
							if dy/abs(dy)==vel[1]/abs(vel[1]):
								ret[1]=False
		return ret
	
	def battle(self,enemies,bg,bgFar,Random):
		if Random:
			num = random.choice([1,1,2,2,2,3])
			enemies = []
			for i in range(num):
				enemies.append(random.choice(self.enemies))
		self.battleFunc(enemies,bg,bgFar)
	
	def sleep(self):
		self.player.getParent().sleep()
		for char in self.player.getParent().getParty():
			char.sleep()
		self.player.getParent().getInventory().spendGold(25)
	
	def update(self,tick):
		if len(self.enemies)>0 and config.Difficulty > 0:
			if self.timeToBattle >= 0:
				if self.player.getMoving():
					self.timeToBattle -= tick
			else:
				bg = random.choice(self.battleBG)
				self.battle(self.enemies,bg[0],bg[1],True)
				self.timeToBattle = 5*random.random()+5
					
				
		
		self.player.update(tick,self.moveCheck)
		for actor in self.actors:
			actor.update(tick,self.moveCheck)
		for NPC in self.NPCs:
			NPC.update(tick,self.moveCheck)
		for trigger in self.triggers:
			if trigger.getType() == "Position":
				if trigger.getArea().collidepoint(self.player.getCenter()):
					if trigger.getEffect() == "Area Change":
						self.loadNewAreaFunc(trigger.getNewAreaXML(),trigger.getNewArea())
						self.player.setPos(trigger.getPlayerPos())
					elif trigger.getEffect() == "Battle":
						if not trigger.trigger():
							self.battle(trigger.getEnemies(),trigger.getBG(),trigger.getBGFar(),trigger.getRandom())
					else:
						if trigger.getArea().collidepoint(self.player.getCenter()):
							trigger.trigger(self.player,self.actors)
			elif trigger.getType() == "Object Position":
				for actor in self.actors:
					if actor.isPushable():
						if trigger.getArea().collidepoint(actor.getCenter()):
							trigger.trigger(actor,self.actors)
							actor.pushable=False
							actor.togglePushed()
							self.player.setPushing(None)
			if trigger.getEffect() == "SBSC":
				Pass = True
				for actor in self.actors:
					if trigger.getNeededStates().__contains__(actor.getID()):
						if actor.state != trigger.getState():
							Pass=False
				if Pass:
					trigger.trigger(self.player,self.actors)
			elif trigger.getEffect() == "TBSC":
				trigger.update(tick,self.actors)

## A container which contains information for game objects.
class GameObject(object):
	def __init__(self,pos,mask,spd,graphicObject,id,state="Idle",rememberState=True,parent=None):
		self.x=pos[0]
		self.y=pos[1]
		self.mask=mask
		self.ID = id
		
		self.parent=parent
		
		self.graphicObject = graphicObject
		
		self.spd=spd
		self.direction=[0,0]
		self.moving=False
		
		self.velocity=[0.0,0.0]
		
		self.state=state
		self.rememberState=rememberState
		
		self.pushing = None
		self.pushDir = [False,False]
	
	def getX(self):
		return int(self.x)
	
	def getY(self):
		return int(self.y)
	
	def getWidth(self):
		return self.graphicObject.getWidth()
	
	def getHeight(self):
		return self.graphicObject.getHeight()
	
	def getPos(self):
		return [int(self.x),int(self.y)]
	
	def getMask(self):
		return self.mask[self.state]
	
	def getVelocity(self):
		return self.velocity
	
	def getState(self):
		return self.state
	
	def setState(self,state):
		self.state=state
		self.graphicObject.setState(state)
	
	def getParent(self):
		return self.parent
	
	def setTalking(self,Talking):
		if self.parent != None:
			self.parent.setTalking(Talking)
	
	def getTalking(self):
		if self.parent != None:
			return self.parent.getTalking()
		else:
			return False
	
	def setShopping(self,Shopping):
		if self.parent != None:
			self.parent.setShopping(Shopping)
	
	def getShopping(self):
		if self.parent != None:
			return self.parent.getShopping()
		else:
			return False
	
	def setVelocity(self,vel):
		self.velocity=vel
	
	def setX(self,x):
		self.x=x
		self.graphicObject.setPos([self.x,self.y])
	
	def setY(self,y):
		self.y=y
		self.graphicObject.setPos([self.x,self.y])
	
	def setPos(self,pos):
		self.x=pos[0]
		self.y=pos[1]
		self.graphicObject.setPos(pos)
	
	def setDirection(self,direction):	#as vector
		self.direction=direction
	
	def getCenter(self):
		return [self.x+(self.graphicObject.getSprite().get_width()/2),self.y+(self.graphicObject.getSprite().get_height()/2)]
	
	def getMoving(self):
		return self.moving
	
	def getDistance(self,target):
		return math.sqrt((self.getCenter()[1]-target.getCenter()[1])**2+(self.getCenter()[0]-target.getCenter()[0])**2)
	
	def getID(self):
		return self.ID
	
	def isPushable(self):
		return False
	
	def setPushing(self,pushing):
		self.pushing = pushing
	
	def getPushing(self):
		return self.pushing
	
	def setPushDir(self,dire):
		self.pushDir=dire
	
	def setMoving(self,moving,direction=None):
		self.moving=moving
		if direction!=None:
			self.direction=direction
	
	def update(self,tick,moveCheck):
		self.velocity=[0,0]
		if self.moving:		#Caps Velocity at Speed
			if abs(self.velocity[0])<abs(self.spd*self.direction[0]):
				self.velocity[0]=(self.spd*self.direction[0])
			if abs(self.velocity[1])<abs(self.spd*self.direction[1]):
				self.velocity[1]=(self.spd*self.direction[1])
		else:
			self.velocity = [0.0,0.0]
		if self.velocity[0]!=0 and not(self.moving and abs(self.direction[0])==1):
			self.velocity[0]-=((self.velocity[0]/abs(self.velocity[0])))*tick
			if abs(self.velocity[0])<.01:
				self.velocity[0]=0.0
		if self.velocity[1]!=0 and not(self.moving and abs(self.direction[1])==1):
			self.velocity[1]-=((self.velocity[1]/abs(self.velocity[1])))*tick
			if abs(self.velocity[1])<.01:
				self.velocity[0]=0.0
		ret = moveCheck(self.getMask(),[int(self.x+self.velocity[0]*tick),int(self.y+self.velocity[1]*tick)],self.velocity)
		if self.pushing != None:
			if self.pushDir[0]:
				self.velocity[1] = 0
			elif self.pushDir[1]:
				self.velocity[0] = 0
			if self.pushing.push([self.velocity[0]*tick,self.velocity[1]*tick],moveCheck) == False:
				self.velocity = [0,0]
		if ret[0]:
			self.x+=self.velocity[0]*tick
		if ret[1]:
			self.y+=self.velocity[1]*tick
		self.graphicObject.setPos([int(self.x),int(self.y)])

class Pushable(GameObject):
	def __init__(self,pos,mask,area,spd,graphicObject,id,state="Idle",rememberState=True):
		GameObject.__init__(self,pos,mask,spd,graphicObject,id,state,rememberState)
		self.area=area
		self.pushable=True
		self.pushed=False
	
	def isPushable(self):
		return self.pushable
	
	def push(self,dire,moveCheck):
		if self.pushed:
			if self.x+dire[0]+self.graphicObject.getWidth()>=self.area.right and dire[0]>0:
				return False
			if self.x+dire[0]<=self.area.left and dire[0]<0:
				return False
			if self.y+dire[1]+self.graphicObject.getHeight()>=self.area.bottom and dire[1]>0:
				return False
			if self.y+dire[0]<=self.area.top and dire[1]<0:
				return False
			ret = moveCheck(self.getMask(),[int(self.x+dire[0]),int(self.y+dire[1])],dire)
			if ret[0]:
				self.x+=dire[0]
			if ret[1]:
				self.y+=dire[1]
		return True
	
	def togglePushed(self):
		self.pushed = not self.pushed
