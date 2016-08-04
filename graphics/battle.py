import pygame
from pygame.locals import *

from animation import Animation, AnimationFrame, loadAnimation
import gui
import config

## Graphics Engine for battle portion of game.
#
#  No more than one instance of the battle graphics engine should be running at any given time.
#
#  Backgrounds can have from two to three component images to them, the ground, "close objects", and "far objects".
#  The first two are necessary and the third is optional. The naming convention for these is; baseNameG for the
#  ground, baseNameC for "close objects", and baseNameF for "far objects". The "far objects" image will move slower
#  than the "close objects" image to give a sense of depth.
class BattleGraphicsEngine(object):

	## Constructor.
	#  @param screen A reference to either a Pygame screen object or a scaledScreen.
	#  @param isScaled If @c screen is a scaledScreen, then should be @c True.
	#  @param bg Base name of the background images to be used.
	#  @param farBG Set to @c True if there is a "far objects" image.
	def __init__(self,screen,isScaled,bg,farBG=False):
		self.screen=screen
		self.isScaled=isScaled

		self.allies=[]
		self.enemies=[]
		self.projectiles=[]

		self.focus=None
		self.x=0
		self.y=0

		self.dmgVals = []
		self.hud = gui.BattleHUD([])

		self.bgG=pygame.image.load(config.AssetPath+bg+"G.png").convert()	#Ground
		self.bgC=pygame.image.load(config.AssetPath+bg+"C.png").convert_alpha()	#Close Objects
		if farBG:
			self.bgF=pygame.image.load(config.AssetPath+"Backgrounds/Battle/"+bg+"F.png").convert()	#Far Objects
		else:
			self.bgF=None

		self.compEffect=None
		self.compValue=[0,0,0]

		self.debugInfo = ""

	## Sets the debug text to be shown at the bottom of the screen.
	def setDebugInfo(self,info):
		self.debugInfo=info

	## Returns the Battle HUD.
	def getHud(self):
		return self.hud

	## Adds a damage value to be displayed on the screen.
	#
	#  The last number represents the age of the text
	#  @param val The number to displayed, assumed to be damage done.
	#  @param x,y Where to draw on the screen the damage value
	def addDmgVal(self,val,pos,color=[0,0,0]):
		for dmg in self.dmgVals:
			if abs(dmg[1][1]-pos[1])<=10 and abs(dmg[1][0]-pos[0])<=15:
				pos[0]+=20
		self.dmgVals.append([val,pos,color,0])

	## Returns the x component of the camera's position.
	def getX(self):
		return int(self.x)

	## Returns the y component of the camera's position.
	def getY(self):
		return int(self.y)

	## Sets the x component of the camera's position.
	def setX(self,x):
		if x>0:
			x=0
		elif x<-640:
			x=-640
		else:
			self.x = x

	## Sets the y component of the camera's position.
	def setY(self,y):
		self.y = y

	## Adds a character to the player's team.
	def addAlly(self,ally):
		self.allies.append(ally)

	## Adds a character to the enemies's team.
	def addEnemy(self,player):
		self.enemies.append(player)

	## Adds a projectile to the projectile list.
	def addProjectile(self,projectile):
		self.projectiles.append(projectile)

	## Sets what the camera will follow and focus on.
	def setFocus(self,focus):
		self.focus=focus

	## Moves the camera along the x axis by @c amt.
	def scrollX(self,amt):
		if self.x-amt>0:
			self.x=0
		elif self.x-amt<-640:
			self.x=-640
		else:
			self.x-=amt

	## Uses composite effects to create visual effects.
	#
	#  May not work?
	#
	#  @todo Add more effects
	def composite(self):
		if self.compEffect==None:
			return
		else:
			self.screen.fill(self.compValue,special_flags=self.compEffect)

	## Remove an actor from the enemies team.
	def removeEnemy(self,enemy):
		self.enemies.remove(enemy)

	## Remove an actor from the players team.
	def removeAlly(self,ally):
		self.allies.remove(ally)

	## Remove a projectile from the projectiles list.
	def removeProjectile(self,proj):
		self.projectiles.remove(proj)

	## Displays the victory screen.
	def victoryScreen(self,clock,Input,players,gold,exp,items):
		temp = 0
		curr = 0
		time = 1
		showing = True
		blink = 1
		bg = self.screen.copy()
		if len(items)==0:
			offset = 0
			x = 112
			width = 65
		elif len(items)==1:
			offset = -10
			x = 112
			width = 60
		else:
			offset=-((26*(len(items)-1))/2+12)
			x = 135+(offset)
			width = (26*(len(items)))+8
		if gold > 1000 and len(items)<=2:
			width+=5

		while showing:
			tick = clock.tick()/1000.0
			blink -= tick
			if blink <= 0:
				blink = 1
			self.screen.blit(bg,(0,0))
			self.screen.fill(config.ColorDark,(x-1,94,width+2,77))
			self.screen.fill(config.Color,(x,95,width,75))
			for inp in Input.getInput():
				if inp[0] == "Quit":
					pygame.quit()
					exit()
				elif inp[1] == "Down":
					if inp[0] == "Accept":
						curr+=1
						time=1
						if curr == 5:
							temp=1
			if curr == 0:
				self.screen.blit(gui.font.render("Gold: 0",False,config.ColorFont),(120,100))
				time -= tick
				if time <=0:
					time =1
					curr = 1
			elif curr == 1:
				self.screen.blit(gui.font.render("Gold: "+str(int(temp)),False,config.ColorFont),(120,100))
				temp = min(temp+(tick*100),gold)
				if temp>=gold:
					time -= tick
				if time <=0:
					time = 1
					curr = 2
					temp = 0
			elif curr == 2:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,config.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: 0",False,config.ColorFont),(120,112))
				time -= tick
				if time <=0:
					time =1
					curr = 3
			elif curr == 3:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,config.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: "+str(int(temp)),False,config.ColorFont),(120,112))
				temp = min(temp+(tick*100),exp)
				for ally in players:
					if ally.getExp()+temp>=ally.getExpNext():
						tempX = max(min(ally.getGraphicObject().getPos()[0]+self.x,265),5)
						tempY = ally.getGraphicObject().getPos()[1] -5
						if tempX +30>x and tempX<x+width:
							tempY = 180
						if blink<=.5:
							self.screen.blit(gui.font.render("Level Up!",False,config.ColorFont),(tempX,tempY))
						else:
							self.screen.blit(gui.font.render("Level Up!",False,config.ColorSel),(tempX,tempY))
				if temp>=exp:
					time -= tick
					if time <=0:
						time = 1
						curr = 4
						temp = 0
			elif curr == 4:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,config.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: "+str(exp),False,config.ColorFont),(120,112))
				for ally in players:
					if ally.getExp()+exp>=ally.getExpNext():
						tempX = max(min(ally.getGraphicObject().getPos()[0]+self.x,265),5)
						tempY = ally.getGraphicObject().getPos()[1] -5
						if tempX +30>x and tempX<x+width:
							tempY = 180
						if blink<=.5:
							self.screen.blit(gui.font.render("Level Up!",False,config.ColorFont),(tempX,tempY))
						else:
							self.screen.blit(gui.font.render("Level Up!",False,config.ColorSel),(tempX,tempY))
				self.screen.blit(gui.font.render("Items:",False,config.ColorFont),(120,124))
				time -= tick
				if time <=0:
					time =1
					curr = 5
					temp = 1
			elif curr == 5:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,config.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: "+str(exp),False,config.ColorFont),(120,112))
				for ally in players:
					if ally.getExp()+exp>=ally.getExpNext():
						tempX = max(min(ally.getGraphicObject().getPos()[0]+self.x,265),5)
						tempY = ally.getGraphicObject().getPos()[1] -5
						if tempX +30>x and tempX<x+width:
							tempY = 180
						if blink<=.5:
							self.screen.blit(gui.font.render("Level Up!",False,config.ColorFont),(tempX,tempY))
						else:
							self.screen.blit(gui.font.render("Level Up!",False,config.ColorSel),(tempX,tempY))
				self.screen.blit(gui.font.render("Items:",False,config.ColorFont),(120,124))
				if len(items)==0:
					self.screen.blit(gui.font.render("No Items",False,config.ColorFont),(120,136))
				else:
					for i in range(0,temp):
						self.screen.blit(items[i].getSprite(),((26*i)+140+offset,136))
					if temp<len(items):
						time -= tick
						if time <= 0:
							time = 1
							temp += 1
			else:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,config.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: "+str(exp),False,config.ColorFont),(120,112))
				self.screen.blit(gui.font.render("Items:",False,config.ColorFont),(120,124))
				if len(items)==0:
					self.screen.blit(gui.font.render("No Items",False,config.ColorFont),(120,136))
				else:
					for i in range(0,len(items)):
						self.screen.blit(items[i].getSprite(),((26*i)+140+offset,136))
				showing = False
			if self.isScaled:
				self.screen.update()
			pygame.display.flip()

	## Updates objects
	#
	#  Updates all objects, draws them in the correct order and in the correct place in relation to the camera.
	#  @param tick Time that has passed since last clock cycle, in seconds.
	def update(self,tick):

		if self.focus != None:
			if self.focus.getX()+self.getX()+(self.focus.getWidth()/2)<158:
				self.scrollX(-self.focus.getSpd()*10*tick)
			elif self.focus.getX()+self.getX()+(self.focus.getWidth()/2)>162:
				self.scrollX(self.focus.getSpd()*10*tick)
			else:	#Stabilization Code
				self.setX(160-(self.focus.getWidth()/2) - self.focus.getX())

			#Perfect tracking with no scroll:
			self.setX(160-(self.focus.getWidth()/2) - self.focus.getX())

		if self.bgF!=None:
			self.screen.blit(self.bgF,[int(self.x*.5),int(self.y*.5)])
		#self.screen.blit(self.bgC,[int(self.x*.9),int(self.y*.9)])
		self.screen.blit(self.bgC,[self.getX(),self.getY()])
		self.screen.blit(self.bgG,[self.getX(),self.getY()+180])

		for enemy in self.enemies:
			enemy.update(tick)
			if enemy!=self.focus:
				enemy.draw(self.screen,self.getX(),self.getY())

		for ally in self.allies:
			ally.update(tick)
			if ally!=self.focus:
				ally.draw(self.screen,self.getX(),self.getY())
				#self.screen.blit(ally.getSprite(),[ally.getX()+self.getX(),ally.getY()+self.getY()])

		for projectile in self.projectiles:
			projectile.update(tick)
			if projectile!=self.focus:
				projectile.draw(self.screen,self.getX(),self.getY())

		self.composite()

		if self.focus!=None:
			self.focus.draw(self.screen,self.getX(),self.getY())
			#self.screen.blit(self.focus.getSprite(),[self.focus.getX()+self.getX(),self.focus.getY()+self.getY()])

		self.hud.draw(self.screen)

		for dmg in self.dmgVals:
			if dmg[3]<=1:
				self.screen.blit(gui.font.render(str(dmg[0]),True,dmg[2]),(dmg[1][0]+self.getX(),int(dmg[1][1])+self.getY()))
			else:
				temp=gui.font.render(str(dmg[0]),True,dmg[2])
				temp.fill((255,255,255,int((4-dmg[3])*255/4)),special_flags=BLEND_RGBA_MULT)
				self.screen.blit(temp,(dmg[1][0]+self.getX(),int(dmg[1][1])+self.getY()))
			dmg[1][1]-=(tick*10)
			dmg[3]+=tick
			if dmg[3]>4:
				self.dmgVals.remove(dmg)

		self.screen.blit(gui.font.render(self.debugInfo,True,[255,255,255]),[0,228])

		if self.isScaled:
			self.screen.update()
		pygame.display.flip()

## An object that contains graphics information for battles.
class BattleGraphicObject(object):

	## Constructor.
	#  @param animations A dictionary of Animation objects.
	#  @param pos Starting position of object.
	#  @param spd Movement spd of object.
	#  @param direction Direction object is facing.
	#  @param state Current state of object.
	#  @param weapon An items.Weapon object to be drawn with the character.
	def __init__(self,animations,pos,spd,direction=1,state="Idle",weapon=None):
		self.animations=animations
		self.currentAnimation = self.animations[state][direction]

		#for i in range(len(self.animations)):
		#	self.animations[i].append([])
		#	for k in range(len(self.animations[i][0])):
		#		self.animations[i][0][k]=pygame.transform.smoothscale(self.animations[i][0][k],(100,100))
		#		self.animations[i][1].append(pygame.transform.flip(pygame.transform.smoothscale(self.animations[i][0][k],(100,100)),True,False))

		self.x=pos[0]
		self.y=pos[1]
		self.direction=direction
		self.spd=spd

		self.state=state
		self.weapon = weapon
		self.genWeaponAnim()
		if self.weapon != None:
			self.weaponAnimCurr = self.weaponAnim[state][direction]

	def getCopy(self):
		return BattleGraphicObject(self.animations,self.getPos(),self.spd,self.direction,self.state,self.weapon)

	## Generates the weapons animation data.
	def genWeaponAnim(self,skills=[]):
		if self.weapon != None:
			self.weaponAnim = {}
			self.weaponAnim["Idle"] = [Animation(None,None,"IdleW"),loadAnimation(self.weapon.getAnimationPath(),"Idle")]
			self.weaponAnim["Run"] = [Animation(None,None,"WalkW"),loadAnimation(self.weapon.getAnimationPath(),"Walk")]

			if self.weapon.getStyle().getType() == "Combo":
				for i in range(1,self.weapon.getStyle().getChain()+1):
					self.weaponAnim["Attack"+str(i)] = [Animation(None,None,"AttackW"+str(i)),loadAnimation(self.weapon.getAnimationPath(),"Attack"+str(i))]
			elif self.weapon.getStyle().getType() == "Charge":
				self.weaponAnim["Attack"] = [Animation(None,None,"AttackW"),loadAnimation(self.weapon.getAnimationPath(),"Attack")]

			self.weaponAnim["Death"] = [Animation(None,None,"DeathW"),loadAnimation(self.weapon.getAnimationPath(),"Death")]

			#Mirroring
			temp = self.weaponAnim["Idle"][1].getFrames()
			i=0
			for frame in temp:
				self.weaponAnim["Idle"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
				i+=1
			#Run
			temp = self.weaponAnim["Run"][1].getFrames()
			i=0
			for frame in temp:
				self.weaponAnim["Run"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
				i+=1
			#Attack
			if self.weapon.getStyle().getType() == "Combo":
				for i in range(1,self.weapon.getStyle().getChain()+1):
					temp = self.weaponAnim["Attack"+str(i)][1].getFrames()
					j = 0
					for frame in temp:
						self.weaponAnim["Attack"+str(i)][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,j))
						j+=1
			elif self.weapon.getStyle().getType() == "Charge":
				temp = self.weaponAnim["Attack"][1].getFrames()
				i=0
				for frame in temp:
					self.weaponAnim["Attack"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
					i+=1
			#Death
			temp = self.weaponAnim["Death"][1].getFrames()
			i=0
			for frame in temp:
				self.weaponAnim["Death"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
				i+=1

			#Skills:
			for skill in skills:
				print skill
				self.weaponAnim[skill] = [Animation(None,None,skill+"W"),loadAnimation(self.weapon.getAnimationPath(),skill)]
				temp = self.weaponAnim[skill][1].getFrames()
				i=0
				for frame in temp:
					self.weaponAnim[skill][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i,offset=frame.getOffset()))
					i+=1
				self.weaponAnim[skill][0].setNextAnimation(self.weaponAnim["Idle"][0])
				self.weaponAnim[skill][1].setNextAnimation(self.weaponAnim["Idle"][1])

			#Linking
			if self.weapon.getStyle().getType() == "Combo":
				for i in range(1,self.weapon.getStyle().getChain()+1):
					self.weaponAnim["Attack"+str(i)][0].setNextAnimation(self.weaponAnim["Idle"][0])
					self.weaponAnim["Attack"+str(i)][1].setNextAnimation(self.weaponAnim["Idle"][1])

	## Sets object's position.
	def setPos(self,pos):
		self.x=pos[0]
		self.y=pos[1]

	## Returns the width of the current sprite.
	def getWidth(self):
		return self.getSprite().get_width()

	## Returns the height of the current sprite.
	def getHeight(self):
		return self.getSprite().get_height()

	## Returns the x component of position.
	def getX(self):
		return self.x

	## Returns the y component of position.
	def getY(self):
		return self.y

	## Returns a list containing [x,y].
	def getPos(self):
		return [self.x,self.y]

	## Sets the x component of position.
	def setX(self,x):
		self.x=x

	## Sets the y component of position.
	def setY(self,y):
		self.y=y

	## Sets the current state of this object.
	def setState(self,state):
		self.state=state
		self.currentAnimation.reset()
		self.currentAnimation = self.animations[self.state][self.direction]
		if self.weapon != None:
			self.weaponAnimCurr.reset()
			self.weaponAnimCurr = self.weaponAnim[self.state][self.direction]

	## Sets the direction this object is facing.
	def setDirection(self,direction):
		self.direction=direction
		#f = self.currentAnimation.getFrame()
		self.currentAnimation.reset()
		self.currentAnimation = self.animations[self.state][self.direction]
		if self.weapon != None:
			self.weaponAnimCurr.reset()
			self.weaponAnimCurr = self.weaponAnim[self.state][self.direction]
		#self.currentAnimation.setFrame(f)

	## Sets the Frame of this object.
	def setFrame(self,frame):
		self.currentAnimation.setFrame(frame)
		if self.weapon != None:
			self.weaponAnimCurr.setFrame(frame)

	## Returns the current state for this object.
	def getState(self):
		return self.state

	## Returns the current animation's name.
	#
	#  Useful for finding out the state of the animation.
	def getCurrAnimName(self):
		return self.currentAnimation.getName()

	## Returns the current sprite for this object.
	def getSprite(self):
		return self.currentAnimation.getSprite()

	## Returns the current frame in the current animation this object is at.
	def getFrame(self):
		return self.currentAnimation.getFrame()

	## Returns the movement speed for this object.
	def getSpd(self):
		return self.spd

	def setWeapon(self,weapon,skills=[]):
		self.weapon=weapon
		self.genWeaponAnim(skills)
		if self.weapon != None:
			self.weaponAnimCurr = self.weaponAnim[self.state][self.direction]

	## Updates animations, to be used when equipping a new weapon.
	def updateAnimations(self,animations):
		self.animations=animations
		self.currentAnimation = self.animations[self.state][self.direction]

	## Updates this object.
	#  @param tick Time that has passed since last clock cycle, in seconds.
	def update(self,tick):
		self.currentAnimation = self.currentAnimation.update(tick)
		if self.weapon != None:
			self.weaponAnimCurr = self.weaponAnimCurr.update(tick)

	## Draws this object to @c screen.
	#
	#  @param screen A reference to either a Pygame screen object or a scaledScreen.
	#  @param offsetX The x offset from the camera
	#  @param offsetY The y offset from the camera
	def draw(self,screen,offsetX,offsetY):
		if self.weapon == None:
			if self.direction == 0:
				screen.blit(self.getSprite(),[self.x-self.currentAnimation.getOffset()[0]+offsetX,self.y+self.currentAnimation.getOffset()[1]+offsetY])
			else:
				screen.blit(self.getSprite(),[self.x+self.currentAnimation.getOffset()[0]+offsetX,self.y+self.currentAnimation.getOffset()[1]+offsetY])
		else:
			if self.direction == 0:
				screen.blit(self.getSprite(),[self.x-self.currentAnimation.getOffset()[0]+offsetX,self.y+self.currentAnimation.getOffset()[1]+offsetY])
				screen.blit(self.weaponAnimCurr.getSprite(),[self.x+(self.weaponAnimCurr.getOffset()[0])+offsetX-self.weapon.getOffset()[0],self.y+self.weaponAnimCurr.getOffset()[1]+offsetY+self.weapon.getOffset()[1]])
			else:
				screen.blit(self.getSprite(),[self.x+self.currentAnimation.getOffset()[0]+offsetX,self.y+self.currentAnimation.getOffset()[1]+offsetY])
				screen.blit(self.weaponAnimCurr.getSprite(),[self.x+self.weaponAnimCurr.getOffset()[0]+offsetX+self.weapon.getOffset()[0],self.y+self.weaponAnimCurr.getOffset()[1]+offsetY+self.weapon.getOffset()[1]])
			#if self.direction == 1:
			#else:
			#	screen.blit(self.weaponAnimCurr.getSprite(),[self.x+offsetX-self.weapon.getOffset()[0],self.y+offsetY+self.weapon.getOffset()[1]])
