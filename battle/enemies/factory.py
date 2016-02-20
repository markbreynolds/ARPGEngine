from battle.enemies.enemy import *
import errors

class EnemyFactory(object):
	enemies = {}
	
	@staticmethod
	def addEnemy(enemy,factory):
		EnemyFactory.enemies[enemy] = factory
	
	@staticmethod
	def createEnemy(enemy,*args,**kwargs):
		if enemy not in EnemyFactory.enemies:
			try:
				if ("import" in enemy) or (";" in enemy) or ("=" in enemy):
					errors.getLogger().critical("Unsafe attempt at object generation: "+enemy)
					exit()
				else:
					EnemyFactory.enemies[enemy] = eval(enemy)
			except NameError:
				errors.getLogger().error("Undefined item: "+enemy)
				return None
		return EnemyFactory.enemies[enemy](*args,**kwargs)
