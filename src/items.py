import config

import pygame
from pygame.locals import *

## Returns an Item object that correlates with the given string.
def getItemFromString(string):
	try:
		return itemList[string]
	except KeyError:
		print string+" item not found!"

#Archtypes:

class Item(object):
	def __init__(self,name,sprite,Type,value,amount=1):
		self.name=name
		self.sprite=sprite
		self.Type=Type
		self.amount=amount
		self.value=value
	
	def getName(self):
		return self.name
	
	def getSprite(self):
		return self.sprite
	
	## Returns how much this item can be purchased for.
	def getValue(self):
		return self.value
	
	def getType(self):
		return self.Type
	
	## Sets how many of this item is in this stack	
	def setAmount(self,amt):
		self.amount = amt
	
	def getAmount(self):
		return self.amount
	
	def getDescription(self):
		return ""
	
	## Gives an option to display a longer description.
	#
	#  defaults to the description returned by getDescription().
	def getLongDescription(self):
		return self.getDescription()
	
	def getEquiped(self):
		return False
	
	## Returns whether this item can be used.
	def getUsable(self):
		return True
	
	## Returns whether this item should target a specific charater.
	def getTarget(self):
		return None
	
	## Uses this item on @c target, returns @c True if item should be removed from inventory.
	#
	#  @param target The actor this item should be used on.
	def use(self,target):
		print "Used on "+str(target)
		return False

class Potion(Item):
	def __init__(self,name,sprite,effect,strength,value,amount=1):
		Item.__init__(self,name,sprite,"Potion",value,amount)
		self.effect=effect
		self.strength=strength
	
	## See item.getDescription().	
	def getDescription(self):
		if self.strength=="Full" or self.strength<=0:
			return str(self.strength)+" "+self.effect
		else:
			return "+"+str(self.strength)+" "+self.effect
	
	## See item.getLongDescription().
	def getLongDescription(self):
		if self.strength=="Full" or self.strength<=0:
			return "Restores "+str(self.strength)+" "+self.effect
		else:
			return "Restores +"+str(self.strength)+" "+self.effect
	
	## See item.getTarget()
	def getTarget(self):
		return True
	
	## See item.use().
	def use(self,target):
		targetb = target.getBattleObject()
		if self.effect == "HP":
			if targetb.getHP()==targetb.getHPM():
				return False
			else:
				targetb.setHP(min(targetb.getHPM(),targetb.getHP()+self.strength))
		elif self.effect == "MP":
			if targetb.getMP()==targetb.getMPM():
				return False
			else:
				targetb.setMP(min(targetb.getMPM(),targetb.getMP()+self.strength))
		self.amount-=1
		if self.amount <=0:
			return True
		return False

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
		OHSword.__init__(self,"Iron Short Sword",pygame.image.load(config.assetPath+"Icons/Items/Weapons/IronShortSword.png"),{"Atk":10},hitbox,5,"Battle/Arms/Swords/IronShortSword/IronShortSword.xml",1000)

##Wooden Short Sword
class WoodenShortSword(OHSword):
	
	## Constructor
	#
	#  @param amount Amount of the item in this stack/inventory.
	def __init__(self):
		hitbox = [pygame.rect.Rect([-2,0,31,67]),pygame.rect.Rect([24,0,31,67])]
		OHSword.__init__(self,"Short Sword",pygame.image.load(config.assetPath+"Icons/Items/Weapons/WoodenShortSword.png"),{"Atk":1},hitbox,5,"Battle/Arms/Swords/WoodenShortSword/WoodenShortSword.xml",100)

#Items:

class EmptyPotion(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Empty Potion",pygame.image.load(config.assetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	
	## see Item.getUsable().
	def getUsable(self):
		return False

class StrangePotion(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Strange Potion",pygame.image.load(config.assetPath+"Icons/Items/Potions/PotionStrange.png").convert_alpha(),"Potion",-1,amount)
	
	def getDescription(self):
		return "A strange potion with unknown effects."
	
	## see Item.getUsable().
	def getUsable(self):
		return False

#Potions:

class HealthPotion(Potion):
	def __init__(self,amount=1):
		Potion.__init__(self,"Health Potion",pygame.image.load(config.assetPath+"Icons/Items/Potions/PotionHealth.png").convert_alpha(),"HP",25,50,amount)

class ManaPotion(Potion):
	def __init__(self,amount=1):
		Potion.__init__(self,"Mana Potion",pygame.image.load(config.assetPath+"Icons/Items/Potions/PotionMana.png").convert_alpha(),"MP",25,50,amount)
		
class ElixirPotion(Potion):
	def __init__(self,amount=1):
		Potion.__init__(self,"Elixir",pygame.image.load(config.assetPath+"Icons/Items/Potions/PotionElixir.png").convert_alpha(),"HP/MP",50,300,amount)

#Armor (Chest):
class LeatherTunic(Body):
	def __init__(self,color,amount=1):
		Body.__init__(self,color+" Leather Tunic",pygame.image.load(config.assetPath+"Icons/Items/Armor/LeatherTunic.png").convert_alpha(),{"Def":1},200,amount)
		self.color=pygame.Color(color)
		self.sprite.fill(self.color,special_flags=BLEND_RGBA_MULT)

class IronChestplate(Body):
	def __init__(self,amount=1):
		Body.__init__(self,"Iron Chestplate",pygame.image.load(config.assetPath+"Icons/Items/Armor/IronChestplate.png").convert_alpha(),{"Def":5},1000,amount)

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

itemList = {"IronShortSword":IronShortSword,"WoodenShortSword":WoodenShortSword,"EmptyPotion":EmptyPotion,"StrangePotion":StrangePotion,"HealthPotion":HealthPotion,"ManaPotion":ManaPotion,"ElixirPotion":ElixirPotion,"LeatherTunic":LeatherTunic,"IronChestPlate":IronChestplate}
