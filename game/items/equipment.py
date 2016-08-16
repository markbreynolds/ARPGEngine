import pygame
from pygame.locals import *

from item import Item
import config

class Equipment(Item):
	def __init__(self,Name,Sprite,Slot,Stats,value,Reqs={},Amount=1):
		Item.__init__(self,Name,Sprite,"Equipment",value,Amount)
		self.slot=Slot
		self.stats=Stats
		self.reqs=Reqs
		self.equiped=False

	def equip(self):
		self.equiped = not self.equiped

	def getEquiped(self):
		return self.equiped

	def getSlot(self):
		return self.slot

	def getStats(self):
		return self.stats

	def getReqs(self):
		return self.reqs

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
	def __init__(self,name,sprite,stats,value,reqs={},amount=1):
		Equipment.__init__(self,name,sprite,"Body",stats,value,reqs,amount)

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
	#  @param projectile A dictionary that provides arguements for a Projectile that will be launched when this weapon is used. If does not launch a projectile set to @c None.
	#  @param skills A list of the skills this weapon can perform. The weapon must have animations for all of these skills.
	def __init__(self,name,sprite,stats,atkBox,knockback,hands,style,animationPath,value,recoveryTime=.25,reqs={},amount=1,offset=[0,0],projectile=None,skills=[]):
		Equipment.__init__(self,name,sprite,"Arms",stats,value,reqs,amount)
		self.style = style
		self.atkBox = atkBox
		self.knockback = knockback
		self.hands = hands
		self.animationPath = animationPath
		self.recoveryTime = recoveryTime
		self.offset = offset
		self.projectile=projectile
		self.skills=set(skills)

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

	## Returns information on the projectile this weapon launches.
	def getProjectile(self):
		return self.projectile

	## Returns a set containing the skills this weapon
	def getSkills(self):
		return self.skills

## One Handed Sword Parent Class
#
#  One handed swords should subclass this class.
class OHSword(Weapon):

	## Constructor
	#
	#  See Weapon for parameter descriptions.
	def __init__(self,name,sprite,stats,atkBox,knockback,animationPath,value,recoveryTime=.25,reqs={},amount=1,offset=[0,-7]):
		#Style:				Name,Chain,reactionTime,frameOrder,frameDelay
		style = ComboWeaponStyle("OHSword",3,.20,[["Attack1.png","Attack2.png","Attack3.png"],["Attack4.png","Attack5.png","Attack6.png"],["Attack1.png","Attack2.png","Attack3.png"]],[[.05,.15,.25],[.05,.15,.25],[.05,.15,.25]])
		Weapon.__init__(self,name,sprite,stats,atkBox,knockback,1,style,animationPath,value,recoveryTime,reqs,amount,offset,skills=["Thrust"])

## Bow Parent Class
#
#  Bows should subclass this class.
class Bow(Weapon):

	## Constructor
	#
	#  See Weapon for parameter descriptions.
	def __init__(self,name,sprite,stats,knockback,animationPath,value,recoveryTime=.25,reqs={},amount=1,offset=[0,0]):
		style = ChargeWeaponStyle("Bow",5,2,.35,["Attack1.png","Attack2.png","Attack3.png","Attack4.png","Attack5.png"])
		proj = {"graphicObject":"Battle/Projectiles/WoodArrow.png","atkbox":[pygame.rect.Rect([0,0,14,25]),pygame.rect.Rect([0,0,14,25])],"damage":stats["Atk"],"pos":[0,20],"speed":500,"dist":400,"parent":None}
		Weapon.__init__(self,name,sprite,stats,None,knockback,2,style,animationPath,value,recoveryTime,reqs,amount,offset,projectile=proj)

#One Handed Swords:

##Iron Short Sword
class IronShortSword(OHSword):

	## Constructor
	#
	#  @param amount Amount of the item in this stack/inventory.
	def __init__(self):
		hitbox = [pygame.rect.Rect([-2,0,31,67]),pygame.rect.Rect([24,0,31,67])]
		OHSword.__init__(self,"Iron Short Sword",pygame.image.load(config.AssetPath+"Icons/Items/Weapons/IronShortSword.png"),{"Atk":10},hitbox,5,"Battle/Arms/Swords/IronShortSword/IronShortSword.xml",1000,reqs={"Class":["Warrior"]})

##Wooden Short Sword
class WoodenShortSword(OHSword):

	## Constructor
	#
	#  @param amount Amount of the item in this stack/inventory.
	def __init__(self):
		hitbox = [pygame.rect.Rect([-2,0,31,67]),pygame.rect.Rect([24,0,31,67])]
		OHSword.__init__(self,"Wooden Short Sword",pygame.image.load(config.AssetPath+"Icons/Items/Weapons/WoodenShortSword.png"),{"Atk":1},hitbox,5,"Battle/Arms/Swords/WoodenShortSword/WoodenShortSword.xml",100,reqs={"Class":["Warrior"]})

#Bows:

##Wooden Short Bow
class WoodenShortBow(Bow):

	## Constructor
	def __init__(self):
		Bow.__init__(self,"Wooden Short Bow",pygame.image.load(config.AssetPath+"Icons/Items/Weapons/WoodenShortBow.png"),{"Atk":1},2,"Battle/Arms/Bows/WoodenShortBow/WoodenShortBow.xml",100,reqs={"Class":["Archer"]})

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
#
#  This particular weapon style describes a weapon that uses successive hits linked
#  into combos.
class ComboWeaponStyle(object):

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

	## Returns the type of weapon style this is.
	def getType(self):
		return "Combo"

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

## This object is a container for information about how different weapons are used by the player.
#
#  This weapon style describes a weapon that must be charged before each each attack.
#  Charging longer will provide a stronger attack.
class ChargeWeaponStyle(object):

	## Constructor
	#
	#  @param name Name of this style, also the directory frames are in.
	#  @param stages The number of charging stages this style has.
	#  @param preStages The number of stages that must be charged through before
	#    the weapon can attack.
	#  @param chargeTime How long each stage must charge before going to the
	#    next stage.
	#  @param frameOrder A list specifying the order of frames. See getFrameOrder()
	#    for more details.
	def __init__(self,name,stages,preStages,chargeTime,frameOrder):
		self.name = name
		self.stages = stages
		self.preStages = preStages
		self.frameOrder = frameOrder
		self.chargeTime = chargeTime

	## Returns the name of the style
	def getName(self):
		return self.name

	## Returns the type of weapon style this is.
	def getType(self):
		return "Charge"

	def getStages(self):
		return self.stages

	def getPreStages(self):
		return self.preStages

	def getChargeTime(self):
		return self.chargeTime

	def getFrameOrder(self):
		return self.frameOrder
