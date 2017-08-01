import pygame

import config
from battle.engine import Projectile
from graphics.animation import Animation, AnimationFrame
from graphics.battle import BattleGraphicObject

## Base class for all skills.
class Skill(object):

	## Constructor
	#  @param name The name of this skill.
	#  @param reqs The requirements to unlock this skill.
	#  @param unlocked Whether or not this can be leveled up yet.
	def __init__(self,name,reqs={},unlocked=True):
		self.name=name
		self.unlocked=unlocked
		self.reqs=reqs
		self.level=0


	## Returns if this skill is unlocked.
	def getUnlocked(self):
		return self.unlocked

	## Returns the name of this skill.
	def getName(self):
		return self.name

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

	## Returns the requirements to unlock this skill.
	def getReqs(self):
		return self.reqs

	## Returns what level this skill is. If level 0, then has not been learned.
	def getLevel(self):
		return self.level

	## Returns True if this class is a subclass of ActiveSkill,
	def isActiveSkill(self):
		return False

	## Increases the level of this skill by one.
	def levelUp(self):
		self.level += 1

## The base class for skills that have to be activated.
class ActiveSkill(Skill):

	## Constructor
	#  @param name The name of this skill.
	#  @param state What state to go into when activated.
	#  @param cost Base amount of MP this skill costs to use.
	#  @param cooldown How long must be waited until the user can do things again
	#  @param unlocked Whether or not this can be upgraded.
	def __init__(self,name,state,cost,cooldown,reqs={},unlocked=True):
		Skill.__init__(self,name,reqs,unlocked)
		self.cost=cost
		self.cooldown=cooldown
		self.state=state

	## Returns how much MP this skill uses. This amount will scale linearly with level by default.
	def getCost(self):
		return self.cost*self.level

	## Returns how much MP this skill will use next level. This amount will scale linearly with level by default.
	def getNextCost(self):
		return self.cost*(self.level+1)

	## Returns the cooldown time for this skill.
	def getCooldown(self):
		return self.cooldown

	## Returns the user state when this skill is used.
	def getState(self):
		return self.state

	## Returns True if this class is a subclass of ActiveSkill,
	def isActiveSkill(self):
		return True

## The base class for skills that changes stats permanently.
class StatSkill(Skill):

	## Constructor
	#
	#  @param stats A list of stat multipliers
	def __init__(self,name,stats,reqs={},unlocked=True):
		Skill.__init__(self,name,reqs,unlocked)
		self.stats = stats

	## Returns a list of stat multipliers this skill provides
	def getStats(self):
		return self.stats

	## Returns the type of skill this is.
	def getType(self):
		return "Stat"

## The base class for temporary stat boost skills.
class BuffSkill(ActiveSkill):

	## Constructor
	#
	#  @param stats A list of stat multipliers.
	#  @param duration How long the stat changes last.
	def __init__(self,name,state,cost,cooldown,stats,duration,reqs={},unlocked=True):
		ActiveSkill.__init__(self,name,state,cost,cooldown,reqs,unlocked)
		self.stats = stats
		self.duration = duration

	## Returns a list of stat multipliers this skill provides
	def getStats(self):
		return self.stats

	## Returns how long this skill's stat boosts last for.
	def getDuration(self):
		return self.duration

	## Returns the type of skill this is.
	def getType(self):
		return "Buff"

## The base class for short range damage skills.
class MeleeSkill(ActiveSkill):

	## Constructor
	#
	#  @param hitbox A Rect object describing this skill's damage box.
	#  @param vel The initial velocity after using this skill.
	def __init__(self,name,state,cost,cooldown,hitbox,vel=[0.0,0.0],reqs={},unlocked=True):
		ActiveSkill.__init__(self,name,state,cost,cooldown,reqs,unlocked)
		self.hitbox = hitbox
		self.vel=vel

	## Returns this skill's damage box.
	def getHitBox(self):
		return self.hitbox

	## Returns the initial velocity an actor should have after using this skill.
	def getVel(self):
		return self.vel

	## Returns the damage multiplier for this skill.
	def getDmgMult(self):
		return 0

	## Returns what type of damage this skill does.
	def getDmgType(self):
		return "Physical"

	## Returns what type of skill this is.
	def getType(self):
		return "Melee"

## The base class for projectile based skills
class ProjectileSkill(ActiveSkill):

	## Constructor
	#  @param name The name of this skill.
	#  @param state What state to go into when activated.
	#  @param cost How much MP this skill costs to use.
	#  @param cooldown See ActiveSkill().
	#  @param projectile The projectile to be launched.
	#  @param unlocked Whether or not this can be upgraded.
	def __init__(self,name,state,cost,cooldown,projectile,reqs={},unlocked=True):
		ActiveSkill.__init__(self,name,state,cost,cooldown,reqs=reqs,unlocked=unlocked)
		self.projectile = projectile

	## Returns this skills projectile object.
	def getProjectile(self):
		return self.projectile.getCopy()

	## Returns what type of damage this skill does.
	def getDmgType(self):
		return "Physical"

	## Returns the damage multiplier for this skill.
	def getDmgMult(self):
		return 0

	## Returns what type of skill this is.
	def getType(self):
		return "Projectile"

## Spd+ Skill
#  Archer level 1 skill.
class SpdUp(StatSkill):

	## Constructor
	def __init__(self):
		StatSkill.__init__(self,"Spd+",{"Spd":1})

	## See Skill.getInfo().
	def getInfo(self):
		return "Raises Spd by "+str(1+.25*self.level)+"x"

	## See Skill.getDescription().
	def getDescription(self):
		return ["Raises Speed permanently."]

	## See Skill.getChanges().
	def getChanges(self):
		return ["Raises Speed by "+str(1+.25*(self.level+1))+"x (+.25 Spd)"]

	## See Skill.levelUp().
	def levelUp(self):
		self.level+=1
		self.stats["Spd"]+=.25
