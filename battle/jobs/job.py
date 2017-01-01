from graphics.gui import Icons
from skill import PowerThrust, WaveSlash, Block, HpUp, DefUp
from skill import SpdUp
## Base class for all jobs.
class Job(object):

	## Constructor
	#
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

	## Returns how the character's stats are affected by their skills. Each stat
	#  is associated with a multiplier.
	#
	#  Should be overriden by subclass.
	def getSkillStats(self):
		return {"Hp":1,"Mp":1,"Atk":1,"Def":1,"Spd":1,"Vit":1,"Mag":1,"Res":1,"Con":1,"Mnd":1}

## Warrior job
class Warrior(Job):

	## Constructor
	#
	#  @param What level warrior the character is.
	def __init__(self,level):
		self.HpUp = HpUp()
		self.DefUp = DefUp()
		Job.__init__(self,"Warrior",[PowerThrust(),WaveSlash(),Block(),self.HpUp,self.DefUp],Icons.warriorSmall,level)

	## Returns the starting stats for this job.
	#
	#  Available Points: 12
	#  Speed starts at 20
	def getStartStats(self):
		return {"HP":10,"MP":1,"Atk":1,"Def":0,"Spd":20,"Vit":0,"Mag":0,"Res":0,"Con":0,"Mnd":0}

	## Returns how much the character's stats should change next level.
	#
	#  Available stat points per level: 5
	def getStatChange(self):
		if (self.level+1)%5==0:
			return {"HP":1,"MP":1,"Atk":1,"Def":1,"Spd":1,"Vit":0,"Mag":0,"Res":0,"Con":0,"Mnd":0}
		elif (self.level+1)%2==0:
			return {"HP":2,"MP":1,"Atk":1,"Def":0,"Spd":0,"Vit":1,"Mag":0,"Res":0,"Con":0,"Mnd":0}
		return {"HP":2,"MP":0,"Atk":1,"Def":1,"Spd":0,"Vit":1,"Mag":0,"Res":0,"Con":0,"Mnd":0}

	## Returns how the character's stats are affected by their skills.
	def getSkillStats(self):
		return {"Hp":self.HpUp.getStats()["Hp"],"Mp":1,"Atk":1,"Def":self.DefUp.getStats()["Def"],"Spd":1,"Vit":1,"Mag":1,"Res":1,"Con":1,"Mnd":1}

## Archer job
class Archer(Job):

	## Constructor
	#
	#  @param level Whata level archer the character is.
	def __init__(self,level):
		self.SpdUp = SpdUp()
		Job.__init__(self,"Archer",[self.SpdUp],Icons.archerSmall,level)

	## Returns the stating stats for this job.
	#
	#  Available Points: 12
	#  Speed starts at 20
	def getStartStats(self):
		return {"HP":7,"MP":2,"Atk":1,"Def":0,"Spd":22,"Vit":0,"Mag":0,"Res":0,"Con":0,"Mnd":0}

	## Returns how much the character's stats should change next level.
	#
	#  Available stat points per level: 5
	def getStatChange(self):
		if (self.level+1)%5==0:
			return {"HP":2,"MP":1,"Atk":0,"Def":1,"Spd":0,"Vit":1,"Mag":0,"Res":0,"Con":0,"Mnd":0}
		elif (self.level+1)%2==0:
			return {"HP":2,"MP":0,"Atk":1,"Def":0,"Spd":1,"Vit":1,"Mag":0,"Res":0,"Con":0,"Mnd":0}
		return {"HP":1,"MP":1,"Atk":1,"Def":0,"Spd":2,"Vit":0,"Mag":0,"Res":0,"Con":0,"Mnd":0}

	## Returns how the character's stats are affected by their skills.
	def getSkillStats(self):
		return {"Hp":1,"Mp":1,"Atk":1,"Def":1,"Spd":self.SpdUp.getStats()["Spd"],"Vit":1,"Mag":1,"Res":1,"Con":1,"Mnd":1}
