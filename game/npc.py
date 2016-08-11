#npc.py

import random

import pygame
from pygame.locals import *

from game import player
from battle.jobs.job import Warrior
import config

#from graphics import GraphicObject, BattleGraphicObject, Animation, AnimationFrame
from game.engine import GameObject
from game.items.factory import ItemFactory
from battle.engine import BattleObject
from graphics.animation import Animation, AnimationFrame, loadAnimation
from graphics.overworld import GraphicObject
from graphics.battle import BattleGraphicObject

## A linked list node represeting part of a conversation.
#
# @note Branches require a link other than None.
class Dialog(object):

	## Constructor
	#
	#   @param Text A list containing text where each item reperesents a line.
	#      Line wrap occurs automatically.
	#   @param Options A list containing options for the player to choose from.
	#   @param Links A list containing references to other Dialog objects in the
	#      conversation. The first item in the @c Options list refers to the first
	#      item in the @c Links list, etc.
	#   @param Actions A list containing strings describing actions to take if a
	#      player chooses certain options. The first item in @c Options list
	#      refers to the first item in the @c Actions list. Actions include:
	#        + Buy
	#        + Sell
	#        + Sleep
	#        + Trigger
	#        + Quest
	#        + Branch
	#   @param Branches A list containing references to other Dialog objects to
	#      be used if the player selects certain options. The first item in the
	#      @c Options list refers to the first item in the @c Branches list.
	#   @param PreAction An action to be performed before the dialog is shown.
	#      Can be any of the actions that can be used in the @c Actions list.
	#   @param PreBranch A reference to the dialog to shown if the preaction
	#      calls for a branch.
	def __init__(self,Text,Options,Links,Actions=None,Branches=None,PreAction=None,PreBranch=None):
		self.text=Text
		self.options=Options
		self.links=Links
		if Actions == None:
			self.actions=[None]*len(Links)
		else:
			self.actions=Actions
		if Branches == None:
			self.branches = [None]*len(Links)
		else:
			self.branches = Branches
		self.preAction = PreAction
		self.preBranch = PreBranch

	## Returns a list containing the text for this dialog.
	def getText(self):
		return self.text

	## Returns a list containing the options for this dialog.
	def getOptions(self):
		return self.options

	## Returns a list containing the links for this dialog.
	def getLinks(self):
		return self.links

	## Returns a list containing the actions for this dialog.
	def getActions(self):
		return self.actions

	## Returns the preaction for this dialog.
	def getPreAction(self):
		return self.preAction

	## Return a list containing the branches for this dialog.
	def getBranches(self):
		return self.branches

	## returns the prebranch for this dialog.
	def getPreBranch(self):
		return self.preBranch


class NPC(player.Player):
	def __init__(self,Name,Id,Pos,Dialog,ClothingType,ClothingColor,HairType,HairColor,Icon=None,Wander=True,Shop=None,State="Idle",Direction=0):
		self.name=Name
		self.ID = Id
		self.icon=Icon
		self.dialog=Dialog
		self.wander=Wander
		self.wanderCount=0.0

		self.talking=False
		if Shop != None:
			self.shop = []
			for item in Shop:
				self.shop.append(ItemFactory.createItem(item))
		else:
			self.shop=Shop

		if ClothingType==None:
			ClothingType=random.randint(1,player.ClothingTypes)
		if ClothingColor==None:
			ClothingColor=random.choice(player.Colors)
		else:
			ClothingColor=player.Colors[ClothingColor]
		if HairType==None:
			HairType=random.randint(1,player.HairTypes)
		if HairColor==None:
			HairColor=random.choice(player.Colors)
		else:
			HairColor=player.Colors[HairColor]

		mask = pygame.mask.Mask((17,25))
		for x in range(6,11):
			for y in range(19,25):
				mask.set_at((x,y),1)

		self.graphicObject = GraphicObject(self.constructAnimations({"Idle":[Animation(None,None,"IdleN"),Animation(None,None,"IdleE"),Animation(None,None,"IdleS"),Animation(None,None,"IdleW")],"Run":[Animation(None,None,"RunN"),Animation(None,None,"RunE"),Animation(None,None,"RunS"),Animation(None,None,"RunW")]},ClothingType,ClothingColor,HairType,HairColor),[0.1,0.25],State,Direction)
		self.gameObject = GameObject([Pos[0],Pos[1]],{"Idle":mask},30,self.graphicObject,Id)

	def constructAnimations(self,animations,ClothingType,ClothingColor,HairType,HairColor):
		for dire in ["W","S","N"]:
			if dire == "W":
				direI = 3
			elif dire == "S":
				direI = 2
			elif dire == "N":
				direI = 0
			for frame in range(1,4):
				temp = pygame.surface.Surface((17,25),flags=SRCALPHA)
				clothes = pygame.image.load(config.AssetPath+"Player/Overworld/Clothes/Type"+str(ClothingType)+"/Walk"+dire+str(frame)+".png").convert_alpha()
				clothes.fill(ClothingColor,special_flags=BLEND_MULT)
				body = pygame.image.load(config.AssetPath+"Player/Overworld/Body/Type"+str(ClothingType)+"/Walk"+dire+str(frame)+".png").convert_alpha()
				hair = pygame.image.load(config.AssetPath+"Player/Overworld/Hair/Type"+str(HairType)+"/Walk"+dire+str(frame)+".png").convert_alpha()
				hair.fill(HairColor,special_flags=BLEND_MULT)
				temp.blit(clothes,(0,0))
				temp.blit(body,(0,0))
				temp.blit(hair,(0,0))
				if frame == 3:
					frame += 1
				animations["Run"][direI].addFrame(AnimationFrame(temp,0.25,None,frame))
				if frame == 2:
					animations["Run"][direI].addFrame(AnimationFrame(animations["Run"][direI].getSprite(),.25,None,3))
		i=0
		for frame in animations["Run"][3].getFrames():
			i+=1
			animations["Run"][1].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
		#Standing
		animations["Idle"][0].addFrame(AnimationFrame(animations["Run"][0].getSprite(),.1,None,0))
		animations["Idle"][1].addFrame(AnimationFrame(animations["Run"][1].getSprite(),.1,None,0))
		animations["Idle"][2].addFrame(AnimationFrame(animations["Run"][2].getSprite(),.1,None,0))
		animations["Idle"][3].addFrame(AnimationFrame(animations["Run"][3].getSprite(),.1,None,0))
		return animations

	def getShop(self):
		return self.shop

	def getIcon(self):
		return self.icon

	def getDialog(self):
		return self.dialog

	def setTalking(self,Talking):
		self.talking=Talking

	def lookAt(self,Target):
		if abs(Target.getY()-self.gameObject.getY())>abs(Target.getX()-self.gameObject.getX()):
			if Target.getY()>self.gameObject.getY():
				self.setDirection(2)
			else:
				self.setDirection(0)
		else:
			if Target.getX()>self.gameObject.getX():
				self.setDirection(1)
			else:
				self.setDirection(3)

	def update(self,tick,moveCheck):
		if self.wander and self.talking==False:
			if self.wanderCount <=0:
				self.wanderCount += random.random()*7
				dire=random.randint(0,3)
				self.setDirection(dire)
				if random.random()>.5:
					self.setState("Run")
					self.graphicObject.setFrame(1.0)
					direction = [0,0]
					if dire == 0:
						direction[1]=-1
					elif dire==1:
						direction[0]=1
					elif dire==2:
						direction[1]=1
					elif dire==3:
						direction[0]=-1
					self.gameObject.setMoving(True,direction)
					self.wanderCount/=2
				else:
					self.gameObject.setMoving(False)
					self.setState("Idle")
			else:
				self.wanderCount -= tick
		self.gameObject.update(tick,moveCheck)

## A NPC that can battle, usually party members.
class BattleNPC(player.Player):

	## Constructor
	def __init__(self,Name,Job,ClothingType,ClothingColor,HairType,HairColor):
		self.name = Name
		self.job = Job
		self.state = 0
		self.direction = 0

		self.inventory = Inventory()

		#For saving:
		self.clothingType=ClothingType
		self.clothingColor=ClothingColor
		self.hairType=HairType
		self.hairColor=HairColor

		self.icon=None

		mask = pygame.mask.Mask((17,25))
		for x in range(6,11):
			for y in range(19,25):
				mask.set_at((x,y),1)

		animations = self.constructAnimations(ClothingType,ClothingColor,HairType,HairColor,False)
		self.graphicObject = GraphicObject(animations,parent=self)
		self.gameObject = GameObject([0,0],{"Idle":mask},60,self.graphicObject,"Player",parent=self)

		animations = self.constructBattleAnimations(False)
		hitbox = [pygame.rect.Rect([16,7,28,61]),pygame.rect.Rect([7,8,28,60])]
		self.battleGraphicObject = BattleGraphicObject(animations,[10,145],20,weapon=self.getInventory().getArm1())
		self.battleObject = BattleObject(self.battleGraphicObject,hitbox,10,self.name,self.getInventory().getArm1(),level=1,exp=15,**self.job.getStartStats())

	## Returns if this is the player.
	def isPlayer(self):
		return False

## Special Non-Player Character.
#
#  Like an NPC, but rather than looking like a regular character,
#  their animations are loaded from a file.
class sNPC(NPC):
	def __init__(self,Name,Id,Pos,Dialog,AnimeXML,Icon=None,Wander=True,Shop=None,State="Idle",Direction=0):
		self.name=Name
		self.ID = Id
		self.icon=Icon
		self.dialog=Dialog
		self.wander=Wander
		self.wanderCount=0.0

		self.talking=False
		if Shop != None:
			self.shop = []
			for item in Shop:
				self.shop.append(ItemFactory.createItem(item))
		else:
			self.shop=Shop


		mask = pygame.mask.Mask((17,25))
		for x in range(6,11):
			for y in range(19,25):
				mask.set_at((x,y),1)

		animations = {"Idle":[loadAnimation(AnimeXML,"IdleN"),loadAnimation(AnimeXML,"IdleE"),loadAnimation(AnimeXML,"IdleS"),loadAnimation(AnimeXML,"IdleW")],"Run":[loadAnimation(AnimeXML,"RunN"),loadAnimation(AnimeXML,"RunE"),loadAnimation(AnimeXML,"RunS"),loadAnimation(AnimeXML,"RunW")]}
		self.graphicObject = GraphicObject(animations,[0.1,0.25],State,Direction)
		self.gameObject = GameObject([Pos[0],Pos[1]],{"Idle":mask},30,self.graphicObject,Id)

class Inventory(object):
	def __init__(self):
		self.head=None
		self.arm1=None
		self.arm2=None
		self.body=None
		self.legs=None
		self.boot=None

	## Returns what is equipped on the player's head.
	def getHead(self):
		return self.head

	## Returns what weapon is equipped.
	def getArm1(self):
		return self.arm1

	## Returns what shield is equipped.
	def getArm2(self):
		return self.arm2

	## Returns what is equipped on the player's body.
	def getBody(self):
		return self.body

	## Returns what is equipped on the player's legs.
	def getLegs(self):
		return self.legs

	## Returns what is equipped on the player's body.
	def getBoot(self):
		return self.boot

	def equip(self,item):
		if item.getSlot()=="Head":
			if self.head==None:
				self.head=item
				self.head.equip()
			else:
				self.head.equip()
				self.head=item
				self.head.equip()
		elif item.getSlot()=="Arms":
			if self.arm1==None:
				self.arm1=item
				self.arm1.equip()
			else:
				self.arm1.equip()
				self.arm1=item
				self.arm1.equip()
		elif item.getSlot()=="Body":
			if self.body==None:
				self.body=item
				self.body.equip()
			else:
				self.body.equip()
				self.body=item
				self.body.equip()
		elif item.getSlot()=="Legs":
			if self.legs==None:
				self.legs=item
				self.legs.equip()
			else:
				self.legs.equip()
				self.legs=item
				self.legs.equip()
		elif item.getSlot()=="Boot":
			if self.boot==None:
				self.boot=item
				self.boot.equip()
			else:
				self.boot.equip()
				self.boot=item
				self.boot.equip()

	def unequip(self,item):
		if item.getSlot()=="Head":
			if self.head==None:
				pass
			else:
				self.head.equip()
				self.head=None
		elif item.getSlot()=="Arms":
			if self.arm1==None:
				pass
			else:
				self.arm1.equip()
				self.arm1=None
		elif item.getSlot()=="Body":
			if self.body==None:
				pass
			else:
				self.body.equip()
				self.body=None
		elif item.getSlot()=="Legs":
			if self.legs==None:
				pass
			else:
				self.legs.equip()
				self.legs=None
		elif item.getSlot()=="Boot":
			if self.boot==None:
				pass
			else:
				self.boot.equip()
				self.boot=None
