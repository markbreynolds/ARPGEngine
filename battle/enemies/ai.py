import random

## Base class for all %AI.
class AI(object):
	
	## Constructor
	#  @param senseRange Defines the area in which the %AI is aware of other entities
	#  @param reactionTime How long it takes before the %AI updates its state.
	#  @param intState Starting internal state the %AI is in.
	#  @param extState Starting external state the %AI is in.
	def __init__(self,senseRange,reactionTime,intState="Idle",extState="Idle"):
		self.intState = intState
		self.extState = extState
		self.senseRange = senseRange
		self.reactionTime = reactionTime
		self.time = 0
		self.target = None
	
	## Returns the entity the %AI is currently targeting.
	def getTarget(self):
		return self.target
	
	## Returns the %AI's external state
	def getExtState(self):
		return self.extState
	
	## Returns the %AI's internal state
	def getIntState(self):
		return self.intState
	
	## Triggers an internal state change.
	#  @param state The new state the %AI will assume.
	def trigger(self,state):
		self.intState = state
	
	## Reacts to sensed objects and changes internal state.
	#
	#  This should be overridden by each different %AI.
	#  @param sensedObjects A list of the objects returned by sense().
	#  @param xPos The centered X position of the parent of this %AI.
	def react(self,sensedObjects,xPos):
		pass
	
	## Applies internal state externally to parent.
	#
	#  This should be overridden by each different %AI.
	#  @param parent The parent object to this %AI.
	def act(self,parent):
		pass
	
	## Returns a list of objects that the %AI can sense
	#
	#  Should not be overridden without good reason. This way all %AIs sense things the same way.
	#  @param objects All objects in the current battle.
	#  @param xPos The centered X position of the parent of this %AI.
	def sense(self,objects,xPos):
		ret = []
		for object in objects:
			if abs(object.getCX()-xPos) <= self.senseRange:
				ret.append(object)
		return ret
	
	## Update the %AI's internals
	#
	#  Should not be overriden without good reason. This way all %AIs work the same general way.
	#  @param objects All objects in the current battle.
	#  @param parent The parent entity of this %AI.
	#  @param tick Time between frames in seconds.
	def update(self,objects,parent,tick):
		if self.time <= 0:
			self.react(self.sense(objects,parent.getCX()),parent.getCX())
			self.act(parent)
			self.time = self.reactionTime
		else:
			self.time -= tick

## Feeble %AI
#
#  A weak %AI that does not try very hard to attack the player.
class FeebleAI(AI):
	
	## Constructor
	#  @param atkRange From how far away the entity can attack.
	#  @param senseRange Defines the area in which the %AI is aware of other entities
	#  @param reactionTime How long it takes before the %AI updates its state.
	def __init__(self,atkRange,senseRange,reactionTime=1.0):
		AI.__init__(self,senseRange,reactionTime)
		self.atkRange = atkRange
	
	## See AI.react()
	def react(self,sensedObjects,xPos):
		if self.intState == "Idle":
			for obj in sensedObjects:
				if obj.isAlly():
					self.target = obj
					self.intState = "Attack"
					return
			if self.extState == "Idle":
				if random.random()<.50:		#50% chance to start moving
					self.extState = "Run"
			elif self.extState == "Run":
				if random.random()<.50:		#50% chance to stop moving
					self.extState = "Idle"
		elif self.intState == "Attack":
			if self.target in sensedObjects:
				if abs(self.target.getCX()-xPos)<self.atkRange:
					self.extState = "Attack"
				else:
					self.extState = "Run"
			else:
				self.intState = "Idle"
				self.extState = "Idle"
	
	## See AI.act()
	def act(self,parent):
		if self.intState=="Idle":
			if random.random()<.001:					#.1% chance
				parent.setDirection(random.randint(0,1))
			if parent.getState() != self.extState:
				parent.setState(self.extState)
				
		elif self.intState=="Attack":
			if self.target.getCX()-parent.getCX()<0:
				parent.setDirection(0)
			else:
				parent.setDirection(1)
			
			if self.extState=="Attack":
				parent.attack()
			else:
				if parent.getState() != self.extState:
					parent.setState(self.extState)

## Wanderer %AI
#
#  A weak %AI that does not try very hard to attack enemies.
class WandererAI(AI):
	
	## Constructor
	#  @param atkRange From how far away the entity can attack.
	#  @param senseRange Defines the area in which the %AI is aware of other entities
	#  @param reactionTime How long it takes before the %AI updates its state.
	def __init__(self,atkRange,senseRange,reactionTime=0.5):
		AI.__init__(self,senseRange,reactionTime)
		self.atkRange = atkRange
	
	## See AI.react()
	def react(self,sensedObjects,xPos):
		if self.intState == "Idle":
			for obj in sensedObjects:
				if obj.isEnemy():
					self.target = obj
					self.intState = "Attack"
					return
			if self.extState == "Idle":
				if random.random()<.50:		#50% chance to start moving
					self.extState = "Run"
			elif self.extState == "Run":
				if random.random()<.50:		#50% chance to stop moving
					self.extState = "Idle"
		elif self.intState == "Attack":
			if self.target in sensedObjects:
				if abs(self.target.getCX()-xPos)<self.atkRange:
					self.extState = "Attack"
				else:
					self.extState = "Run"
			else:
				self.intState = "Idle"
				self.extState = "Idle"
	
	## See AI.act()
	def act(self,parent):
		if self.intState=="Idle":
			if random.random()<.1:					#10% chance
				parent.setDirection(random.randint(0,1))
			if parent.getState() != self.extState:
				parent.setState(self.extState)
				
		elif self.intState=="Attack":
			if self.target.getCX()-parent.getCX()<0:
				parent.setDirection(0)
			else:
				parent.setDirection(1)
			
			if self.extState=="Attack":
				parent.attack()
			else:
				if parent.getState() != self.extState:
					parent.setState(self.extState)
