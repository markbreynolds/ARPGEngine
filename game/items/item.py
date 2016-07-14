import pygame
from pygame.locals import *

import config

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


#Items:

class EmptyPotion(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Empty Potion",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potions",10,amount)

	## see Item.getUsable().
	def getUsable(self):
		return False


class StrangePotion(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Strange Potion",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionStrange.png").convert_alpha(),"Potion",-1,amount)

	def getDescription(self):
		return "A strange potion with unknown effects."

	## see Item.getUsable().
	def getUsable(self):
		return False

#Test Items
class Test(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test1(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test1",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test2(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test2",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test3(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test3",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test4(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test4",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test5(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test5",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test6(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test6",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test7(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test7",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test8(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test8",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test9(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test9",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False

class Test10(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Test10",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionEmpty.png").convert_alpha(),"Potion",10,amount)
	## see Item.getUsable().
	def getUsable(self):
		return False
