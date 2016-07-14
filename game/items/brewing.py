import pygame

from item import Item
import config

class GreenSlimeball(Item):
	def __init__(self,amount=1):
		Item.__init__(self,"Green Slime",pygame.image.load(config.AssetPath+"Icons/Items/Brewing/GreenSlimeball.png").convert_alpha(),"Craftable",2,amount)

	## see Item.getUsable().
	def getUsable(self):
		return False
