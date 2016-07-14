import pygame
from pygame.locals import *

from battle.engine import BattleObject
from graphics.animation import Animation, AnimationFrame
#from graphics import BattleGraphicObject, Animation, AnimationFrame
from graphics.battle import BattleGraphicObject
from ai import FeebleAI
import config

## The enemy base class.
class Enemy(BattleObject):

	## Constructor
	#  @param level This actor's level.
	#  @param drops A list of tuples containing items that can be dropped on death and the probability of this.
	#  @param baseExp Helps determine how much experience will be gained from defeated this enemy.
	#  @param baseGold Helps determine how much gold will be earned from defeated this enemy.
	#
	#  @note One enemy has the potential to drop all of its drops. Tuple Format: (items.Item,dropChance), where dropChance is a number between 0 and 1.
	def __init__(self,level,drops,baseExp,baseGold):
		self.level = level
		self.drops = drops
		self.baseExp = baseExp
		self.baseGold = baseGold
		self.statOffsets = {"HpM":0,"MpM":0,"Atk":0,"Def":0,"Spd":0,"Vit":0,"Mag":0,"Res":0,"Con":0,"Mnd":0}

	## Calculates how much experience the player should get from defeating this enemy.
	#
	#  exp = level*baseExp
	def calcExp(self):
		return self.level*self.baseExp

	## Calculates how much gold the player should get from defeating this enemy.
	#
	#  gold = level*baseGold
	def calcGold(self):
		return self.level*self.baseGold

	## Returns the items this enemy can drop.
	def getDrops(self):
		return self.drops

## An object that contains a slime.
#
#  Usually opting for the already colored slimes (e.g. GreenSlime) is better as the level parser will know what to do with it.
class Slime(Enemy):

	## Constructor.
	#  @param level The slime's level, which defines how strong it is.
	#  @param color What RGB color the slime is. No other effect at this time.
	#  @param pos X position of the slime
	def __init__(self,level,color,drops,pos):
		Enemy.__init__(self,level,drops,1,2)
		self.color = color

		self.hitBox = [pygame.rect.Rect([15,30,50,30]),pygame.rect.Rect([15,30,50,30])]
		self.atkBox = [pygame.rect.Rect([0,30,58,30]),pygame.rect.Rect([40,30,58,30])]
		self.attacking = False

		self.name = "Slime"
		self.ai = FeebleAI(55,150)

		animations = self.genAnim()
		self.graphicObject = BattleGraphicObject(animations,[pos,150],2*level,weapon=None,state="Idle")

		self.genStats()

		self.time=0.0
		self.state="Idle"

		self.x=float(pos)
		self.y=0.0
		self.velX = 0
		self.velY = 0
		self.direction=1

	## Makes the slime attack.
	def attack(self):
		if self.getState()=="Idle" or self.getState()=="Run":
			if self.getTime()<=0:
				self.attacking=True
				self.setState("Attack")
				self.setTime(self.weaponDelay[0]+self.weaponRecovery)

	## Generates Stats
	def genStats(self):
		self.weaponReaction = 0
		self.weaponChain = 1
		self.weaponRecovery = .25
		self.weaponDelay = [.50]

		self.HpM=5*self.level
		self.Hp=5*self.level
		self.MpM=0
		self.Mp=0
		self.Status=0b0	#0b0=Normal, 0b1=Poison, 0b10=Paralyze, 0b100=Frozen, 0b1000=Burn

		#Physical Stats
		self.Atk=int(1*self.level)	#Attack
		self.Def=int(.25*self.level)	#Defense
		self.Spd=2*self.level	#Speed
		self.Vit=2*self.level	#Vitality

		#Magical Stats
		self.Mag=0		#Magic
		self.Res=0		#Resistance
		self.Con=0		#Concentration
		self.Mnd=0		#Mind

	## Generate animations.
	def genAnim(self):
		animations = {"Idle":[Animation(None,None,"IdleW"),Animation(None,None,"IdleE")],"Run":[Animation(None,None,"RunW"),Animation(None,None,"RunE")],"Attack":[Animation(None,None,"AttackW"),Animation(None,None,"AttackE")],"Death":[Animation(None,None,"DeathW"),Animation(None,None,"DeathE")],"Dead":[Animation(None,None,"DeadW"),Animation(None,None,"DeadE")]}

		#Idle:
		temp = pygame.image.load(config.AssetPath+"Battle/Enemies/Gelatinous/Slime/Idle1.png").convert_alpha()
		temp.fill(self.color,special_flags=BLEND_MULT)
		animations["Idle"][1].addFrame(AnimationFrame(temp,.5,None,0))

		#Run:
		for i in range(1,7):
			temp = pygame.image.load(config.AssetPath+"Battle/Enemies/Gelatinous/Slime/Walk"+str(i)+".png").convert_alpha()
			temp.fill(self.color,special_flags=BLEND_MULT)
			animations["Run"][1].addFrame(AnimationFrame(temp,.17,None,i-1))

		#Attack:
		for i in range(1,3):
			temp = pygame.image.load(config.AssetPath+"Battle/Enemies/Gelatinous/Slime/Attack"+str(i)+".png").convert_alpha()
			temp.fill(self.color,special_flags=BLEND_MULT)
			animations["Attack"][1].addFrame(AnimationFrame(temp,.17,None,i-1))

		#Death:
		for i in range(1,7):
			temp = pygame.image.load(config.AssetPath+"Battle/Enemies/Gelatinous/Slime/Death"+str(i)+".png").convert_alpha()
			temp.fill(self.color,special_flags=BLEND_MULT)
			animations["Death"][1].addFrame(AnimationFrame(temp,.1,None,i-1))
		temp = pygame.image.load(config.AssetPath+"Battle/Enemies/Gelatinous/Slime/Dead.png").convert_alpha()
		temp.fill(self.color,special_flags=BLEND_MULT)
		animations["Dead"][1].addFrame(AnimationFrame(temp,.17,None,i-1))


		##Create Mirroring
		#Idle
		temp = animations["Idle"][1].getFrames()
		i=0
		for frame in temp:
			animations["Idle"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
			i+=1
		#Run
		temp = animations["Run"][1].getFrames()
		i=0
		for frame in temp:
			animations["Run"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
			i+=1
		#Attack
		temp = animations["Attack"][1].getFrames()
		j = 0
		for frame in temp:
			animations["Attack"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,j))
			j+=1

		#Death
		animations["Death"][0]=animations["Death"][1]
		animations["Dead"][0]=animations["Dead"][1]

		##And linking...
		animations["Attack"][0].setNextAnimation(animations["Idle"][0])
		animations["Attack"][1].setNextAnimation(animations["Idle"][1])
		animations["Death"][0].setNextAnimation(animations["Dead"][0])
		animations["Death"][1].setNextAnimation(animations["Dead"][1])
		temp = Animation(None,None,"Remove")
		temp.addFrame(AnimationFrame(pygame.surface.Surface((1,1)),.5,None,1))
		animations["Death"][0].setNextAnimation(temp)
		animations["Death"][1].setNextAnimation(temp)

		return animations

## Green variant of Slime.
class GreenSlime(Slime):

	## Constructor
	#  @param level The slime's level, which defines how strong it is.
	#  @param pos X position of the slime
	def __init__(self,level,pos):
		Slime.__init__(self,level,[0,255,0],[("GreenSlimeball",.5),],pos)
		self.name = "Green Slime"


## Green variant of Slime.
class RedSlime(Slime):

	## Constructor
	#  @param level The slime's level, which defines how strong it is.
	#  @param pos X position of the slime
	def __init__(self,level,pos):
		Slime.__init__(self,level,[255,255,0],pos)
		self.name = "Green Slime"

	## Generates stats
	def genStats(self):
		Slime.genStats(self)
		self.HpM=3*self.level
		self.Hp=3*self.level
		self.Atk=int(2*self.level)	#Attack
