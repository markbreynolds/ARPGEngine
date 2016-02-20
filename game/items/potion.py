import pygame
from pygame.locals import *

from item import Item
import config

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

#Potions:

class HealthPotion(Potion):
	def __init__(self,amount=1):
		Potion.__init__(self,"Health Potion",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionHealth.png").convert_alpha(),"HP",25,50,amount)

class ManaPotion(Potion):
	def __init__(self,amount=1):
		Potion.__init__(self,"Mana Potion",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionMana.png").convert_alpha(),"MP",25,50,amount)
		
class ElixirPotion(Potion):
	def __init__(self,amount=1):
		Potion.__init__(self,"Elixir",pygame.image.load(config.AssetPath+"Icons/Items/Potions/PotionElixir.png").convert_alpha(),"HP/MP",50,300,amount)
