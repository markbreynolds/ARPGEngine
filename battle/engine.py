import random

import pygame

import config
from graphics.animation import Animation, AnimationFrame
## The Battle Engine
#
#  A new battle engine is created for each battle.
class BattleEngine(object):

	## Constructor
	#
	#  @param GraphicsEngine A reference to a graphics.BattleGraphicsEngine.
	def __init__(self,GraphicsEngine):
		self.playerParty=[]
		self.enemyParty=[]
		self.projectiles=[]
		self.loot = []
		self.exp = 0
		self.gold = 0
		self.graphicsEngine=GraphicsEngine

	## Adds a BattleObject to the allies team.
	def addAlly(self,ally):
		ally.setTeam(1)
		self.playerParty.append(ally)
		self.graphicsEngine.addAlly(ally.getGraphicObject())

	## Adds a BattleObject to the enemies team.
	def addEnemy(self,enemy):
		enemy.setTeam(-1)
		self.enemyParty.append(enemy)
		self.graphicsEngine.addEnemy(enemy.getGraphicObject())

	## Adds a projectile to the projectile list.
	def addProjectile(self,projectile):
		self.projectiles.append(projectile)
		self.graphicsEngine.addProjectile(projectile.getGraphicObject())

	## Returns how much experience the player earned.
	def getExp(self):
		return self.exp

	## Returns the items the player got.
	def getLoot(self):
		return self.loot

	## Returns how much gold the player earned.
	def getGold(self):
		return self.gold

	## Returns the player's party
	def getPlayerParty(self):
		return self.playerParty

	## Returns the graphics.BattleGraphicsEngine.
	def getGraphicsEngine(self):
		return self.graphicsEngine

	## Updates the battle engine.
	def update(self,tick):
		for ally in self.playerParty:
			ally.update(tick)
			if ally.getHP()<=0:
				if ally.getState() == "Death":
						pass
				else:
					ally.setState("Death")
				if ally.isPlayer():
					print "Game Over"
				self.playerParty.remove(ally)
				#ally.setState("Dead")

			ally.updateAI(tick,self.playerParty+self.enemyParty)
			if ally.isAttacking():
				for enemy in self.enemyParty:
					if enemy.getHitBox().colliderect(ally.getAtkBox()):
						self.graphicsEngine.addDmgVal(enemy.takeDamage(ally.getAtk()),enemy.getGraphicObject().getPos(),(255,255,255))
						ally.setAttacking(False)
			if ally.getProjectile() != None:
				self.addProjectile(ally.getProjectile())
				ally.resetProjectile()

		for enemy in self.enemyParty:
			enemy.update(tick)
			if enemy.getHP()<=0:
				if enemy.getState() == "Death":
					if enemy.getGraphicObject().getCurrAnimName()=="Remove":
						self.enemyParty.remove(enemy)
						self.graphicsEngine.removeEnemy(enemy.getGraphicObject())
						self.exp+=enemy.calcExp()
						self.gold+=enemy.calcGold()
						for item in enemy.getDrops():
							if random.random()<item[1]:
								self.loot.append(item[0])
					else:
						pass
				else:
					enemy.setState("Death")
			else:
				enemy.updateAI(tick,self.playerParty+self.enemyParty)
				if enemy.isAttacking():
					for ally in self.playerParty:
						if ally.getHitBox().colliderect(enemy.getAtkBox()):
							self.graphicsEngine.addDmgVal(ally.takeDamage(enemy.getAtk()),ally.getGraphicObject().getPos(),(255,0,0))
							enemy.setAttacking(False)

		for projectile in self.projectiles:
			removed = False
			if projectile.getParent().isAlly():
				for enemy in self.enemyParty:
					if enemy.getHitBox().colliderect(projectile.getAtkBox()):
						if not enemy in projectile.getHitList():
							self.graphicsEngine.addDmgVal(enemy.takeDamage(projectile.getAtk()),enemy.getGraphicObject().getPos(),(255,255,255))

							if projectile.getPiercing():
								projectile.addHit(enemy)
							else:
								if not removed:
									self.projectiles.remove(projectile)
									self.graphicsEngine.removeProjectile(projectile.getGraphicObject())
									removed = True

			elif projectile.getParent().isEnemy():
				for ally in self.playerParty:
					if ally.getHitBox().colliderect(projectile.getAtkBox()):
						if not ally in projectile.getHitList():
							self.graphicsEngine.addDmgVal(ally.takeDamage(projectile.getAtk()),ally.getGraphicObject().getPos(),(255,0,0))
							if projectile.getPiercing():
								projectile.addHit(ally)
							else:
								self.projectiles.remove(projectile)
								self.graphicsEngine.removeProjectile(projectile.getGraphicObject())
								removed = True
			if not removed and projectile.update(tick):
				self.projectiles.remove(projectile)
				self.graphicsEngine.removeProjectile(projectile.getGraphicObject())

		self.graphicsEngine.update(tick)

		return len(self.enemyParty)==0

## An actor involved in a battle.
#
#  This class contains all of the data and functions for battle actors.
#  This class is subclass by all enemies and is used directly for the player.
class BattleObject(object):

	## Constructor
	#
	#  @param graphicObject The graphics.BattleGraphicObject associated with this actor.
	#  @param hitBox A pygame rect that describes the area in which this actor is susceptible to being attacked.
	#  @param pos The X postion of this actor.
	#  @param name This actor's name.
	#  @param weapon The weapon this actor has equipped (if none then @c None).
	#  @param level What level the actor is.
	#  @param exp How much experience the actor has (how close to the next level).
	#  @param HP How many health points this actor has. (Health Points)
	#  @param MP How many mana points this actor has. (Mana Points)
	#  @param Atk How much attack power this actor has. (Attack)
	#  @param Def How much defense this actor has. (Defense)
	#  @param Spd How fast this character can move. (Speed)
	#  @param Vit How much vitality this character has. (Vitality)
	#  @param Mag How strong this character's magic is. (Magic)
	#  @param Res How resistant this character is to magic. (Resistance)
	#  @param Con How easily this character's spells can be broken (stopped mid cast). (Concentration)
	#  @param Mnd How strong this character's mind is. (Mind)
	def __init__(self,graphicObject,hitBox,pos,name,weapon,level=0,exp=0,HP=1,MP=1,Atk=0,Def=0,Spd=20,Vit=0,Mag=0,Res=0,Con=0,Mnd=0):
		self.graphicObject=graphicObject
		self.hitBox = hitBox

		self.name=name
		self.level=level
		self.exp=exp		#Next=level*10 + (level-1)^2*10
							#level 1: 10exp, level 2: 30 exp, level 3: 70, level 4: 130

#		if weapon != None:
#			if weapon.getStyle().getType() == "Combo":
#				delay = weapon.getStyle().getFrameDelay()
#				self.weaponReaction = weapon.getStyle().getReactionTime()
#				self.weaponChain = weapon.getStyle().getChain()
#				self.weaponRecovery = weapon.getRecoveryTime()
#				self.atkBox = weapon.getAtkBox()
#				self.weaponStyle =
#		else:
#			delay = [[.15,.25],[.15,.15,.25],[.15,.25]]
#			self.weaponReaction = .20
#			self.weaponChain = 3
#			self.weaponRecovery = .25
#			self.atkBox = [pygame.rect.Rect([4,7,25,61]),pygame.rect.Rect([23,7,25,60])]
#		self.weaponDelay = []
#		for item in delay:
#			self.weaponDelay.append(sum(item))

		self.HpM=HP
		self.Hp=HP
		self.MpM=MP
		self.Mp=MP
		self.status=0b0	#0b0=Normal, 0b1=Poison, 0b10=Paralyze, 0b100=Frozen, 0b1000=Burn

		#Physical Stats
		self.Atk=Atk	#Attack
		self.Def=Def	#Defense
		self.Spd=Spd	#Speed
		self.Vit=Vit	#Vitality

		#Magical Stats
		self.Mag=Mag	#Magic
		self.Res=Res	#Resistance
		self.Con=Con	#Concentration
		self.Mnd=Mnd	#Mind

		self.statOffsets = {"HpM":0,"MpM":0,"Atk":0,"Def":0,"Spd":0,"Vit":0,"Mag":0,"Res":0,"Con":0,"Mnd":0}

		self.time=0.0
		self.state="Idle"

		self.x=float(pos)
		self.y=0.0
		self.velX = 0.0
		self.velY = 0.0
		self.direction=1

		self.team = 0
		self.playerStatus = False
		self.attacking = False
		self.projectile = None

		self.abilities=[]
		self.job=None
		self.ai = None

	## Gives this actor experience.
	def addExp(self,amt):
		self.exp+=amt

	## Returns if this actor is the player.
	def isPlayer(self):
		return self.playerStatus

	## Sets this actors x position.
	def setX(self,x):
		self.x = x
		self.graphicObject.setX(x)

	## Damages this actor's health.
	def takeDamage(self,dmg):
		if self.getDirection() == 1:
			self.velX = -max(0,(dmg-self.getDef())/(self.getHPM()))*100
		else:
			self.velX =  max(0,(dmg-self.getDef())/(self.getHPM()))*100
		self.Hp-=max(dmg-self.getDef(),0)
		return max(dmg-self.getDef(),0)

	## Uses a skill
	def useSkill(self,skill):
		self.state = "Skill"
		self.Mp-=skill.getCost()
		self.getGraphicObject().setState(skill.getState())
		self.setTime(skill.getCooldown())

	## Sets whether or not this actor is attacking
	def setAttacking(self,val):
		self.attacking=val

	## Returns whether or not this actor is attacking.
	def isAttacking(self):
		return self.attacking

	## Sets whether this actor is an ally or an enemy.
	#  1 = Ally
	#  0 = Neutral
	#  -1 = Enemy
	def setTeam(self,team):
		self.team=team

	## Returns whether this actor is an ally.
	def isAlly(self):
		return self.team == 1

	## Returns whether this actor is an enemy.
	def isEnemy(self):
		return self.team == -1

	## Returns whether this actor is neither an enemy or an ally.
	def isNeutral(self):
		if self.team == 0:
			return True
		return False

	## Returns this actor's name.
	def getName(self):
		return self.name

	## Returns this actor's attack power.
	def getAtk(self):
		return self.Atk+self.statOffsets["Atk"]

	## Returns this actor's defense.
	def getDef(self):
		return self.Def+self.statOffsets["Def"]

	## Returns this actor's speed.
	def getSpd(self):
		return self.Spd+self.statOffsets["Spd"]

	## Returns this actor's vitality.
	def getVit(self):
		return self.Vit+self.statOffsets["Vit"]

	## Returns this actor's magic strength.
	def getMag(self):
		return self.Mag+self.statOffsets["Mag"]

	## Returns this actor's magic resistance.
	def getRes(self):
		return self.Res+self.statOffsets["Res"]

	## Returns this actor's concentration.
	def getCon(self):
		return self.Con+self.statOffsets["Con"]

	## Returns this actor's mind.
	def getMnd(self):
		return self.Mnd+self.statOffsets["Mnd"]

	## Returns this actor's natural attack power.
	def getAtkN(self):
		return self.Atk

	## Returns this actor's natural defense.
	def getDefN(self):
		return self.Def

	## Returns this actor's natural speed.
	def getSpdN(self):
		return self.Spd

	## Returns this actor's natural vitality.
	def getVitN(self):
		return self.Vit

	## Returns this actor's natural magic strength.
	def getMagN(self):
		return self.Mag

	## Returns this actor's natural magic resistance.
	def getResN(self):
		return self.Res

	## Returns this actor's natural concentration.
	def getConN(self):
		return self.Con

	## Returns this actor's natural mind.
	def getMndN(self):
		return self.Mnd

	## Returns this actor's maximum health.
	def getHPM(self):
		return self.HpM+self.statOffsets["HpM"]

	## Returns this actor's maximum health formatted prettily as a string.
	def getHPMS(self):
		HpM=self.HpM+self.statOffsets["HpM"]
		if HpM > 9999:
			return str(HpM/1000)+"K"
		return str(HpM)

	## Returns this actor's current health.
	def getHP(self):
		return self.Hp

	## Returns this actor's current health formatted prettily as a string.
	def getHPS(self):
		if self.Hp > 9999:
			return str(self.Hp/1000)+"K"
		return str(self.Hp)

	## Returns this actor's maximum mana power.
	def getMPM(self):
		return self.MpM+self.statOffsets["MpM"]

	## Returns this actor's maximum mana power formatted prettily as a string.
	def getMPMS(self):
		MpM=self.MpM+self.statOffsets["MpM"]
		if MpM > 9999:
			return str(MpM/1000)+"K"
		return str(MpM)

	## Returns this actor's current mana power.
	def getMP(self):
		return self.Mp

	## Returns this actor's current mana power formatted prettily as a string.
	def getMPS(self):
		if self.Mp > 9999:
			return str(self.Mp/1000)+"K"
		return str(self.Mp)

	## Returns this actor's status.
	def getStatus(self):
		return self.status

	## Returns this actor's current state.
	def getState(self):
		return self.state

	## Returns this actor's graphic object.
	def getGraphicObject(self):
		return self.graphicObject

	## Returns this actor's internal clock.
	def getTime(self):
		return self.time

	## Sets this actor's health.
	def setHP(self,HP):
		self.Hp = HP

	## Sets this actor's mana.
	def setMP(self,MP):
		self.Mp = MP

	## Sets this actor's internal clock.
	def setTime(self,time):
		self.time = time

	## Sets this actor's current state.
	def setState(self,state):
		self.state=state
		self.graphicObject.setState(state)

	## Sets this actor's direction.
	def setDirection(self,direction):
		self.direction=direction
		self.graphicObject.setDirection(direction)

	## Returns this actor's direction.
	def getDirection(self):
		return self.direction

	## Returns this actor's level.
	def getLevel(self):
		return self.level

	## Returns how much experience this actor has.
	def getExp(self):
		return self.exp

	## Returns how much experience this actor needs to reach the next level.
	def getExpNext(self):
		return self.level*10+((self.level-1)**2)*10

	## Returns this actor's hit box.
	def getHitBox(self):
		return self.hitBox[self.getDirection()].move(self.getGraphicObject().getX(),self.getGraphicObject().getY())

	## Returns this actor's attack box.
	def getAtkBox(self):
		return self.atkBox[self.getDirection()].move(self.getGraphicObject().getX(),self.getGraphicObject().getY())

	## Returns this actor's center x.
	def getCX(self):
		return self.x+(self.getGraphicObject().getWidth()/2)

	## Returns whether this actor is spawning a projectile.
	#
	#  @return Projectile object to spawned.
	def getProjectile(self):
		return self.projectile

	## Clears the current projectile.
	def resetProjectile(self):
		self.projectile = None

	## Internal logic for attacking.
	def attack(self):
		if self.weaponType == "Combo":
			if self.getState()=="Idle" or self.getState()=="Run":
				if self.getTime()<=0:
					self.attacking=True
					self.setState("Attack1")
					self.setTime(self.weaponDelay[0])
			elif self.getState().startswith("Attack"):
				i = int(self.getState().lstrip("Attack"))
				if i<self.weaponChain:
					if self.getTime()>=0 and self.getTime()<=self.weaponReaction:
						self.attacking=True
						self.setState("Attack"+str(i+1))
						self.setTime(self.weaponDelay[i])
					else:
						self.setState("Idle")
						self.setTime(self.weaponRecovery*2)
		elif self.weaponType == "Charge":
			if self.getState()=="Idle" or self.getState()=="Run":
				if self.getTime()<=0:
					self.setState("Attack")
					#self.setTime(self.weaponDelay[0])

	def release(self,graphicObject):
		if self.weaponType == "Charge":
			stage = int(self.graphicObject.getFrame())
			self.setState("Idle")
			if stage > self.weaponPreStages:
				scale = .5+(.5*(stage-(self.weaponPreStages+1))/(self.weaponStages-(self.weaponPreStages+1)))	# Calculate how strong the attack should be
				proj = dict(self.weaponProj)																#    based on how charged it was. Range: [.5-1]
				proj["parent"] = self
				proj["pos"] = [self.x,self.graphicObject.getY()+proj["pos"][1]]
				if self.direction == 1:
					proj["pos"][0] += self.graphicObject.getWidth()
				else:
					proj["direction"] = 0
				proj["damage"] = int(self.getAtk()*scale)		# Should this be trucated? Are decimal damages bad?
				proj["speed"] *= scale
				proj["dist"] *= scale
				img = pygame.image.load(config.AssetPath+proj["graphicObject"]).convert_alpha()
				animR = Animation(AnimationFrame(img,.5,None,"Idle"),None,"Idle")
				animL = Animation(AnimationFrame(pygame.transform.flip(img,True,False),.5,None,"Idle"),None,"Idle")
				proj["graphicObject"] = graphicObject({"Idle":[animL,animR]},proj["pos"],proj["speed"])
				self.projectile = Projectile(**proj)

	## Levels up this actor.
	def levelUp(self,HP=0,MP=0,Atk=0,Def=0,Spd=0,Vit=0,Mag=0,Res=0,Con=0,Mnd=0):
		self.exp -= self.getExpNext()
		self.level += 1;
		self.HpM += HP
		self.Hp  += HP
		self.MpM += MP
		self.Mp  += MP
		self.Atk += Atk
		self.Def += Def
		self.Spd += Spd
		self.Vit += Vit
		self.Mag += Mag
		self.Res += Res
		self.Con += Con
		self.Mnd += Mnd

	## Updates the currently equipped weapon.
	def updateWeapon(self,weapon,animations):
		if weapon != None:
			if weapon.getStyle().getType()=="Combo":
				delay = weapon.getStyle().getFrameDelay()
				self.weaponReaction = weapon.getStyle().getReactionTime()
				self.weaponChain = weapon.getStyle().getChain()
				self.weaponRecovery = weapon.getRecoveryTime()
				self.weaponType = "Combo"
				self.atkBox = weapon.getAtkBox()
			elif weapon.getStyle().getType()=="Charge":
				self.weaponType = "Charge"
				self.weaponRecovery = weapon.getRecoveryTime()
				self.weaponPreStages = weapon.getStyle().getPreStages()
				self.weaponStages = weapon.getStyle().getStages()
			self.weaponProj = weapon.getProjectile()
		else:
			delay = [[.15,.25],[.15,.15,.25],[.15,.25]]
			self.weaponReaction = .20
			self.weaponChain = 3
			self.weaponRecovery = .25
			self.weaponType = "Combo"
			self.atkBox = [pygame.rect.Rect([4,7,25,61]),pygame.rect.Rect([23,7,25,60])]
		if self.weaponType == "Combo":
			self.weaponDelay = []
			for item in delay:
				self.weaponDelay.append(sum(item))

		self.graphicObject.setWeapon(weapon)
		self.graphicObject.updateAnimations(animations)

	## Code for AI calls
	#  @param tick Time between frames, in seconds.
	#  @param objects All objects in the current battle.
	def updateAI(self,tick,objects):
		if self.ai != None:
			self.ai.update(objects,self,tick)

	## Updates this actor.
	def update(self,tick):
		if self.time > 0:
			self.time -= tick
		if self.state=="Run":
			if self.direction==0:
				if self.x>0:
					self.x-=self.Spd*10*tick
				else:
					self.x = 0
			else:
				if self.x+self.graphicObject.getWidth()<960:
					self.x+=self.Spd*10*tick
				else:
					self.x = 960-self.graphicObject.getWidth()
			self.graphicObject.setX(int(self.x))
		elif self.state.startswith("Attack"):
			if self.weaponType == "Combo":
				if self.time <= 0:
					self.setAttacking(False)
					self.setState("Idle")
					self.time = self.weaponRecovery
				if self.time >= self.weaponReaction:
					if self.direction==0:
						self.x-=self.Spd*1.5*tick
					else:
						self.x+=self.Spd*1.5*tick
					self.graphicObject.setX(int(self.x))
			elif self.weaponType == "Charge":
				#if self.time
				pass
		elif self.state == "Skill":
			if self.time<=0:
				self.setState("Idle")
		self.x+=self.velX*tick
		self.graphicObject.setX(int(self.x))
		if self.velX >= .05:
			self.velX += 100*tick*(-abs(self.velX)/self.velX)
		else:
			self.velX = 0

## An object that shoots out of an actor and deals damage.
class Projectile(object):

	## Constructor
	#
	#  @param graphicObject The graphics.BattleGraphicObject associated with this actor.
	#  @param atkBox A pygame rect that describes the area in which this projectile does damage.
	#  @param damage How much base damage this projectile does.
	#  @param pos The starting postion of this projectile.
	#  @param speed How fast the projectile will move in pixels/second.
	#  @param dist How far the projectile will go in pixels.
	#  @param parent Which actor shot this projectile.
	#  @param piercing Whether this projectile moves through enemys or stops once they have been hit.
	def __init__(self,graphicObject,atkbox,damage,pos,speed,dist,parent,direction=1,piercing=False):
		self.graphicObject = graphicObject
		self.atkbox = atkbox
		self.damage = damage
		self.x = pos[0]
		self.y = pos[1]
		self.speed = speed
		self.distMax = dist
		self.dist = 0
		self.parent = parent
		self.direction = direction
		self.piercing = piercing
		self.hitList = []

	## Returns the list of entities that have already been hit.
	def getHitList(self):
		return self.hitList

	## Adds @c hit to the list of entities that have already been hit.
	def addHit(self,hit):
		self.hitList.append(hit)

	## Returns a copy of this projectile.
	def getCopy(self):
		return Projectile(self.graphicObject.getCopy(),self.atkbox,self.damage,[self.x,self.y],self.speed,self.distMax,self.parent,self.direction,self.piercing)

	## Returns this objects graphic object.
	def getGraphicObject(self):
		return self.graphicObject

	## Returns this projectile's attack box.
	def getAtkBox(self):
		return self.atkbox[self.direction].move(self.getGraphicObject().getX(),self.getGraphicObject().getY())

	## Returns this projectile's parent.
	def getParent(self):
		return self.parent

	## Returns how much base damage this projectile does.
	def getAtk(self):
		return self.damage

	## Returns if this projectile can travel through enemies
	def getPiercing(self):
		return self.piercing

	## Sets this projectile's direction.
	def setDirection(self,dire):
		self.direction=dire
		self.graphicObject.setDirection(dire)

	## Sets this projectile's position
	def setPos(self,pos):
		self.x=pos[0]
		self.y=pos[1]
		self.graphicObject.setPos(pos)

	## Resets how far this projectile has travelled
	def resetDist(self):
		self.dist = 0

	## Sets the actor who shot this projectile.
	def setParent(self,parent):
		self.parent = parent

	def setDamage(self,dmg):
		self.damage = dmg

	## Updates this projectile.
	def update(self,tick):
		if self.direction == 1:
			self.x+=self.speed*tick
		else:
			self.x-=self.speed*tick
		self.dist+=self.speed*tick
		self.graphicObject.setX(int(self.x))
		if self.dist>=self.distMax:
			return True
