## @package quests
#
#  This module contains the code for quests.

import json

import errors

## This object represents a quest and contains the relative information for it.
class Quest(object):

	## Constructor.
	#
	#  @param name The name or title for this quest.
	#  @param type
	#  @parblock
	#  What type of quest this is. (See getType() for more info).
	#
	#    Types:
	#    + "Main" - This quest is part of the main quest line and main plot.
	#    + "Side" - This quest if part of a side quest line or a sub plot.
	#
	#  @endparblock
	#  @param objectives A list containing Objective objects.
	#  @param reward
	#  @parblock
	#  A list of rewards the player gets for completing this quest.
	#
	#    Rewards:
	#    + "Gold #" - # amount of gold.
	#    + "Exp #" - # experience points.
	#    + "Item # itemArg1 itemArg2 ..." - The Item # with itemArg1 and itemArg2 etc.
	#
	#  @endparblock
	#  @param rewardHidden Whether or not the player should be able to see the reward for this quest.
	#  @param currentObjective What objective the player is currently working towards as a index of the @c objectives list.
	#  @param completed Whether or not this quest has been completed.
	def __init__(self,name,type,objectives,rewards=[None],rewardHidden=False,currentObjective=0,completed=False):
		self.name = name
		self.cat = type			#self.cat = Category
		self.objectives = objectives
		self.rewards = rewards
		self.rewardHidden = rewardHidden
		self.current = currentObjective
		self.completed = completed

	## Returns the name of this quest
	def getName(self):
		return self.name

	## Returns the type of this quest.
	#
	#  This is to be used for sorting quests.
	def getType(self):
		return self.cat

	## Returns the value to be used for sorting.
	def getSort(self):
		if not self.completed:
			return self.cat
		else:
			return "qCompleted"

	def getObjectiveCompleted(self,ident):
		for i in range(0,self.current):
			if self.objectives[i].getIdent()==ident:
				return True
		return False

	def getCurrentIdent(self):
		if not self.completed:
			return self.objectives[self.current].getIdent()
		return None

	## Returns the name of the current objective.
	def getCurrentName(self):
		if not self.completed:
			return self.objectives[self.current].getName()
		return None

	## Returns the formatted description of the current objective.
	def getCurrentDescription(self):
		if not self.completed:
			return self.objectives[self.current].getDescription()

	## Returns whether or not this quest has been finished.
	def getCompleted(self):
		return self.completed

	## Completes an objective.
	#
	#  If the current objective has the same identity as the objective trying
	#  to be completed, then the current objective is completed. If there are
	#  no more objectives to complete, then this quest is marked complete.
	#
	#  @param ident Identity to check against.
	def completeObjective(self,ident):
		if not self.completed and self.objectives[self.current].getIdent() == ident:
			self.current += 1
			#self.current,len(self.objectives)
			if self.current>=len(self.objectives):
				self.completed = True
			return True
		return False

	## Returns what rewards the player will get from this quest.
	#
	#  Returns @c None if no rewards are earned from this quest.
	def getRewards(self):
		return self.rewards

	## Returns whether or not the player should be able to see the rewards for this quest.
	def isRewardVisible(self):
		return not self.rewardHidden

## This object represents one of the steps in a quest.
class Objective(object):

	## Constructor.
	#
	#  @param ident The identity of this objective.
	#  @param name The name of this objective.
	#  @param description The formatted description of this objective. (See getDescription() for more info)
	def __init__(self,ident,name,description):
		self.ident = ident
		self.name = name
		self.description = description

	## Returns the identity of this objective.
	def getIdent(self):
		return self.ident

	## Returns the name of this objective.
	def getName(self):
		return self.name

	## Returns the formatted description of this objective.
	#
	#  This description should be a list of strings with each string representing one line of text. Line breaks must be manually
	#  inserted.
	def getDescription(self):
		return self.description

def loadQuest(xmlPath,quest):
	errors.info("Loading quest: "+quest)

	try:
		filer = open(xmlPath,"r")
	except IOError:
		errors.critical("Quest file not found.")
		exit()

	lines = filer.readlines()

	started=False

	questData = []

	for i in range(len(lines)):	#Strip Tabs and New Lines
		lines[i] = lines[i].lstrip("\t").rstrip("\n")

	for line in lines:	#Extract Quest Data
		if not started:
			if line == "<Quest "+quest+">":
				started=True
			continue
		if line == "</Quest>":
			break
		questData.append(line)

	args = {}
	objectives=[]

	i=0
	while i < len(questData):
		if questData[i].startswith("<Objective"):
			temp = {}
			n=1
			temp["ident"] = questData[i].lstrip("<Objective").rstrip(">").lstrip(" ")
			while questData[i+n]!="</Objective>":
				key = questData[i+n][1:questData[i+n].find(">")]
				value = questData[i+n][questData[i+n].find(">")+1:questData[i+n].find("<",questData[i+n].find(">"))]
				temp[key[0].lower()+key[1:]]=json.loads(value)
				n+=1
			objectives.append(temp)
			i+=n+1
		else:
			key = questData[i][1:questData[i].find(">")]
			value = questData[i][questData[i].find(">")+1:questData[i].find("<",questData[i].find(">"))]
			args[key[0].lower()+key[1:]]=json.loads(value)
			i+=1

	args["objectives"] = []
	for objArgs in objectives:
		args["objectives"].append(Objective(**objArgs))

	return Quest(**args)
