import pygame

import config
from battle.engine import Projectile
from graphics.animation import Animation, AnimationFrame
from graphics.battle import BattleGraphicObject

## Base class for all skills.
class Skill(object):
	
	## Constructor
	#  @param name The name of this skill.
	#  @param state What state to go into when activated.
	#  @param cost Base amount of MP this skill costs to use.
	#  @param cooldown How long must be waited the user can do things again
	#  @param unlocked Whether or not this can be upgraded.
	def __init__(self,name,state,cost,cooldown,unlocked=True):
		self.name=name
		self.state=state
		self.unlocked=unlocked
		self.cost=cost
		self.cooldown=cooldown
		self.level=0
	
	## Uses this skill.
	def use(self,user):
		print self.name+" used!"
	
	## Returns how much MP this skill uses. This amount will scale linearly with level by default.
	def getCost(self):
		return self.cost*self.level
	
	## Returns how much MP this skill will use next level. This amount will scale linearly with level by default.
	def getNextCost(self):
		return self.cost*(self.level+1)
	
	## Returns if this skill is unlocked.
	def getUnlocked(self):
		return self.unlocked
	
	## Returns the name of this skill.
	def getName(self):
		return self.name
	
	## Returns the user state when this skill is used.
	def getState(self):
		return self.state
	
	## Returns the cooldown time for this skill.
	def getCooldown(self):
		return self.cooldown
	
	## Returns what type of skill this is.
	def getType(self):
		return None
	
	## Returns the info to display in the status bar for this skill.
	def getInfo(self):
		return "No Description Provided"
	
	## Returns the formatted description of this skill. Each line should be a seperate string in the list.
	def getDescription(self):
		return ["No Description","Provided"]
	
	## Returns how this skill will improve next level.
	def getChanges(self):
		return ["No Change Provided"]
	
	## Returns the type of skill.
	def getType(self):
		return "Generic"
	
	## Returns what level this skill is. If level 0, then has not been learned.
	def getLevel(self):
		return self.level
	
	## Increases the level of this skill by one.
	def levelUp(self):
		self.level += 1


## The base class for projectile based skills
class ProjectileSkill(Skill):

	## Constructor
	#  @param name The name of this skill.
	#  @param state What state to go into when activated.
	#  @param cost How much MP this skill costs to use.
	#  @param cooldown See Skill().
	#  @param projectile The projectile to be launched.
	#  @param unlocked Whether or not this can be upgraded.
	def __init__(self,name,state,cost,cooldown,projectile,unlocked=True):
		Skill.__init__(self,name,state,cost,cooldown,unlocked)
		self.projectile = projectile
	
	## Returns this skills projectile object.
	def getProjectile(self):
		return self.projectile.getCopy()
	
	## Uses this skill.
	#  @param user The character using this skill.
	def use(self,user):
		if user.getMP()>=self.getCost() and (user.getState()=="Idle" or user.getState()=="Run"):
			proj = self.getProjectile()
			proj.setPos([user.getGraphicObject().getX(),user.getGraphicObject().getY()])
			proj.setDirection(user.getDirection())
			proj.resetDist()
			proj.setParent(user)
			user.useSkill(self)
			return proj
		else:
			return False
	
	## Returns what type of skill this is.
	def getType(self):
		return "Projectile"


#Warrior Skills:

## Wave Slash Skill
#  Warrior level 1 skill
class WaveSlash(ProjectileSkill):
	
	## Constructor:
	def __init__(self):
		self.dmg = 3
		img = pygame.image.load(config.AssetPath+"Battle/Abilities/Warrior/WaveSlash.png").convert_alpha()
		animr = Animation(AnimationFrame(img,.5,None,"Idle"),None,"Idle")
		animl = Animation(AnimationFrame(pygame.transform.flip(img,True,False),.5,None,"Idle"),None,"Idle")
		projectileGO = BattleGraphicObject({"Idle":[animl,animr]},(0,0),50)
		proj = Projectile(projectileGO,[pygame.rect.Rect([2,0,30,70]),pygame.rect.Rect([20,0,30,70])],self.dmg,(0,0),125,150,None,piercing=True)
		ProjectileSkill.__init__(self,"Wave Slash","Attack1",1,.75,proj)
	
	## See Skill.getChanges().
	def getChanges(self):
		return ["+3 Damage","+1 MP Cost"]
	
	## See Skill.getInfo().
	def getInfo(self):
		return "Deals "+str(self.level*3)+" base damage"
	
	## Returns the formatted description of this skill.
	def getDescription(self):
		return ["A wave of energy","that slashes through","enemies."]
	
#	## Returns this skills projectile object.
#	def getProjectile(self):
#		animr = graphics.Animation(graphics.AnimationFrame(pygame.image.load(config.AssetPath+"Battle/Abilities/Warrior/WaveSlash.png").convert_alpha(),.5,None,"Idle"),None,"Idle")
#		animl = graphics.Animation(graphics.AnimationFrame(pygame.transform.flip(pygame.image.load(config.AssetPath+"Battle/Abilities/Warrior/WaveSlash.png").convert_alpha(),True,False),.5,None,"Idle"),None,"Idle")
#		projectileGO = graphics.BattleGraphicObject({"Idle":[animl,animr]},(0,0),50)
#		return Projectile(projectileGO,[pygame.rect.Rect([2,0,30,70]),pygame.rect.Rect([20,0,30,70])],self.dmg*self.level,(0,0),125,150,None,piercing=True)
