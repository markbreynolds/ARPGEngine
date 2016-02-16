## @package graphics
#  Documentation for the Graphics Module.
#
#  This module contains the code related the screen and graphics.

import pygame
import math
import gui

from pygame.locals import *

## @deprecated Use fonts in gui
font = pygame.font.Font("Fonts/visitor1.ttf",10)

## Sort function for sorting by y
#
#  Allows things that have smallers y values to be drawn first.
def sortY(a):
	if int(a.getPos()[1])!=a.getPos()[1]:
		print "Sort Error: "+str(type(a))
	return int(a.getPos()[1]+a.getHeight())

## A window that emulates a smaller python window.
class ScaledScreen(object):
	
	## Constructor.
	#  @param screen Reference to pygame screen object.
	#  @param actualResX Horizontal resolution of pygame window.
	#  @param actualResY Vertical resolution of pygame window.
	#  @param smoothing
	#  @parblock
	#  Smoothing type to use.
	#
	#       Smoothing Types:
	#         0 = No smoothing.
	#         1 = 2x smoothing.
	#         2 = Full smoothing.
	#
	#  @endparblock
	def __init__(self,screen,actualResX,actualResY,smoothing=0):
		self.scaledScreen=screen
		self.aResX=actualResX
		self.aResY=actualResY
		self.screen=pygame.surface.Surface((320,240))
		self.smoothing=smoothing
		if self.smoothing==1:
			self.aResX=640
			self.aResY=480
	
	## Updates the pygame screen by scaling the internal screen.
	def update(self):
		if self.smoothing==0:
			pygame.transform.scale(self.screen,(self.aResX,self.aResY),self.scaledScreen)
		elif self.smoothing==1:
			pygame.transform.scale2x(self.screen,self.scaledScreen)
		elif self.smoothing==2:
			pygame.transform.smoothscale(self.screen,(self.aResX,self.aResY),self.scaledScreen)
	
	## Functions the same as pygame.Surface.fill().
	#  @param color Color to fill screen.
	#  @param rect Rectangle to fill within, if @c None then fill entire screen.
	#  @param special_flags Fill mode, see Pygame documentation.
	def fill(self,color,rect=None,special_flags=0):
		if rect!=None:
			if rect[0]<0:
				rect[2]-=abs(rect[0])
			if rect[1]<0:
				rect[3]-=abs(rect[1])
		self.screen.fill(color,rect,special_flags)
	
	## Functions the same as pygame.Surface.fill().
	#  @param source Source image to copy
	#  @param dest Destination location to copy image to on screen.
	#  @param area Area of source to copy, if @c None then copy entire image.
	#  @param special_flags Copy mode, see Pygame documentation.
	def blit(self,source,dest,area=None,special_flags=0):
		self.screen.blit(source,dest,area,special_flags)
	
	## Functions the same as pygame.Surface.copy().
	def copy(self,*args):
		return self.screen.copy(*args)
	
## Container for a single frame in an animation.
class AnimationFrame(object):
	
	## Constructor.
	#  @param image Image data.
	#  @param delay Delay before proceeding to next frame, in seconds.
	#  @param nextFrame Reference to next AnimationFrame.
	#  @param number Frame number.
	def __init__(self,image,delay,nextFrame,number):
		self.image = image
		self.delay = delay
		self.nextFrame = nextFrame
		self.number = number
		self.count = 0
	
	## Returns this frame's image data
	def getImage(self):
		return self.image
	
	## Returns the delay before proceeding to the next frame, in seconds.
	def getDelay(self):
		return self.delay
	
	## Returns the next frame.
	def getNextFrame(self):
		return self.nextFrame
	
	## Returns this frame's frame number.
	def getNumber(self):
		return self.number
	
	## Updates this frame and returns the current frame.
	#  @param tick Time that has passed since last clock cycle in seconds.
	def update(self,tick):
		self.count += tick
		if self.count >= self.delay:
			self.count=0
			return self.nextFrame
		else:
			return self
	
	## Resets frame to original state.
	def reset(self):
		self.count = 0

## Container for a sequence of frames.
class Animation(object):
	
	## Constructor.
	#  @param firstFrame First AnimationFrame in the sequence.
	#  @param nextAnimation Reference to next Animation.
	#  @param name Name of animation.
	def __init__(self,firstFrame,nextAnimation,name):
		self.firstFrame = firstFrame
		self.nextAnimation = nextAnimation
		self.frame = self.firstFrame
		self.name = name
	
	## Adds a frame to the animation.
	#  @param frame Frame to be added.
	def addFrame(self,frame):
		if self.firstFrame == None:
			self.firstFrame = frame
			self.frame = self.firstFrame
		else:
			temp = self.firstFrame
			while temp.nextFrame != None:
				temp = temp.nextFrame
			temp.nextFrame = frame
	
	## Returns a list of AnimationFrame objects in the animation.
	def getFrames(self):
		temp = self.firstFrame
		if temp == None:
			return []
		else:
			ret = [temp]
			while temp.nextFrame != None:
				temp = temp.nextFrame
				ret.append(temp)
			return ret
	
	## Returns the current frame number.
	def getFrame(self):
		return self.frame.number + (float(self.frame.count)/self.frame.delay)
	
	## Returns the next animation.
	def getNextAnimation(self):
		return self.nextAnimation
	
	## Returns this animation's name.
	def getName(self):
		return self.name
	
	## Sets the current frame number.
	def setFrame(self,frame):
		temp = self.firstFrame
		while temp.number != int(frame):
			if temp.nextFrame == None:
				if temp.number<int(frame):
					self.frame=self.firstFrame
					return
			temp = temp.nextFrame
		self.frame = temp
		self.frame.count = (frame-int(frame))*self.frame.delay
	
	## Sets the next animation, useful for manual linking.
	def setNextAnimation(self,animation):
		self.nextAnimation = animation
	
	## Updates this animation and returns the current animation.
	#
	#  Also updates the current frame.
	#  @param tick Time that has passed since last clock cycle in seconds.
	def update(self,tick):
		self.frame = self.frame.update(tick)
		if self.frame == None:
			self.frame = self.firstFrame
			if self.nextAnimation == None:
				return self
			else:
				return self.nextAnimation
		else:
			return self
	
	## Resets animation to original state.
	#
	#  Also resets current frame to original state.
	def reset(self):
		self.frame.reset()
		self.frame = self.firstFrame
	
	## Returns the current frame's image.
	def getSprite(self):
		return self.frame.image

## Loads an animation from a file and returns an Animation object
#
#  Supports the following tags:
#  + @c delay - Sets the default delay between frames for this animation, in seconds.
#  + @c nextAnimation - Sets the animation which should occur after this animation, given no change in state.
#  + @c Frame - Subobject which contains AnimationFrame data.
#
#  The @c Frame subobject supports:
#  + @c image - Sets the image or sprite for this frame.
#  + @c number - Sets the frame number.  Auto numbers if not defined.
#  + @c delay - Sets the delay between this frame and the next, in seconds.
#
#  @note
#  @parblock
#  Frames will be linked in the order they are listed.
#
#  i.e. The first frame listed, will be displayed first. The second frame listed, will be displayed second. etc.
#  @endparblock
#
#  @param xmlPath Path to xml file containing animation data.
#  @param animation Name of animation to load from file.
def loadAnimation(xmlPath,animation):
	filer = open(xmlPath,"r")
	lines = filer.readlines()
	
	started=False
	animData = []
	
	for i in range(len(lines)):	#Strip Tabs and New Lines
		lines[i] = lines[i].lstrip("\t").rstrip("\n")
	
	for line in lines:	#Extract Level Data
		if not started:
			if line == "<Animation "+animation+">":
				started=True
			continue
		if line == "</Animation>":
			animData.append(line)
			break
		animData.append(line)
	
	frames = []
	i = 0
	globalDelay = None
	nextAnimation=None
	
	while animData[i]!="</Animation>":
		if animData[i].startswith("<delay>"):
			globalDelay = float(animData[i][7:-8])
		if animData[i].startswith("<nextAnimation>"):
			nextAnimation = animData[i][15:-16]
		elif animData[i] == "<Frame>":
			i+=1
			
			image =None
			number=len(frames)
			delay = globalDelay
			
			while animData[i] != "</Frame>":
				if animData[i].startswith("<image>"):
					image = pygame.image.load(animData[i][7:-8]).convert_alpha()
				elif animData[i].startswith("<number>"):
					number = int(animData[i][8:-9])
				elif animData[i].startswith("<delay>"):
					delay = float(animData[i][7:-8])
				i+=1
			
			frames.append(AnimationFrame(image,delay,None,number))
		i+=1
	
	for i in range(len(frames)-1):
		frames[i].nextFrame = frames[i+1]
	
	return Animation(frames[0],nextAnimation,animation)

## An object that contains text to be drawn on the screen.
#
#  @deprecated To be used for debugging purposes only!
class TextObject(object):
	
	## Constructor.
	#  @param text Text to be displayed.
	#  @param pos Position to display the text.
	#  @param color Color the text should be displayed in.
	def __init__(self,text,pos,color=(255,255,255)):
		self.text = text
		self.color = color
		self.sprite = font.render(text,True,color)
		self.pos=pos
		self.layer=1
	
	## Sets text to be drawn.
	#
	#  @note @c update() must be called before this change will take effect.
	def setText(self,text):
		self.text=text
	
	## Sets position.
	def setPos(self,pos):
		self.pos=pos
	
	## Updates the object's sprite.
	#
	#  This function must be called after changing either the text or color in order for those changes to take effect.
	def update(self,tick=None):
		self.sprite = font.render(self.text,True,self.color)
	
	## Returns the position of this object.
	def getPos(self):
		return self.pos
	
	## Returns the x portion of position.
	def getX(self):
		return self.pos[0]
	
	## Returns the y portion of position.
	def getY(self):
		return self.pos[1]
	
	## Returns the sprite containing the text described in this object.
	def getSprite(self):
		return self.sprite
	
	## Returns the height of this object?
	#
	#
	def getHeight(self):
		return 240
		
	## Draws this object to @c screen.
	#
	#  @param screen A reference to either a Pygame screen object or a scaledScreen.
	#  @param offsetX The x offset from the camera
	#  @param offsetY The y offset from the camera
	def draw(self,screen,offsetX,offsetY):
		screen.blit(self.getSprite(),[self.getX()+offsetX,self.getY()+offsetY])


## An object that contains graphics information.
#
#  Anything that the character can interact with should use this.
class GraphicObject(object):
	
	## Constructor.
	#  @param animations An Animation object containing animation data for this object.
	#  @param parent Reference to parent object, ie. the Player class for the player's graphic object.
	#  @param state Starting state of the object.
	#  @param direction
	#  @parblock
	#  Direction object is facing.
	#
	#       Directions:
	#         0 = North
	#         1 = East
	#         2 = South
	#         3 = West
	#
	#  @endparblock
	#  @param layer Sets draw order for objects.  Objects in layer 1 render first, then objects in layer 0, etc.
	def __init__(self,animations,parent=None,state="Idle",direction=0,layer=0):
		self.animations = animations
		self.currentAnimation = self.animations[state][direction]
		
		self.state = state
		self.direction = direction	#0-N, 1-E, 2-S, 3-W
		self.layer = layer
		self.parent= parent
		
		#Keeping x and y as separate variables is more efficent than tuples and lists when tested with adding, subtracting, and defining.
		self.x = 0
		self.y = 0
	
	## Sets where the object should be drawn.
	#
	#  Does not change where object is in regards to interactions with objects.
	#  See game.GameObject.setPos().
	def setPos(self,pos):
		self.x=pos[0]
		self.y=pos[1]
	
	## Returns width of current frame.
	def getWidth(self):
		return self.getSprite().get_width()
	
	## Returns height of current frame.
	def getHeight(self):
		return self.getSprite().get_height()
	
	## Returns where the object is being drawn.
	def getPos(self):
		return [self.x,self.y]
	
	## Returns a reference to the parent object.
	def getParent(self):
		return self.parent
	
	## Returns the x portion of position.
	def getX(self):
		return self.x
	
	## Returns the y portion of position.
	def getY(self):
		return self.y
	
	## Sets the current state of the object.
	def setState(self,state):
		self.state=state
		self.currentAnimation.reset()
		self.currentAnimation = self.animations[self.state][self.direction]
	
	## Sets the direction the object is facing.
	def setDirection(self,direction):
		self.direction=direction
		f = self.currentAnimation.getFrame()
		self.currentAnimation.reset()
		self.currentAnimation = self.animations[self.state][self.direction]
		self.currentAnimation.setFrame(f)
	
	## Returns the current frame's image.
	def getSprite(self):
		return self.currentAnimation.getSprite()
	
	## Returns the current frame number.
	def getFrame(self):
		return self.currentAnimation.getFrame()
	
	## Sets the current frame number.
	def setFrame(self,frame):
		self.currentAnimation.setFrame(frame)
	
	## Updates this object.
	#  @param tick Time that has passed since last clock cycle in seconds.
	def update(self,tick):
		self.currentAnimation = self.currentAnimation.update(tick)

## Graphics Engine for main portion of game.
#
#  Only one instance of the graphics engine should be running at any given time.
class GraphicsEngine(object):
	
	## Constructor.
	#  @param screen A reference to either a Pygame screen object or a scaledScreen.
	#  @param isScaled If @c screen is a scaledScreen, then should be @c True.
	def __init__(self,screen,isScaled=False):
		self.screen = screen
		self.isScaled = isScaled
		self.objects = []
		self.player = None
		self.background = pygame.surface.Surface([0,0])
		self.cameraPosX = 0
		self.cameraPosY = 0
		self.focus=None
		
		self.talking=None
		self.shop=False
		self.paused=False
		self.inven=False
		self.sleep=False
		self.sleepTime = 0
		self.levelName=None
		self.debug=False
		
		self.compEffect = None
		self.compValue = [0,0,0]
		self.compValChg = None
	
	## Add an object.
	#
	#  Adds an object to the list of objects to be drawn and updated.
	#  @param Object Object to be added.
	def addObject(self,Object):
		self.objects.append(Object)
	
	## Clears object list.
	def clearObjects(self):
		self.objects = []
	
	## Sets who is the player.
	#  @param player The player.
	def setPlayer(self,player):
		self.player = player
	
	## Sets the focus of the camera.
	#
	#  Sets an object for the camera to follow.
	#  @param focus Object for camera to follow.
	def setFocus(self,focus):
		self.focus = focus
	
	## Sets up the GUI for who the player is talking to.
	#  @param talking The NPC the player is talking to.
	def setTalking(self,talking):
		self.talking=gui.Dialog(talking,self.player.getParent())
	
	## Exits a conversation.
	def resetTalking(self):
		self.talking=None
	
	## Returns whether or not the player is talking to someone.
	def getTalking(self):
		return self.talking
	
	## Sets which shop the player is interacting with
	def setShop(self,shop):
		self.shop = shop
	
	## Returns which shop the player is interacting with
	def getShop(self):
		return self.shop
	
	def getSleep(self):
		return self.sleep
	
	## Sets the name of the current area.
	def setLevelName(self,name):
		self.levelName=name
	
	## Toggles whether or not the player's inventory is open.
	def toggleInven(self):
		if self.inven:
			self.inven=False
		else:
			self.inven=gui.InvenMenu(self.player.getParent(),self.levelName)
	
	## Returns the InvenMenu object for the player.
	def getInven(self):
		return self.inven
	
	## Toggles the pause menu.
	def togglePause(self):
		if self.paused:
			self.paused=False
		else:
			self.paused=gui.PauseMenu()
	
	## Returns the PauseMenu object.
	def getPause(self):
		return self.paused
	
	## Loads a new area
	#
	#  @deprecated Replaced by setBackground().
	def loadLevel(self,level):
		self.background = pygame.image.load("Backgrounds/Images/"+level+".png").convert()
	
	## Sets an image as the background
	def setBackground(self,bg):
		self.background = bg
	
	## Returns the screen
	#
	#  For passing the screen to the BattleGraphicsEngine, not for drawing things to the screen without using the engine.
	def getScreen(self):
		return self.screen
	
	## Returns if is using a ScaledScreen
	#
	#  For passing to the BattleGraphicsEngine
	def getIsScaled(self):
		return self.isScaled
	
	## Uses composite effects to create visual effects.
	#
	#  May not work?
	#
	#  @todo Add more effects
	def composite(self,tick=1):
		if self.compEffect==None:
			return
		else:
			if self.compValChg != None:
				if 0<self.compValue[0]+self.compValChg[0]*tick<255:
					self.compValue[0]+=self.compValChg[0]*tick
				if 0<self.compValue[1]+self.compValChg[1]*tick<255:
					self.compValue[1]+=self.compValChg[1]*tick
				if 0<self.compValue[2]+self.compValChg[2]*tick<255:
					self.compValue[2]+=self.compValChg[2]*tick
			self.screen.fill(self.compValue,special_flags=self.compEffect)
	
	## Updates objects
	#
	#  Updates all objects, draws them in the correct order and in the correct place in relation to the camera.
	#  @param tick Time that has passed since last clock cycle, in seconds.
	def update(self,tick):
		self.screen.fill((0,0,0))
		
		if self.focus != None:
			if self.background.get_width()>320:
				offsetX = self.focus.getX()+(self.focus.getWidth()/2)-160
			else:
				offsetX = 0
			if self.background.get_height()>240:
				offsetY = self.focus.getY()+(self.focus.getHeight()/2)-120
			else:
				offsetY = 0
		else:
			offsetX=0
			offsetY=0
		
		for Object in self.objects:
			Object.update(tick)
		
		
		self.player.update(tick)
		self.objects.append(self.player)
		
		self.screen.blit(self.background,(self.cameraPosX-offsetX,self.cameraPosY-offsetY))
		for go in self.objects:
			if go.layer<0:
				self.screen.blit(go.getSprite(),(go.getX()-offsetX,go.getY()-offsetY))
		
		self.objects.sort(key=sortY,reverse=False)
		for go in self.objects:
			if go.layer==0:
				self.screen.blit(go.getSprite(),(go.getX()-offsetX,go.getY()-offsetY))
		
		for go in self.objects:
			if go.layer==1:
				self.screen.blit(go.getSprite(),(go.getX()-offsetX,go.getY()-offsetY))
		
		self.objects.remove(self.player)
		
		if self.inven:
			if self.inven.update(self.screen,tick):
				self.toggleInven()
		
		if self.shop != False:
			if self.shop.update(self.screen,tick):
				self.shop = False
		
		if self.paused:
			self.paused.update(self.screen,tick)
		
		if self.talking != None:
			if self.talking.update(self.screen,tick)==False:
				if self.talking.getShop() == "Buy":
					self.setShop(gui.ShopBuyMenu(self.player.getParent(),self.talking.talking.getShop()))
				elif self.talking.getShop() == "Sell":
					self.setShop(gui.ShopSellMenu(self.player.getParent()))
				elif self.talking.getSleep():
					self.player.getParent().setCanMove(False)
					self.sleep=True
					self.sleepTime = 3.0
					self.compValue=[253.9,253.9,253.9]
					self.compValChg=[-127,-127,-127]
					self.compEffect=BLEND_RGB_MULT
				self.talking.talking.setTalking(False)
				self.talking=False
		
		if self.sleep:
			if self.sleepTime <= 0:
				self.compValChg=[255,255,255]
			else:
				self.sleepTime -= tick
			if self.compValue[0] >= 254:
				self.compEffect = None
				self.sleep = False
				self.player.getParent().setCanMove(True)
		
		for go in self.objects:
			if go.layer==2:
				self.screen.blit(go.getSprite(),(go.getX()-offsetX,go.getY()-offsetY))
		
		self.composite(tick)
		
		if self.debug:
			self.debug.update()
			self.screen.blit(self.debug.getSprite(),[0,0])
		
		if self.isScaled:
			self.screen.update()
		pygame.display.update()

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
	def genWeaponAnim(self):
		if self.weapon != None:
			self.weaponAnim = {}
			self.weaponAnim["Idle"] = [Animation(None,None,"IdleW"),loadAnimation(self.weapon.getAnimationPath(),"Idle")]
			self.weaponAnim["Run"] = [Animation(None,None,"WalkW"),loadAnimation(self.weapon.getAnimationPath(),"Walk")]
			for i in range(1,self.weapon.getStyle().getChain()+1):
				self.weaponAnim["Attack"+str(i)] = [Animation(None,None,"AttackW"+str(i)),loadAnimation(self.weapon.getAnimationPath(),"Attack"+str(i))]
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
			for i in range(1,self.weapon.getStyle().getChain()+1):
				temp = self.weaponAnim["Attack"+str(i)][1].getFrames()
				j = 0
				for frame in temp:
					self.weaponAnim["Attack"+str(i)][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,j))
					j+=1
			#Death
			temp = self.weaponAnim["Death"][1].getFrames()
			i=0
			for frame in temp:
				self.weaponAnim["Death"][0].addFrame(AnimationFrame(pygame.transform.flip(frame.getImage(),True,False),frame.getDelay(),None,i))
				i+=1
			
			#Linking
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
	
	def setWeapon(self,weapon):
		self.weapon=weapon
		self.genWeaponAnim()
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
			screen.blit(self.getSprite(),[self.x+offsetX,self.y+offsetY])
		else:
			screen.blit(self.getSprite(),[self.x+offsetX,self.y+offsetY])
			#if self.direction == 1:
			screen.blit(self.weaponAnimCurr.getSprite(),[self.x+offsetX+self.weapon.getOffset()[0],self.y+offsetY+self.weapon.getOffset()[1]])
			#else:
			#	screen.blit(self.weaponAnimCurr.getSprite(),[self.x+offsetX-self.weapon.getOffset()[0],self.y+offsetY+self.weapon.getOffset()[1]])

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
		
		self.bgG=pygame.image.load("Backgrounds/Battle/"+bg+"G.png").convert()	#Ground
		self.bgC=pygame.image.load("Backgrounds/Battle/"+bg+"C.png").convert_alpha()	#Close Objects
		if farBG:
			self.bgF=pygame.image.load("Backgrounds/Battle/"+bg+"F.png").convert()	#Far Objects
		else:
			self.bgF=None
		
		self.compEffect=None
		self.compValue=[0,0,0]
	
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
			self.screen.fill(gui.ColorDark,(x-1,94,width+2,77))
			self.screen.fill(gui.Color,(x,95,width,75))
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
				self.screen.blit(gui.font.render("Gold: 0",False,gui.ColorFont),(120,100))
				time -= tick
				if time <=0:
					time =1
					curr = 1
			elif curr == 1:
				self.screen.blit(gui.font.render("Gold: "+str(int(temp)),False,gui.ColorFont),(120,100))
				temp = min(temp+(tick*100),gold)
				if temp>=gold:
					time -= tick
				if time <=0:
					time = 1
					curr = 2
					temp = 0
			elif curr == 2:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,gui.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: 0",False,gui.ColorFont),(120,112))
				time -= tick
				if time <=0:
					time =1
					curr = 3
			elif curr == 3:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,gui.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: "+str(int(temp)),False,gui.ColorFont),(120,112))
				temp = min(temp+(tick*100),exp)
				for ally in players:
					if ally.getExp()+temp>=ally.getExpNext():
						tempX = max(min(ally.getGraphicObject().getPos()[0]+self.x,265),5)
						tempY = ally.getGraphicObject().getPos()[1] -5
						if tempX +30>x and tempX<x+width:
							tempY = 180
						if blink<=.5:
							self.screen.blit(gui.font.render("Level Up!",False,gui.ColorFont),(tempX,tempY))
						else:
							self.screen.blit(gui.font.render("Level Up!",False,gui.ColorSel),(tempX,tempY))
				if temp>=exp:
					time -= tick
					if time <=0:
						time = 1
						curr = 4
						temp = 0
			elif curr == 4:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,gui.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: "+str(exp),False,gui.ColorFont),(120,112))
				for ally in players:
					if ally.getExp()+exp>=ally.getExpNext():
						tempX = max(min(ally.getGraphicObject().getPos()[0]+self.x,265),5)
						tempY = ally.getGraphicObject().getPos()[1] -5
						if tempX +30>x and tempX<x+width:
							tempY = 180
						if blink<=.5:
							self.screen.blit(gui.font.render("Level Up!",False,gui.ColorFont),(tempX,tempY))
						else:
							self.screen.blit(gui.font.render("Level Up!",False,gui.ColorSel),(tempX,tempY))
				self.screen.blit(gui.font.render("Items:",False,gui.ColorFont),(120,124))
				time -= tick
				if time <=0:
					time =1
					curr = 5
					temp = 1
			elif curr == 5:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,gui.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: "+str(exp),False,gui.ColorFont),(120,112))
				for ally in players:
					if ally.getExp()+exp>=ally.getExpNext():
						tempX = max(min(ally.getGraphicObject().getPos()[0]+self.x,265),5)
						tempY = ally.getGraphicObject().getPos()[1] -5
						if tempX +30>x and tempX<x+width:
							tempY = 180
						if blink<=.5:
							self.screen.blit(gui.font.render("Level Up!",False,gui.ColorFont),(tempX,tempY))
						else:
							self.screen.blit(gui.font.render("Level Up!",False,gui.ColorSel),(tempX,tempY))
				self.screen.blit(gui.font.render("Items:",False,gui.ColorFont),(120,124))
				if len(items)==0:
					self.screen.blit(gui.font.render("No Items",False,gui.ColorFont),(120,136))
				else:
					for i in range(0,temp):
						self.screen.blit(items[i].getSprite(),((26*i)+140+offset,136))
					if temp<len(items):
						time -= tick
						if time <= 0:
							time = 1
							temp += 1
			else:
				self.screen.blit(gui.font.render("Gold: "+str(gold),False,gui.ColorFont),(120,100))
				self.screen.blit(gui.font.render("Exp: "+str(exp),False,gui.ColorFont),(120,112))
				self.screen.blit(gui.font.render("Items:",False,gui.ColorFont),(120,124))
				if len(items)==0:
					self.screen.blit(gui.font.render("No Items",False,gui.ColorFont),(120,136))
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
			#offsetX = self.focus.getX()+(self.focus.getWidth()/2)-160
			#print self.x,offsetX
			#if int(self.x)>offsetX:
			#	self.scrollX(-10*tick)
			#elif int(self.x)<offsetX:
			#	self.scrollX(10*tick)
		
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
				self.screen.blit(font.render(str(dmg[0]),True,dmg[2]),(dmg[1][0]+self.getX(),int(dmg[1][1])+self.getY()))
			else:
				temp=font.render(str(dmg[0]),True,dmg[2])
				temp.fill((255,255,255,int((4-dmg[3])*255/4)),special_flags=BLEND_RGBA_MULT)
				self.screen.blit(temp,(dmg[1][0]+self.getX(),int(dmg[1][1])+self.getY()))
			dmg[1][1]-=(tick*10)
			dmg[3]+=tick
			if dmg[3]>4:
				self.dmgVals.remove(dmg)
		
		if self.isScaled:
			self.screen.update()
		pygame.display.flip()

def blurTrans(clock,screen,oldScreen,newScreen):
	time = 0
	trans = True
	
	while trans:
		if time<.5:
			tick = clock.tick()/1000.0
			temp = pygame.transform.scale(pygame.transform.scale(oldScreen,(int(160-(310*time)),int(120-(230*time)))),(320,240))
			screen.blit(temp,(0,0))
			time+=tick
			screen.update()
			pygame.display.update()
		elif time<1:
			tick = clock.tick()/1000.0
			temp = pygame.transform.scale(pygame.transform.scale(newScreen,(int(5+(630*(time-.5))),int(5+(470*(time-.5))))),(320,240))
			screen.blit(temp,(0,0))
			time+=tick
			screen.update()
			pygame.display.update()
		else:
			trans = False
