import pygame
import config

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
	filer = open(config.AssetPath+xmlPath,"r")
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
					image = pygame.image.load(config.AssetPath+animData[i][7:-8]).convert_alpha()
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
