## @package player
#  Documentation for the %Player Module.
#
#  This module contains the code related to the player and inventory.
#


"""
## Goals: V 0.2.0
#
#    -# Create Objects for each Class
#      - getDescription()
#      - getName()
#      - getAbilities()
#
"""

import pygame
from pygame.locals import *

from graphics import GraphicObject as GraphicsObject, BattleGraphicObject as BattleGraphicsObject, Animation, AnimationFrame
from game import GameObject as GamesObject
from battle import BattleObject as BattlesObject
import gui
import items
import jobs

HairTypes=4
ClothingTypes=1
Colors = [[255,0,0],[255,127,0],[255,255,0],[127,255,0],[0,255,0],[0,255,127],[0,255,255],[0,127,255],[0,0,255],[255,255,255],[127,127,127],[100,50,0]]
Classes = ["Warrior","Archer","Mage","Unarmed"]

## Object that contains all of the information for the player's character.
class Player(object):
	
	## Constructor
	#  @param name The player's name
	#  @param job The player's class (see jobs)
	#  @param clothingType The style of clothing to use. (see Player/Overworld/Clothes/Type# and Player/Overworld/Body/Type#)
	#  @param clothingColor What color the clothing should be.
	#  @param hairType What style of hair to use. (see Player/Overworld/Hair/Type#)
	#  @param hairColor What color the hair should be.
	#  @param preview Whether or not this Player is being used in the character creator. If @c True not all animations will be generated.
	def __init__(self,name,clothingType,clothingColor,hairType,hairColor,preview=False):
		self.name = name
		self.job = jobs.Warrior(1)
		self.state = 0
		self.direction = 0
		
		self.inventory=Inventory([items.EmptyPotion(3),items.HealthPotion(5),items.StrangePotion(20),items.LeatherTunic("Purple"),items.IronChestplate(),items.WoodenShortSword()])
		self.party=[]
		self.skills={"S1":None,"S1U":None,"S1R":None,"S1D":None,"S1L":None}
		
		self.talking = False
		self.shopping = False
		self.canMove = True
		
		#For saving:
		self.clothingType=clothingType
		self.clothingColor=clothingColor
		self.hairType=hairType
		self.hairColor=hairColor
		
		self.icon=None
		
		mask = pygame.mask.Mask((17,25))
		for x in range(6,11):
			for y in range(19,25):
				mask.set_at((x,y),1)
		
		animations = self.constructAnimations(clothingType,clothingColor,hairType,hairColor,preview)
		self.graphicObject = GraphicsObject(animations,parent=self)
		self.gameObject = GamesObject([0,0],{"Idle":mask},60,self.graphicObject,"Player",parent=self)
		
		animations = self.constructBattleAnimations(preview)
		hitbox = [pygame.rect.Rect([16,7,28,61]),pygame.rect.Rect([7,8,28,60])]
		self.battleGraphicObject = BattleGraphicsObject(animations,[10,145],20,weapon=self.getInventory().getArm1())
		self.battleObject = BattlesObject(self.battleGraphicObject,hitbox,10,self.name,self.getInventory().getArm1(),level=1,exp=15,**self.job.getStartStats())

	## Constructs the overworld animations for this character.
	#
	#  @param clothingType The style of clothing to use. (see Player/Overworld/Clothes/Type# and Player/Overworld/Body/Type#)
	#  @param clothingColor What color the clothing should be.
	#  @param hairType What style of hair to use. (see Player/Overworld/Hair/Type#)
	#  @param hairColor What color the hair should be.
	#  @param preview Whether or not this Player is being used in the character creator. If @c True not all animations will be generated.
	def constructAnimations(self,ClothingType,ClothingColor,HairType,HairColor,Preview=False):
		animations = {"Idle":[Animation(None,None,"IdleN"),Animation(None,None,"IdleE"),Animation(None,None,"IdleS"),Animation(None,None,"IdleW")],"Walk":[Animation(None,None,"WalkN"),Animation(None,None,"WalkE"),Animation(None,None,"WalkS"),Animation(None,None,"WalkW")]}
		
		self.icon = pygame.surface.Surface((27,27),flags=SRCALPHA)
		base=pygame.image.load("Player/Overworld/Profile/Base.png").convert_alpha()
		clothes=pygame.image.load("Player/Overworld/Profile/Shirt.png").convert_alpha()
		clothes.fill(ClothingColor,special_flags=BLEND_MULT)
		hair=pygame.image.load("Player/Overworld/Profile/Hair"+str(HairType)+".png").convert_alpha()
		hair.fill(HairColor,special_flags=BLEND_MULT)
		
		self.icon.blit(base,[0,0])
		self.icon.blit(clothes,[0,0])
		self.icon.blit(hair,[0,0])
		
		for dire in ["W","S","N"]:
			if dire == "W":
				direI = 3
			elif dire == "S":
				direI = 2
			elif dire == "N":
				direI = 0
			for frame in range(1,4):
				hair = pygame.image.load("Player/Overworld/Hair/Type"+str(HairType)+"/Walk"+dire+str(frame)+".png").convert_alpha()
				hair.fill(HairColor,special_flags=BLEND_MULT)
				temp = pygame.surface.Surface((17,25),flags=SRCALPHA)
				clothes = pygame.image.load("Player/Overworld/Clothes/Type"+str(ClothingType)+"/Walk"+dire+str(frame)+".png").convert_alpha()
				clothes.fill(ClothingColor,special_flags=BLEND_MULT)
				body = pygame.image.load("Player/Overworld/Body/Type"+str(ClothingType)+"/Walk"+dire+str(frame)+".png").convert_alpha()
				temp.blit(clothes,(0,0))
				temp.blit(body,(0,0))
				temp.blit(hair,(0,0))
				if frame == 3:
					frame += 1
				animations["Walk"][direI].addFrame(AnimationFrame(temp,0.20,None,frame-1))
				if frame == 2:
					animations["Walk"][direI].addFrame(AnimationFrame(animations["Walk"][direI].getSprite(),.20,None,2))
		i=0
		for frame in animations["Walk"][3].getFrames():
			i+=1
			animations["Walk"][1].addFrame(AnimationFrame(pygame.transform.flip(frame.image,True,False),frame.delay,None,i-1))
		#Standing
		animations["Idle"][0].addFrame(AnimationFrame(animations["Walk"][0].getSprite(),.1,None,0))
		animations["Idle"][1].addFrame(AnimationFrame(animations["Walk"][1].getSprite(),.1,None,0))
		animations["Idle"][2].addFrame(AnimationFrame(animations["Walk"][2].getSprite(),.1,None,0))
		animations["Idle"][3].addFrame(AnimationFrame(animations["Walk"][3].getSprite(),.1,None,0))		
		
		return animations
	
	## Constructs the battle animations for this character.
	#
	#  @param preview Whether or not this Player is being used in the character creator. If @c True not all animations will be generated.
	def constructBattleAnimations(self,Preview=False):
		animations = {"Idle":[Animation(None,None,"IdleW"),Animation(None,None,"IdleE")],"Run":[Animation(None,None,"RunW"),Animation(None,None,"RunE")],"Death":[Animation(None,None,"DeathW"),Animation(None,None,"DeathE")],"Dead":[Animation(None,None,"DeadW"),Animation(None,None,"DeadE")]}
		
		weapon = self.getInventory().getArm1()
		if weapon == None:
			style = "Unarmed"
			styleName = style
		else:
			style = weapon.getStyle()
			styleName = style.getName()
		
		#Idle:
		temp = pygame.surface.Surface((52,70),flags=SRCALPHA)
		
		body = pygame.image.load("Player/Battle/"+styleName+"/Body/Type"+str(self.clothingType)+"/Idle1.png").convert_alpha()
		hair = pygame.image.load("Player/Battle/"+styleName+"/Hair/Type"+str(self.hairType)+"/Idle1.png").convert_alpha()
		hair.fill(self.hairColor,special_flags=BLEND_MULT)
		shirt= pygame.image.load("Player/Battle/"+styleName+"/Shirt/Type"+str(self.clothingType)+"/Idle1.png").convert_alpha()
		shirt.fill(self.clothingColor,special_flags=BLEND_MULT)
		
		temp.blit(shirt,(0,0))
		temp.blit(body,(0,0))
		temp.blit(hair,(0,0))
		animations["Idle"][1].addFrame(AnimationFrame(temp,.5,None,0))
		
		#Run:
		for i in range(1,5):
			temp = pygame.surface.Surface((52,70),flags=SRCALPHA)
			
			body = pygame.image.load("Player/Battle/"+styleName+"/Body/Type"+str(self.clothingType)+"/Walk"+str(i)+".png").convert_alpha()
			hair = pygame.image.load("Player/Battle/"+styleName+"/Hair/Type"+str(self.hairType)+"/Walk"+str(i)+".png").convert_alpha()
			hair.fill(self.hairColor,special_flags=BLEND_MULT)
			shirt= pygame.image.load("Player/Battle/"+styleName+"/Shirt/Type"+str(self.clothingType)+"/Walk"+str(i)+".png").convert_alpha()
			shirt.fill(self.clothingColor,special_flags=BLEND_MULT)
			
			temp.blit(shirt,(0,0))
			temp.blit(body,(0,0))
			temp.blit(hair,(0,0))
			animations["Run"][1].addFrame(AnimationFrame(temp,.17,None,i-1))
		
		##Attacking:
		if style == "Unarmed":
			chain = 3
			frameOrder = [["Attack1.png","Idle1.png"],["Attack2.png","Attack3.png","Attack2.png"],["Attack1.png","Idle1.png"]]
			frameDelay = [[.15,.15],[.15,.15,.15],[.15,.15]]
		else:
			chain = style.getChain()
			frameOrder = style.getFrameOrder()
			frameDelay = style.getFrameDelay()
		
		for i in range(1,chain+1):
			animations["Attack"+str(i)] = [Animation(None,None,"Attack"+str(i)+"W"),Animation(None,None,"Attack"+str(i)+"E")]
			for j in range(0,len(frameOrder[i-1])):
				temp = pygame.surface.Surface((52,70),flags=SRCALPHA)
					
				body = pygame.image.load("Player/Battle/"+styleName+"/Body/Type"+str(self.clothingType)+"/"+frameOrder[i-1][j]).convert_alpha()
				hair = pygame.image.load("Player/Battle/"+styleName+"/Hair/Type"+str(self.hairType)+"/"+frameOrder[i-1][j]).convert_alpha()
				hair.fill(self.hairColor,special_flags=BLEND_MULT)
				shirt= pygame.image.load("Player/Battle/"+styleName+"/Shirt/Type"+str(self.clothingType)+"/"+frameOrder[i-1][j]).convert_alpha()
				shirt.fill(self.clothingColor,special_flags=BLEND_MULT)
				
				temp.blit(shirt,(0,0))
				temp.blit(body,(0,0))
				temp.blit(hair,(0,0))
				animations["Attack"+str(i)][1].addFrame(AnimationFrame(temp,frameDelay[i-1][j],None,j))
		#Death
		temp = pygame.surface.Surface((70,70),flags=SRCALPHA)
		body = pygame.image.load("Player/Battle/"+styleName+"/Body/Type"+str(self.clothingType)+"/Death1.png").convert_alpha()
		hair = pygame.image.load("Player/Battle/"+styleName+"/Hair/Type"+str(self.hairType)+"/Death1.png").convert_alpha()
		hair.fill(self.hairColor,special_flags=BLEND_MULT)
		shirt= pygame.image.load("Player/Battle/"+styleName+"/Shirt/Type"+str(self.clothingType)+"/Death1.png").convert_alpha()
		shirt.fill(self.clothingColor,special_flags=BLEND_MULT)
		temp.blit(shirt,(0,0))
		temp.blit(body,(0,0))
		temp.blit(hair,(0,0))
		animations["Death"][1].addFrame(AnimationFrame(temp,.2,None,0))
		temp = pygame.surface.Surface((70,70),flags=SRCALPHA)
		body = pygame.image.load("Player/Battle/"+styleName+"/Body/Type"+str(self.clothingType)+"/Dead.png").convert_alpha()
		hair = pygame.image.load("Player/Battle/"+styleName+"/Hair/Type"+str(self.hairType)+"/Dead.png").convert_alpha()
		hair.fill(self.hairColor,special_flags=BLEND_MULT)
		shirt= pygame.image.load("Player/Battle/"+styleName+"/Shirt/Type"+str(self.clothingType)+"/Dead.png").convert_alpha()
		shirt.fill(self.clothingColor,special_flags=BLEND_MULT)
		temp.blit(shirt,(0,0))
		temp.blit(body,(0,0))
		temp.blit(hair,(0,0))
		animations["Dead"][1].addFrame(AnimationFrame(temp,.5,None,0))
		#animations[2][1].append(temp)
		#animations[4][1].append(temp)
		
		#temp = pygame.surface.Surface((52,70),flags=SRCALPHA)
			
		#body = pygame.image.load("Player/Battle/"+Weapon+"/Body/Type"+str(ClothingType)+"/Idle1.png").convert_alpha()
		#hair = pygame.image.load("Player/Battle/"+Weapon+"/Hair/Type"+str(HairType)+"/Idle1.png").convert_alpha()
		#hair.fill(HairColor,special_flags=BLEND_MULT)
		#shirt= pygame.image.load("Player/Battle/"+Weapon+"/Shirt/Type"+str(ClothingType)+"/Idle1.png").convert_alpha()
		#shirt.fill(ClothingColor,special_flags=BLEND_MULT)
		
		#temp.blit(shirt,(0,0))
		#temp.blit(body,(0,0))
		#temp.blit(hair,(0,0))
		#animations[2][1].append(temp)
		#animations[4][1].append(temp)
		
		#for i in range(2,4):
			#temp = pygame.surface.Surface((52,70),flags=SRCALPHA)
			
			#body = pygame.image.load("Player/Battle/"+Weapon+"/Body/Type"+str(ClothingType)+"/Attack"+str(i)+".png").convert_alpha()
			#hair = pygame.image.load("Player/Battle/"+Weapon+"/Hair/Type"+str(HairType)+"/Attack"+str(i)+".png").convert_alpha()
			#hair.fill(HairColor,special_flags=BLEND_MULT)
			#shirt= pygame.image.load("Player/Battle/"+Weapon+"/Shirt/Type"+str(ClothingType)+"/Attack"+str(i)+".png").convert_alpha()
			#shirt.fill(ClothingColor,special_flags=BLEND_MULT)
			
			#temp.blit(shirt,(0,0))
			#temp.blit(body,(0,0))
			#temp.blit(hair,(0,0))
			#animations[3][1].append(temp)
		
		#temp = pygame.surface.Surface((52,70),flags=SRCALPHA)
		
		#body = pygame.image.load("Player/Battle/"+Weapon+"/Body/Type"+str(ClothingType)+"/Attack2.png").convert_alpha()
		#hair = pygame.image.load("Player/Battle/"+Weapon+"/Hair/Type"+str(HairType)+"/Attack2.png").convert_alpha()
		#hair.fill(HairColor,special_flags=BLEND_MULT)
		#shirt= pygame.image.load("Player/Battle/"+Weapon+"/Shirt/Type"+str(ClothingType)+"/Attack2.png").convert_alpha()
		#shirt.fill(ClothingColor,special_flags=BLEND_MULT)
		
		#temp.blit(shirt,(0,0))
		#temp.blit(body,(0,0))
		#temp.blit(hair,(0,0))
		#animations[3][1].append(temp)
		
		##Create Mirroring
		#Idle
		temp = animations["Idle"][1].getFrames()
		i=0
		for frame in temp:
			animations["Idle"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
			i+=1
		#Run
		temp = animations["Run"][1].getFrames()
		i=0
		for frame in temp:
			animations["Run"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
			i+=1
		#Attack
		for i in range(1,chain+1):
			temp = animations["Attack"+str(i)][1].getFrames()
			j = 0
			for frame in temp:
				animations["Attack"+str(i)][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,j))
				j+=1
		#Death
		temp = animations["Death"][1].getFrames()
		i=0
		for frame in temp:
			animations["Death"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
			i+=1
		temp = animations["Dead"][1].getFrames()
		i=0
		for frame in temp:
			animations["Dead"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
			i+=1
		
		##And linking...
		for i in range(1,chain+1):
			animations["Attack"+str(i)][0].setNextAnimation(animations["Idle"][0])
			animations["Attack"+str(i)][1].setNextAnimation(animations["Idle"][1])
		animations["Death"][0].setNextAnimation(animations["Dead"][0])
		animations["Death"][1].setNextAnimation(animations["Dead"][1])
		
		return animations
	
	## Returns whether or not the character can move.
	def getCanMove(self):
		return self.canMove
	
	## Sets whether or not the character can move.
	#
	#  This should be set to false if the player is for example sleeping.
	def setCanMove(self,canMove):
		self.canMove = canMove
	
	## Recovers all this character's health, mana, and removes status effects.
	def sleep(self):
		self.battleObject.Hp = self.battleObject.HpM
		self.battleObject.Mp = self.battleObject.MpM
		self.battleObject.status = 0b0
	
	## Returns this character's Job object.
	def getClass(self):
		return self.job
	
	## Returns this character's BattleObject.
	def getBattleObject(self):
		return self.battleObject
	
	## Returns a list of other character's in the party.
	def getParty(self):
		return self.party
	
	## Returns this object's sprite.
	#
	#  Apparently used by the character creator? Probable shouldn't be used.
	def getSprite(self):
		return self.graphicObject.getSprite()
	
	## Sets the overworld state of this character.
	def setState(self,state):
		self.state=state
		self.graphicObject.setState(state)
	
	## Sets what direction this character is facing on the overworld.
	#
	#  @param direction A number from 0 to 3 representing N to W respectively.
	def setDirection(self,direction): #Direction is a number from 0 to 3
		self.direction=direction
		self.graphicObject.setDirection(direction)
	
	## Returns this character's portrait icon.
	def getIcon(self):
		return self.icon
	
	## Returns this character's name.
	def getName(self):
		return self.name
	
	## Returns what direction this character is facing on the overworld.
	def getDirection(self):
		return self.direction
	
	## Returns the skill binded to that button.
	def getSkill(self,button):
		return self.skills[button]
	
	## Binds a skill to a button:
	def setSkill(self,button,skill):
		self.skills[button] = skill
	
	## Returns this character's GameObject.
	def getGameObject(self):
		return self.gameObject
	
	## Returns this character's GraphicObject.
	def getGraphicObject(self):
		return self.graphicObject
	
	## Sets who this character is talking to.
	def setTalking(self,talking):
		self.talking = talking
	
	## Returns who this character is talking to.
	def getTalking(self):
		return self.talking
	
	## Sets whether or not this character is shopping.
	def setShopping(self,shopping):
		self.shopping = shopping
	
	## Returns whether or not this character is shopping.
	def getShopping(self):
		return self.shopping
	
	## Returns this character's inventory.
	def getInventory(self):
		return self.inventory
	
	## Returns this character's overworld mask.
	def getMask(self):
		return self.gameObject.getMask()
	
	## Returns if this object is moving.
	def getMoving(self):
		return self.gameObject.getMoving()
	
	## Levels up this character and changes their stats.
	def levelUp(self):
		self.job.level+=1
		self.battleObject.levelUp(**self.job.getStatChange())
	
	## Returns this class's job
	def getJob(self):
		return self.job
	
	## Makes this character equip an item and adjusted their stats.
	def equip(self,item):
		self.inventory.equip(item)
		for stat in item.getStats():
			self.battleObject.statOffsets[stat]+=item.getStats()[stat]
	
	## Makes this character unequip an item and adjusted their stats.
	def unequip(self,item):
		self.inventory.unequip(item)
		for stat in item.getStats():
			self.battleObject.statOffsets[stat]-=item.getStats()[stat]
	
	## Returns if this is the player.
	def isPlayer(self):
		return True
	
	## Updates this objects GraphicObject.
	def update(self,tick):
		self.graphicObject.update(tick)

## This object keeps track of all of the items and gold for the player.
class Inventory(object):
	def __init__(self,Items=None,gold=1000,size=0):
		if Items==None:
			self.items=[]
		else:
			self.items=Items
		self.gold=gold
		
		self.size=size
		
		self.head=None
		self.arm1=None
		self.arm2=None
		self.body=None
		self.legs=None
		self.boot=None
	
	## Adds an item to the inventory
	def addItem(self,item):
		for invenItem in self.items:
			if type(item) == type(invenItem):
				invenItem.amount+=1
				return
		else:
			self.items.append(item)
	
	## Returns the item in the players inventory that is the same as @c item.
	#
	#  Default: None
	def hasItem(self,item):
		for invenItem in self.items:
			if type(item) == type(invenItem):
				return invenItem
		return None
	
	## Adds gold.
	def addGold(self,amt):
		self.gold+=amt
	
	## Removes gold.
	def spendGold(self,amt):
		self.gold-=amt
	
	## Returns a list of the items the player has.
	def getItems(self):
		return self.items
	
	## Returns how much gold the player has.
	def getGold(self):
		return self.gold
	
	## Returns how much gold the player has formatted nicely as a string.
	def getGoldS(self):
		if self.gold > 9999:
			return str(self.gold/1000)+"K"
		return str(self.gold)
	
	## Returns the size of the inventory.
	#
	#  0 = Normal size
	#  1 = Upgraded
	def getSize(self):
		return self.size
	
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
	
	## Equips an item in the appropiate equipment slot.
	#
	#  @param item An Equipment object.
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
	
	## Unequips an item and empties the appropiate equipment slot.
	#
	#  @param item An Equipment object.
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
	
	
	## Compares a peice of equipment with the currently equipt equipment.
	#
	#  Returns the stat value of @c item if nothing is equipt in the equivelant slot.
	#
	#  @param item An Equipment object.
	#  @param stat A string of the stat to be compared.
	def getComparison(self,item,stat):
		new = item.getStats()[stat]
		if item.getSlot()=="Head":
			if self.head == None:
				return new
			else:
				return new-self.head.getStats()[stat]
		elif item.getSlot()=="Arms":
			if self.arm1 == None:
				return new
			else:
				return new-self.arm1.getStats()[stat]
		elif item.getSlot()=="Body":
			if self.body == None:
				return new
			else:
				return new-self.body.getStats()[stat]
		elif item.getSlot()=="Legs":
			if self.legs == None:
				return new
			else:
				return new-self.legs.getStats()[stat]
		elif item.getSlot()=="Boot":
			if self.boot == None:
				return new
			else:
				return new-self.boot.getStats()[stat]
	
	## Updates the inventory in order to keep it clean.
	def update(self):
		while self.items[-1]==None:
			self.items.pop(-1)
	
	## Removes an item from the player's inventory.
	#
	#  @param item Item to remove.
	def remove(self,item):
		if item.getEquiped():
			self.unequip(item)
		self.items.remove(item)
		self.update()

## Character Creator.
#  @Deprecated See gui.CharacterCreator.
def Creator(screen,clockObject,inputEngine):
	editing = True
	editingName = False
	timer = 0
	
	fontObject = gui.font
	
	sel = 0
	Name = "Markus Calarkus"	#Change to ""
	Class = 0
	ClothingType=1
	ClothingColor=0
	HairType=1
	HairColor=0

	preview = Player("Null","Null",ClothingType,Colors[ClothingColor],HairType,Colors[HairColor],True)
	preview.setState(1)
	preview.setDirection(2)
	while editing:
		screen.fill((0,0,0))
		screen.fill(gui.ColorDark,[4,4,122,147])
		screen.fill(gui.Color,[5,5,120,145])
		if sel == 0:
			if editingName:
				screen.blit(fontObject.render("Name: "+Name+"|",False,gui.ColorSel,gui.Color),(10,10))
			else:
				screen.blit(fontObject.render("Name: "+Name,False,gui.ColorSel,gui.Color),(10,10))
		else:
			screen.blit(fontObject.render("Name: "+Name,False,gui.ColorFont,gui.Color),(10,10))
		if sel == 1:
			screen.blit(fontObject.render("Class:   "+Classes[Class],False,gui.ColorSel,gui.Color),(10,24))
		else:
			screen.blit(fontObject.render("Class:   "+Classes[Class],False,gui.ColorFont,gui.Color),(10,24))
		if sel == 2:
			screen.blit(fontObject.render("Clothing: "+str(ClothingType),False,gui.ColorSel,gui.Color),(10,52))
		else:
			screen.blit(fontObject.render("Clothing: "+str(ClothingType),False,gui.ColorFont,gui.Color),(10,52))
		if sel == 3:
			screen.blit(fontObject.render("Color: "+str(ClothingColor),False,gui.ColorSel,gui.Color),(10,66))
		else:
			screen.blit(fontObject.render("Color: "+str(ClothingColor),False,gui.ColorFont,gui.Color),(10,66))
		if sel == 4:
			screen.blit(fontObject.render("Hair: "+str(HairType),False,gui.ColorSel,gui.Color),(10,94))
		else:
			screen.blit(fontObject.render("Hair: "+str(HairType),False,gui.ColorFont,gui.Color),(10,94))
		if sel == 5:
			screen.blit(fontObject.render("Color: "+str(HairColor),False,gui.ColorSel,gui.Color),(10,110))
		else:
			screen.blit(fontObject.render("Color: "+str(HairColor),False,gui.ColorFont,gui.Color),(10,110))
		if sel == 6:
			screen.blit(fontObject.render("Ok",False,gui.ColorSel,gui.Color),(10,138))
		else:
			screen.blit(fontObject.render("Ok",False,gui.ColorFont,gui.Color),(10,138))
		
		if Classes[Class]=="Warrior":
			screen.blit(gui.Icons.warriorSmall,(44,22))
		elif Classes[Class]=="Archer":
			screen.blit(gui.Icons.archerSmall,(44,22))
		elif Classes[Class]=="Mage":
			screen.blit(gui.Icons.mageSmall,(44,22))
		
		if len(Name)>14:
			screen.fill(gui.ColorDark,[4,224,313,14])
			screen.fill(gui.Color,[5,225,311,12])
			screen.blit(fontObject.render("*Warning:Your name is long, it may not display properly",False,gui.ColorBold),(9,226))
		
		for event in inputEngine.getInput(True):
			if event[0] == "Quit":
				pygame.quit()
				exit()
			elif event[1] == "Down":
				if editingName:
					if event[0].startswith("Raw_"):
						char = event[0][4:]
						if len(char) == 1:
							if (pygame.key.get_mods() & KMOD_LSHIFT)|(pygame.key.get_mods() & KMOD_RSHIFT):
								Name += char.capitalize()
							else:
								Name += char
						else:
							if event[0] == "Raw_backspace":
								Name = Name[0:-1]
							elif event[0] == "Raw_space":
								Name += " "
					elif event[0] == "Accept":
						editingName = False
				else:
					if event[0] == "Down":
						if sel == 6:
							sel=0
						else:
							sel+=1
					elif event[0] == "Up":
						if sel == 0:
							sel=6
						else:
							sel-=1
					elif event[0] == "Right":
						if sel == 1:
							if Class == 2:
								Class = 0
							else:
								Class+= 1
						elif sel == 2:
							if ClothingType == ClothingTypes:
								ClothingType = 1
							else:
								ClothingType+= 1
						elif sel == 3:
							if ClothingColor == len(Colors)-1:
								ClothingColor = 0
							else:
								ClothingColor+= 1
						elif sel == 4:
							if HairType == HairTypes:
								HairType = 1
							else:
								HairType+= 1
						elif sel == 5:
							if HairColor == len(Colors)-1:
								HairColor = 0
							else:
								HairColor+=1
						d = preview.getDirection()
						f = preview.getGraphicObject().getFrame()
						preview = Player("Null","Null",ClothingType,Colors[ClothingColor],HairType,Colors[HairColor],True)
						preview.setState(1)
						preview.setDirection(d)
						preview.getGraphicObject().setFrame(f)
					elif event[0] == "Left":
						if sel == 1:
							if Class == 0:
								Class = 2
							else:
								Class-= 1
						elif sel == 2:
							if ClothingType == 1:
								ClothingType = ClothingTypes
							else:
								ClothingType-= 1
						elif sel == 3:
							if ClothingColor == 0:
								ClothingColor = len(Colors)-1
							else:
								ClothingColor-= 1
						elif sel == 4:
							if HairType == 1:
								HairType = HairTypes
							else:
								HairType-= 1
						elif sel == 5:
							if HairColor == 0:
								HairColor = len(Colors)-1
							else:
								HairColor-=1
						d = preview.getDirection()
						f = preview.getGraphicObject().getFrame()
						preview = Player("Null","Null",ClothingType,Colors[ClothingColor],HairType,Colors[HairColor],True)
						preview.setState(1)
						preview.setDirection(d)
						preview.getGraphicObject().setFrame(f)
					elif event[0] == "Accept":
						if sel == 0:
							editingName = True
						elif sel == 1:
							if Class == 3:
								Class = 0
							else:
								Class+= 1
						elif sel == 2:
							if ClothingType == ClothingTypes:
								ClothingType = 1
							else:
								ClothingType+= 1
						elif sel == 3:
							if ClothingColor == len(Colors)-1:
								ClothingColor = 0
							else:
								ClothingColor+= 1
						elif sel == 4:
							if HairType == HairTypes:
								HairType = 1
							else:
								HairType+= 1
						elif sel == 5:
							if HairColor == len(Colors)-1:
								HairColor = 0
							else:
								HairColor+=1
						elif sel == 6:
							return Player(Name,Classes[Class],ClothingType,Colors[ClothingColor],HairType,Colors[HairColor])
						if sel!=0 and sel!=6:
							d = preview.getDirection()
							f = preview.getGraphicObject().getFrame()
							preview = Player("Null","Null",ClothingType,Colors[ClothingColor],HairType,Colors[HairColor],True)
							preview.setState(1)
							preview.setDirection(d)
							preview.getGraphicObject().setFrame(f)
		
		tick = clockObject.tick()/1000.0
		timer += tick
		if timer >= 2:
			if preview.getDirection() == 3:
				preview.setDirection(0)
			else:
				preview.setDirection(preview.getDirection()+1)
			timer = 0
		preview.update(tick)
		screen.blit(pygame.transform.scale2x(preview.getSprite()),(150,50))
		screen.fill(gui.ColorDark,[200,50,29,29])
		screen.fill(gui.Color,[201,51,27,27])
		screen.blit(preview.getIcon(),[201,51])
		screen.update()
		pygame.display.update()
		
		
