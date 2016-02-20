import pygame
from pygame.locals import *

from item import Item
import config

class Equipment(Item):
	def __init__(self,Name,Sprite,Slot,Stats,value,Amount=1):
		Item.__init__(self,Name,Sprite,"Equipment",value,Amount)
		self.slot=Slot
		self.stats=Stats
		self.equiped = False
	
	def equip(self):
		self.equiped = not self.equiped
	
	def getEquiped(self):
		return self.equiped
	
	def getSlot(self):
		return self.slot
	
	def getStats(self):
		return self.stats
	
	def getDescription(self):
		ret = ""
		for stat in self.stats:
			if self.stats[stat]>0:
				ret+= stat+": +"+str(self.stats[stat])+", "
			else:
				ret+= stat+": "+str(self.stats[stat])+", "
		ret = ret.rstrip(", ")
		return ret
	
	def getUsable(self):
		return False

class Body(Equipment):
	def __init__(self,name,sprite,stats,value,amount=1):
		Equipment.__init__(self,name,sprite,"Body",stats,value,amount)

## %Weapon Archtype
#
#  All weapons must be children of this class.
class Weapon(Equipment):
	
	## Constructor.
	#
	#  @param name Name of the weapon.
	#  @param sprite Sprite to show in inventory.
	#  @param stats A list of stats that will be affected by this weapon.
	#  @param atkBox The rectangle the defines how far the weapon can hit
	#  @param knockback How far this weapon will knock hit entities.
	#  @param hands How many hands it takes to wield this weapon. Determines whether this weapon can be dual-wielded or used with a shield. Must be either 1 or 2.
	#  @param style Which WeaponStyle to use when this weapon is equipped.
	#  @param animationPath The path to the weapon's animation xml
	#  @param recoveryTime How long the player must wait before they can attack again.
	#  @param amount How many of this weapon the player has.
	#  @param offset At what offset to draw the weapon in battle.
	def __init__(self,name,sprite,stats,atkBox,knockback,hands,style,animationPath,value,recoveryTime=.25,amount=1,offset=[0,0]):
		Equipment.__init__(self,name,sprite,"Arms",stats,value,amount)
		self.style = style
		self.atkBox = atkBox
		self.knockback = knockback
		self.hands = hands
		self.animationPath = animationPath
		self.recoveryTime = recoveryTime
		self.offset = offset
	
	## Returns the hitRange for this weapon.
	def getAtkBox(self):
		return self.atkBox
	
	## Returns the knockback for this weapon.
	def getKnockback(self):
		return self.knockback
	
	## Returns the WeaponStyle this weapon uses.
	def getStyle(self):
		return self.style
	
	## Returns number of hands needed to hold this weapon.
	def getHands(self):
		return self.hands
	
	## Returns how long the player must wait before they can attack again.
	def getRecoveryTime(self):
		return self.recoveryTime
	
	## Returns the path to the weapon's animation xml.
	def getAnimationPath(self):
		return self.animationPath
	
	## Returns at what offset to draw this weapon from the character.
	def getOffset(self):
		return self.offset

## One Handed Sword Parent Class
#
#  One handed swords should subclass this class.
class OHSword(Weapon):
	
	## Constructor
	#
	#  See Weapon for parameter functions.
	def __init__(self,name,sprite,stats,atkBox,knockback,animationPath,value,recoveryTime=.25,amount=1,offset=[0,-7]):
		#Style:				Name,Chain,reactionTime,frameOrder,frameDelay
		style = WeaponStyle("OHSword",3,.20,[["Attack1.png","Attack2.png","Attack3.png"],["Attack4.png","Attack5.png","Attack6.png"],["Attack1.png","Attack2.png","Attack3.png"]],[[.05,.15,.25],[.05,.15,.25],[.05,.15,.25]])
		Weapon.__init__(self,name,sprite,stats,atkBox,knockback,1,style,animationPath,value,recoveryTime,amount,offset)


#One Handed Swords:

##Iron Short Sword
class IronShortSword(OHSword):
	
	## Constructor
	#
	#  @param amount Amount of the item in this stack/inventory.
	def __init__(self):
		hitbox = [pygame.rect.Rect([-2,0,31,67]),pygame.rect.Rect([24,0,31,67])]
		OHSword.__init__(self,"Iron Short Sword",pygame.image.load(config.AssetPath+"Icons/Items/Weapons/IronShortSword.png"),{"Atk":10},hitbox,5,"Battle/Arms/Swords/IronShortSword/IronShortSword.xml",1000)

##Wooden Short Sword
class WoodenShortSword(OHSword):
	
	## Constructor
	#
	#  @param amount Amount of the item in this stack/inventory.
	def __init__(self):
		hitbox = [pygame.rect.Rect([-2,0,31,67]),pygame.rect.Rect([24,0,31,67])]
		OHSword.__init__(self,"Short Sword",pygame.image.load(config.AssetPath+"Icons/Items/Weapons/WoodenShortSword.png"),{"Atk":1},hitbox,5,"Battle/Arms/Swords/WoodenShortSword/WoodenShortSword.xml",100)

#Armor (Chest):
class LeatherTunic(Body):
	def __init__(self,color,amount=1):
		Body.__init__(self,color+" Leather Tunic",pygame.image.load(config.AssetPath+"Icons/Items/Armor/LeatherTunic.png").convert_alpha(),{"Def":1},200,amount)
		self.color=pygame.Color(color)
		self.sprite.fill(self.color,special_flags=BLEND_RGBA_MULT)

class IronChestplate(Body):
	def __init__(self,amount=1):
		Body.__init__(self,"Iron Chestplate",pygame.image.load(config.AssetPath+"Icons/Items/Armor/IronChestplate.png").convert_alpha(),{"Def":5},1000,amount)

#Weapon Styles:

## This object is a container for information about how different weapons are used by the player.
class WeaponStyle(object):
	
	## Constructor
	#
	#  @param name Name of this style, also the directory frames are in.
	#  @param chain The number of regular attacks that can be performed in a row.
	#  @param reactionTime How long the player has before the end of an attack, to begin the next attack in the chain. In seconds.
	#  @param frameOrder A 2d list, one list for each chain, each specifying the order of frames. See getFrameOrder() for more details.
	#  @param frameDelay A 2d list, one list for each chain, each specifying the delay between frames.
	def __init__(self,name,chain,reactionTime,frameOrder,frameDelay):
		self.name = name
		self.chain = chain
		self.reactionTime = reactionTime
		self.frameOrder = frameOrder
		self.frameDelay = frameDelay
	
	## Returns the name of the style
	def getName(self):
		return self.name
	
	## Returns the number of regular attacks that can be performed in a row.
	def getChain(self):
		return self.chain
	
	## Returns how long the player has before the end of an attack, to begin the next attack in the chain. In seconds.
	def getReactionTime(self):
		return self.reactionTime
	
	## Returns the order of frames for each attack in the chain.
	#
	#  Each frame is specified by its file name, ie: Attack1.png
	def getFrameOrder(self):
		return self.frameOrder
	
	## Returns a list of delays between frames, in seconds.
	#
	#  Each delay will correspond to a frame from frameOrder.
	def getFrameDelay(self):
		return self.frameDelay
