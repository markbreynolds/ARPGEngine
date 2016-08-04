## @package triggers
#  Documentation for the Triggers Module.
#
#  Contains the code for trigger containers.
#
## Goals: V 0.1.0a
#    -# Battle Trigger - Done
#      - Monster - Done
## Goals: V 0.2.0a
#    -# <b>Cutscene Trigger</b>
#      - <b>Point to Cutscene File</b>
#      - <b>After Battle Cutscene</b>
## Goals: V 0.3.0a
#

import errors

## Container for trigger information.
#
#  Contains basic information about triggers.
class Trigger(object):

	## Constructor.
	#
	#  @param Type
	#  @parblock
	#  Category or type of trigger:
	#
	#    Types:
	#    + "Action" - Requires the action button to be pressed to activate.
	#    + "Position" - Requires the player to stand in a specific area to activate.
	#    + "Object Position" - Requires an object (i.e. a Pushable) to be moved to a specific area.
	#    + "Dialog" - Requires the player to say the right thing in the dialog with a character.
	#    + "Other" - Any other type of trigger that has other activation methods, i.e. SBSC.
	#
	#  @endparblock
	#  @param Area The area that this trigger can be activated from.
	#  @param Id This trigger's ID.
	#  @param Effect
	#  @parblock
	#  What this trigger does.
	#
	#    Effects:
	#    + "State Set" - Sets the state of @c Target. See StateSetTrigger().
	#    + "State Toggle" - Toggles the state of @c Target each time it trigger() is called. See StateToggleTrigger().
	#    + "Area Change" - Changes the current area. See AreaChangeTrigger().
	#    + "SBSC" - Changes the state of an object based on the states of other objects in this area. See SBSCTrigger().
	#    + "TBSC" - Changes the state of an object after an amount of time has passed. See TBSCTrigger().
	#    + "Battle" - Starts a battle.
	#    + "Item" - Gives the player an item.
	#
	#  @endparblock
	#  @param AutoReset Determines whether or not this trigger must be manually reset with a call to reset().
	#  @param Active Determines whether this trigger can be triggered.
	#
	#  @todo
	#  @parblock
	#    Effects:
	#    + "Cutscene"
	#  @endparblock

	def __init__(self,Type,Area,Id,Effect,AutoReset=False,Active=True):
		self.cat = Type		#Category
		self.area = Area
		self.ID = Id
		self.effect = Effect
		self.triggered = False
		self.autoReset = AutoReset
		self.active = Active

	## Resets the current trigger.
	#
	#  Only needed if @c AutoReset is set to @c False.
	def reset(self):
		self.triggered = False

	## Returns the type of this trigger.
	def getType(self):
		return self.cat

	## Returns the area in which this trigger can be activated.
	def getArea(self):
		return self.area

	## Returns the effect of this trigger.
	def getEffect(self):
		return self.effect

	## Returns whether or not this trigger auto resets.
	def getAutoReset(self):
		return self.autoReset

	## Returns this trigger's ID.
	def getID(self):
		return self.ID

	## Checks if this trigger has been triggered and if it is active.
	#
	#  Returns True if trigger can be triggered.
	def triggerCheck(self):
		if not self.autoReset:
			if self.triggered:
				return False
		if not self.active:
			return False
		return True

	## Activates this trigger.
	#
	#  This trigger is just the base class, it should be overwritten by any subclasses for custom triggering code.
	#  Prints out the trigger type by default.
	#  @param triggerer The actor that caused the trigger to activate.
	#  @param objects A list of all objects and actors in the current area.
	def trigger(self,triggerer,objects):
		if self.triggerCheck():
			errors.info(self.cat+" Triggered")
			self.triggered = True


## State Set %Trigger
#
#  This trigger sets the state of an object when activated.
class StateSetTrigger(Trigger):
	## Constructor.
	#
	#  @param Type The triggering method. See @c Type in Trigger.
	#  @param Area The area that this trigger can be activated from.
	#  @param Target The target whose state will be set.
	#  @param NewState The new state to set the target's state to.
	#  @param AutoReset Determines whether or not this trigger must be manually reset with a call to reset().
	def __init__(self,Type,Area,Id,Target,NewState,AutoReset=True,Active=True):
		Trigger.__init__(self,Type,Area,Id,"State Set",AutoReset,Active)
		self.target = Target
		self.newState = NewState

	## Returns the target of this trigger.
	def getTarget(self):
		return self.target

	## Returns the state that @c Target will be set to for this trigger.
	def getNewState(self):
		return self.newState

	## Activates this trigger.
	#
	#  This changes the state of @c Target to @c NewState
	#  @param triggerer The actor that caused the trigger to activate.
	#  @param objects A list of all objects and actors in the current area.
	def trigger(self,triggerer,objects):
		if self.triggerCheck():
			for Object in objects:
				if Object.getID()==self.target:
					Object.setState(self.newState)
					errors.debug(self.getID()+" triggered.")
					self.triggered = True

## State Toggle %Trigger
#
#  This trigger toggles the state of an object between @c PrimaryState and @c SecondaryState.
class StateToggleTrigger(Trigger):
	## Constructor.
	#
	#  @param Type The triggering method. See @c Type in Trigger.
	#  @param Area The area that this trigger can be activated from.
	#  @param Target The target whose state will be toggled.
	#  @param PrimaryState The default state that will be toggled to.
	#  @param SecondaryState The secondary state.
	#  @param AutoReset Determines whether or not this trigger must be manually reset with a call to reset().
	def __init__(self,Type,Area,Id,Target,PrimaryState,SecondaryState,AutoReset=True,Active=True):
		Trigger.__init__(self,Type,Area,Id,"State Toggle",AutoReset,Active)
		self.target = Target
		self.primaryState = PrimaryState
		self.secondaryState = SecondaryState

	## Activates this trigger.
	#
	#  This toggles the state of @c Target between @c PrimaryState and @c SecondaryState.
	#
	#  The primary or default state will be toggled to if @c Target 's state is anything other than @c PrimaryState.
	#
	#  The secondary state will be toggled to if triggered while @c Target is in the @c PrimaryState.
	#  @param triggerer The actor that caused the trigger to activate.
	#  @param objects A list of all objects and actors in the current area.
	def trigger(self,triggerer,objects):
		if self.triggerCheck():
			for Object in objects:
				if Object.getID()==self.target:
					if Object.getState()==self.primaryState:
						Object.setState(self.secondaryState)
					else:
						Object.setState(self.primaryState)
					errors.debug(self.getID()+" triggered.")
					self.triggered = True

## Area Change %Trigger
#
#  This trigger changes the current area that the player is in.
class AreaChangeTrigger(Trigger):
	## Constructor.
	#
	#  @param Type The triggering method. See @c Type in Trigger.
	#  @param Area The area that this trigger can be activated from.
	#  @param NewArea The name of the new area.
	#  @param NewAreaXML The path to the XML containing the data for the new area.
	#  @param PlayerPos Where the player should start in the area.
	def __init__(self,Type,Area,Id,NewArea,NewAreaXML,PlayerPos,Active=True):
		Trigger.__init__(self,Type,Area,Id,"Area Change",True,Active)
		self.newArea = NewArea
		self.newAreaXML = NewAreaXML
		self.playerPos = PlayerPos

	## Returns the name of the new area.
	def getNewArea(self):
		return self.newArea

	## Returns the path to the XML describing the new area.
	def getNewAreaXML(self):
		return self.newAreaXML

	## Returns the position the player should start at.
	def getPlayerPos(self):
		return self.playerPos

## State Based State Change (SBSC) %Trigger
#
#  This trigger changes the state of a target based on the state of other objects in the current area.
class SBSCTrigger(Trigger):
	## Constructor.
	#
	#  @param NeededStates A list of actor ids which will be
	#  @param Target The target whose state will be set.
	#  @param NewState The new state to set the target's state to.
	#  @param AutoReset Determines whether or not this trigger must be manually reset with a call to reset().
	def __init__(self,NeededStates,State,Id,Target,NewState,AutoReset=False,Active=True):
		Trigger.__init__(self,"Other",None,Id,"SBSC",AutoReset,Active)
		self.neededStates = NeededStates
		self.state = State
		self.target = Target
		self.newState = NewState

	def getNeededStates(self):
		return self.neededStates

	def getState(self):
		return self.state

	## Activates this trigger.
	#
	#  This sets the state of @c Target when all objects in @c NeededStates in the @c State state.
	#  @param triggerer The actor that caused the trigger to activate.
	#  @param objects A list of all objects and actors in the current area.
	def trigger(self,triggerer,objects):
		if self.triggerCheck():
			for Object in objects:
				if Object.getID()==self.target:
					Object.setState(self.newState)
					errors.debug(self.getID()+" triggered.")
					self.triggered = True

## Time Based State Change (TBSC) %Trigger
#
#  This trigger changes the state of a target after an amount of time in seconds has passed.
class TBSCTrigger(Trigger):		#Time Based State Change (TBSC)
	## Constructor.
	#
	#  @param Type The triggering method. See @c Type in Trigger.
	#  @param Time The amount of time before @c Target 's state is changed, in seconds.
	#  @param Area The area that this trigger can be activated from.
	#  @param Target The target whose state will be set.
	#  @param NewState The new state to set the target's state to.
	#  @param AutoReset Determines whether or not this trigger must be manually reset with a call to reset().
	def __init__(self,Type,Time,Area,Id,Target,NewState,AutoReset=True,Active=True):
		Trigger.__init__(self,Type,Area,Id,"TBSC",AutoReset,Active=True)
		self.time = Time
		self.target = Target
		self.newState = NewState
		self.timeLeft = Time

	## Updates the timer.
	#
	#  Updates the timer and eventually causes the state change.
	#  @param tick time since last call, in seconds.
	#  @param objectsA list of all objects and actors in the current area.
	def update(self,tick,objects):
		if self.triggered:
			self.timeLeft -= tick
			if self.timeLeft<=0:
				for Object in objects:
					if Object.getID()==self.target:
						Object.setState(self.newState)
						if self.autoReset:
							self.reset()

	## Activates this trigger.
	#
	#  Starts the timer until the state of @c Target is changed..
	#  @param triggerer The actor that caused the trigger to activate.
	#  @param objects A list of all objects and actors in the current area.
	def trigger(self,triggerer,objects):
		if self.triggerCheck():
			self.timeLeft = self.time
			errors.debug(self.getID()+" triggered.")
			self.triggered = True

## Battle %Trigger
#
#  This trigger causes a battle to happen
class BattleTrigger(Trigger):
	## Constructor.
	#
	#  @param Type The triggering method. See @c Type in Trigger.
	#  @param Time The amount of time before @c Target 's state is changed, in seconds.
	#  @param Area The area that this trigger can be activated from.
	#  @param Enemies A list of strings with name of Enemies to be fought (i.e. GreenSlime), can be left blank if using @c Random=True.
	#  @param BG Which background image should be used in the battle.
	#  @param BGFar Set to true if there is a second background image that should be displayed far away.
	#  @param Random Whether or not the enemies should be chosen randomly.
	#  @param AutoReset Determines whether or not this trigger must be manually reset with a call to reset().
	def __init__(self,Type,Area,Id,Enemies,BG,BGFar=False,Random=False,AutoReset=False,Active=True):
		Trigger.__init__(self,Type,Area,Id,"Battle",AutoReset,Active)
		self.bg = BG
		self.bgFar = BGFar
		self.enemies = Enemies
		self.random = Random

	## Returns the background.
	def getBG(self):
		return self.bg

	## Returns whether or not there is a far background.
	def getBGFar(self):
		return self.bgFar

	## Returns the enemies to be fought.
	def getEnemies(self):
		return self.enemies

	## Returns whether or not the enemies should be randomized.
	def getRandom(self):
		return self.random

	## Activates this trigger.
	def trigger(self):
		if self.triggerCheck():
			self.triggered = True
			errors.debug(self.getID()+" triggered.")
			return False
		else:
			return True

## %Item %Trigger
#
#  Gives the player an item.
#
#  @todo Add ability to give random item?
class ItemTrigger(Trigger):
	def __init__(self,Type,Area,Id,Item,AutoReset=False,Active=True):
		Trigger.__init__(self,Type,Area,Id,"Item",AutoReset,Active)
		self.item = Item

	## Returns the item this trigger gives the player.
	def getItem(self):
		return self.item

	## Activates this trigger.
	def trigger(self):
		if self.triggerCheck():
			self.triggered = True
			errors.debug(self.getID()+" triggered.")
			return False
		else:
			return True

## %Quest %Trigger
#
#  Completes an objective for a quest.
class QuestCompleteTrigger(Trigger):
	def __init__(self,Type,Area,Id,QuestXML,Quest,Objective,AutoReset=False,Active=True):
		Trigger.__init__(self,Type,Area,Id,"Quest Complete",AutoReset,Active)
		self.questXML = QuestXML
		self.quest = Quest
		self.objective = Objective

	## Returns the path to the XML containing the quest.
	def getQuestXML(self):
		return self.questXML

	## Returns the quest the objective is in that this trigger completes..
	def getQuest(self):
		return self.quest

	## Returns the objective this trigger completes.
	def getObjective(self):
		return self.objective

	## Activates this trigger.
	def trigger(self):
		if self.triggerCheck():
			self.triggered = True
			errors.debug(self.getID()+" triggered.")
			return False
		else:
			return True

#class Effect(object):
