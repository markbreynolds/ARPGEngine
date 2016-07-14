from game.items.item import *
from game.items.potion import *
from game.items.equipment import *
from game.items.brewing import *
import errors

class ItemFactory(object):
	items = {}

	@staticmethod
	def addItem(item,factory):
		ItemFactory.items[item] = factory

	@staticmethod
	def createItem(item,*args,**kwargs):
		if item not in ItemFactory.items:
			try:
				if ("import" in item) or (";" in item) or ("=" in item):
					errors.getLogger().critical("Unsafe attempt at object generation: "+item)
					exit()
				else:
					ItemFactory.items[item] = eval(item)
			except NameError:
				errors.error("Undefined item: "+item)
				return None
		return ItemFactory.items[item](*args,**kwargs)
