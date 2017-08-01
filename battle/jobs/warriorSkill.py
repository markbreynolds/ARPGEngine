import pygame

import config
from battle.engine import Projectile
from graphics.animation import Animation, AnimationFrame
from graphics.battle import BattleGraphicObject
from skill import ProjectileSkill, MeleeSkill, StatSkill

#Warrior Skills:

## Wave Slash Skill
#  Warrior level 1 skill.
class WaveSlash(ProjectileSkill):

	## Constructor:
	def __init__(self):
		self.dmg = 0.1		# (self.dmg*self.level) + base = damage multiplier
		img = pygame.image.load(config.AssetPath+"Battle/Abilities/Warrior/WaveSlash.png").convert_alpha()
		animr = Animation(AnimationFrame(img,.5,None,"Idle"),None,"Idle")
		animl = Animation(AnimationFrame(pygame.transform.flip(img,True,False),.5,None,"Idle"),None,"Idle")
		projectileGO = BattleGraphicObject({"Idle":[animl,animr]},(0,0),50)
		proj = Projectile(projectileGO,[pygame.rect.Rect([2,0,30,70]),pygame.rect.Rect([20,0,30,70])],self.dmg,(0,0),125,150,None,piercing=True)
		ProjectileSkill.__init__(self,"Wave Slash","Attack1",1,.75,proj,reqs={})

	## See Skill.getChanges().
	def getChanges(self):
		return [str(1.1+(self.level+1)*self.dmg)+"x Damage (+.1)",str(self.level+1)+" MP Cost (+1)"]

	## See Skill.getInfo().
	def getInfo(self):
		return "Deals "+str(1.1+self.level*self.dmg)+"x damage."

	## Returns the formatted description of this skill.
	def getDescription(self):
		return ["A wave of energy that slashes", "through enemies."]

	## Returns the damage multiplier for this skill.
	def getDmgMult(self):
		return 1.1+self.level*self.dmg

## Power Thrust Skill
#  Warrior level 1 skill.
class PowerThrust(MeleeSkill):
	def __init__(self):
		self.dmg = 0.2		# (self.dmg*self.level) + base = damage multiplier
		hitbox = [pygame.rect.Rect([-50,0,100,100]),pygame.rect.Rect([0,0,100,100])]
		MeleeSkill.__init__(self,"Power Thrust","Thrust",0,.75,hitbox,vel=[75.0,0])

	## See Skill.getChanges().
	def getChanges(self):
		return [str(1.0+(self.level+1)*self.dmg)+"x Damage (+.2)",str(self.level+1)+" MP Cost (+1)"]

	## See Skill.getInfo().
	def getInfo(self):
		return "Deals "+str(1.0+self.level*self.dmg)+"x damage."

	## Returns the formatted description of this skill.
	def getDescription(self):
		return ["A powerful forward thrust that", "pierces through enemies."]

	## Returns the damage multiplier for this skill.
	def getDmgMult(self):
		return 1.0+self.level*self.dmg

## Upper Cut Skill
#  Warrior level 1 skill.
class UpperCut(MeleeSkill):
	def __init__(self):
		self.dmg = 0.2		# (self.dmg*self.level) + base = damage multiplier
		hitbox = [pygame.rect.Rect([-50,0,100,100]),pygame.rect.Rect([0,0,100,100])]
		MeleeSkill.__init__(self,"Upper Cut","UpperCut",0,.75,hitbox,vel=[25.0,175.0])

	## See Skill.getChanges().
	def getChanges(self):
		return [str(1.2+(self.level+1)*self.dmg)+"x Damage (+.2)",str(self.level+1)+" MP Cost (+1)"]

	## See Skill.getInfo().
	def getInfo(self):
		return "Deals "+str(1.2+self.level*self.dmg)+"x damage."

	## Returns the formatted description of this skill.
	def getDescription(self):
		return ["A quick slash upward that", "launches enemies into the air."]

	## Returns the damage multiplier for this skill.
	def getDmgMult(self):
		return 1.2+self.level*self.dmg

## HP+ Skill
#  Warrior level 1 skill.
class HpUp(StatSkill):

	## Constructor
	def __init__(self):
		StatSkill.__init__(self,"Hp+",{"Hp":1.0})

	## See Skill.getInfo().
	def getInfo(self):
		return "Raises max HP by "+str(self.stats["Hp"])+"x"

	## See Skill.getDescription().
	def getDescription(self):
		return ["Raises maximum HP permanently."]

	## See Skill.getChanges().
	def getChanges(self):
		return ["Raises max HP by "+str(self.stats["Hp"]+.2)+"x (+.2x HP)"]

	## See Skill.levelUp().
	def levelUp(self):
		self.level+=1
		self.stats["Hp"]+=.2

## Def+ Skill
#  Warrior level 1 skill.
class DefUp(StatSkill):

	## Constructor
	def __init__(self):
		StatSkill.__init__(self,"Def+",{"Def":1})
		#StatSkill.__init__(self,"Def+",{"Def":1},unlocked=False)	# Why was this locked??

	## See Skill.getInfo().
	def getInfo(self):
		return "Raises Def by "+str(1+.1*self.level)+"x"

	## See Skill.getDescription().
	def getDescription(self):
		return ["Raises Defense permanently."]

	## See Skill.getChanges().
	def getChanges(self):
		return ["Raises Defense by "+str(1+.1*(self.level+1))+"x (+.1x Def)"]

	## See Skill.levelUp().
	def levelUp(self):
		self.level+=1
		self.stats["Def"]+=.1
