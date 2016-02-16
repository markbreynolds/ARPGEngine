## @package jobs
#  Documentation for the Jobs Module.
#
#  This module contains the code related to the jobs (called classes in game) and abilities.
#
#  In the code classes must be called jobs, because calling them classes would create a collision with the @c class keyword.
#
## Goals: V 0.2.0
#
#    -# Class objects - Done
#      - Warrior - Done
#    -# Leveling up - Done

import gui
import graphics
import pygame
from battle import Projectile

## Base class for all jobs.
class Job(object):
	
	## Constructor
	#  @param name The name of this job.
	#  @param skills A list of skills this job can have.
	#  @param icon The icon associated with this job.
	#  @param level What level in this job the character is.
	def __init__(self,name,skills,icon,level):
		self.name = name
		self.skills = skills
		self.icon = icon
		self.level = level
	
	## Returns this job's name.
	def getName(self):
		return self.name
	
	## Return the skills this job can learn.
	def getSkills(self):
		return self.skills
	
	def getUnlockedSkills(self):
		ret = []
		for skill in self.skills:
			if skill.getUnlocked():
				ret.append(skill)
		return ret
	
	## Return the icon associated with this job.
	def getIcon(self):
		return self.icon
	
	## Returns the description for this job.
	def getDescription(self):
		return self.name
	
	## Returns the starting stats for this job.
	#
	#  Should be overriden by subclass.
	def getStartStats(self):
		return {"HP":0,"MP":0,"Atk":0,"Def":0,"Spd":0,"Vit":0,"Mag":0,"Res":0,"Con":0,"Mnd":0}
	
	## Returns how much the character's stats should change next level.
	#  Can be based on a formula, but should only increase five points per level.
	#  
	#  Should be overriden by subclass.
	def getStatChange(self):
		return {"HP":0,"MP":0,"Atk":0,"Def":0,"Spd":0,"Vit":0,"Mag":0,"Res":0,"Con":0,"Mnd":0}

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


## Warrior job
class Warrior(Job):
	
	## Constructor
	#  @param What level warrior the character is.
	def __init__(self,level):
		Job.__init__(self,"Warrior",[WaveSlash(),Skill("Test1",None,1,1),Skill("Test2",None,1,1),Skill("Test3",None,1,1),Skill("Test4",None,1,1),Skill("Test5",None,1,1),Skill("Test6",None,1,1)],gui.Icons.warriorSmall,level)
	
	## Returns the starting stats for this job.
	def getStartStats(self):
		return {"HP":10,"MP":1,"Atk":1,"Def":0,"Spd":20,"Vit":0,"Mag":0,"Res":0,"Con":0,"Mnd":0}
	
	## Returns how much the character's stats should change next level.
	def getStatChange(self):
		if self.level%5==0:
			return {"HP":2,"MP":0,"Atk":1,"Def":1,"Spd":0,"Vit":1,"Mag":0,"Res":0,"Con":0,"Mnd":0}
		elif self.level%2==0:
			return {"HP":2,"MP":1,"Atk":1,"Def":0,"Spd":0,"Vit":1,"Mag":0,"Res":0,"Con":0,"Mnd":0}
		return {"HP":2,"MP":0,"Atk":1,"Def":0,"Spd":1,"Vit":1,"Mag":0,"Res":0,"Con":0,"Mnd":0}

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
		animr = graphics.Animation(graphics.AnimationFrame(pygame.image.load("Battle/Abilities/Warrior/WaveSlash.png").convert_alpha(),.5,None,"Idle"),None,"Idle")
		animl = graphics.Animation(graphics.AnimationFrame(pygame.transform.flip(pygame.image.load("Battle/Abilities/Warrior/WaveSlash.png").convert_alpha(),True,False),.5,None,"Idle"),None,"Idle")
		projectileGO = graphics.BattleGraphicObject({"Idle":[animl,animr]},(0,0),50)
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
	
	## Returns this skills projectile object.
	def getProjectile(self):
		animr = graphics.Animation(graphics.AnimationFrame(pygame.image.load("Battle/Abilities/Warrior/WaveSlash.png").convert_alpha(),.5,None,"Idle"),None,"Idle")
		animl = graphics.Animation(graphics.AnimationFrame(pygame.transform.flip(pygame.image.load("Battle/Abilities/Warrior/WaveSlash.png").convert_alpha(),True,False),.5,None,"Idle"),None,"Idle")
		projectileGO = graphics.BattleGraphicObject({"Idle":[animl,animr]},(0,0),50)
		return Projectile(projectileGO,[pygame.rect.Rect([2,0,30,70]),pygame.rect.Rect([20,0,30,70])],self.dmg*self.level,(0,0),125,150,None,piercing=True)
