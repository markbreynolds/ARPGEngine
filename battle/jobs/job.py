from graphics.gui import Icons
from skill import WaveSlash

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

	## Returns a list of skills that have been unlocked.
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

## Warrior job
class Warrior(Job):

	## Constructor
	#  @param What level warrior the character is.
	def __init__(self,level):
		Job.__init__(self,"Warrior",[WaveSlash()],Icons.warriorSmall,level)

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
