## @package animator
#  Documentation for the Wireframe Animator Tool.
#
#  This tool is intended to be used to help animate characters by using rigs and armatures.

import math
import pickle
import pygame
from pygame.locals import *

try:
	import pygtk
	import gtk
except ImportError:
	print "pygtk is not installed, please either install it or contact me to add support for ugly non gtk windows."

nextAvailableID = 0
lastFileOpened = None

def loadDialog():
	dialog = gtk.FileChooserDialog("Open..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	
	fltr = gtk.FileFilter()
	fltr.set_name("All Files")
	fltr.add_pattern("*")
	dialog.add_filter(fltr)
	
	fltr = gtk.FileFilter()
	fltr.set_name("Pickle Files")
	fltr.add_pattern("*.pickle")
	dialog.add_filter(fltr)
	
	response = dialog.run()
	if response == gtk.RESPONSE_OK:
		global root, lastFileOpened
		filer = open(dialog.get_filename(),"r")
		root = pickle.load(filer)	#load file
		filer.close()
		lastFileOpened = dialog.get_filename()
	dialog.destroy()
	while gtk.events_pending():		#Yes I've been told this is bad, but I like calling my own code rather than having GTK do it.
		gtk.main_iteration()

def saveDialog():
	dialog = gtk.FileChooserDialog("Save..",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	dialog.set_do_overwrite_confirmation(True)
	if lastFileOpened == None:
		dialog.set_current_name("untitled")
	else:
		dialog.set_current_name(lastFileOpened.split("/")[-1])
	
	fltr = gtk.FileFilter()
	fltr.set_name("All Files")
	fltr.add_pattern("*")
	dialog.add_filter(fltr)
	
	fltr = gtk.FileFilter()
	fltr.set_name("Pickle Files")
	fltr.add_pattern("*.pickle")
	dialog.add_filter(fltr)
	
	response = dialog.run()
	if response == gtk.RESPONSE_OK:
		filename = dialog.get_filename()
		if not filename.endswith(".pickle"):
			filename+=".pickle"
		filew = open(filename,"w")
		pickle.dump(root,filew,protocol=2)	#save file
		filew.close()
	dialog.destroy()
	while gtk.events_pending():		#Yes I've been told this is bad, but I like calling my own code rather than having GTK do it.
		gtk.main_iteration()

def loadRefDialog():
	dialog = gtk.FileChooserDialog("Open..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	
	fltr = gtk.FileFilter()
	fltr.set_name("All Files")
	fltr.add_pattern("*")
	dialog.add_filter(fltr)
	
	fltr = gtk.FileFilter()
	fltr.set_name("Images")
	fltr.add_pattern("*.png")
	fltr.add_pattern("*.jpg")
	fltr.add_pattern("*.gif")
	fltr.add_pattern("*.bmp")
	fltr.add_pattern("*.tga")
	fltr.add_pattern("*.tif")
	dialog.add_filter(fltr)
	
	response = dialog.run()
	if response == gtk.RESPONSE_OK:
		global refImage
		refImage = image(pygame.image.load(dialog.get_filename()).convert_alpha(),[20,20])	#load file
	dialog.destroy()
	while gtk.events_pending():		#This is bad blah blah blah...
		gtk.main_iteration()

## This function returns the next bone ID, and increments nextID by 1.
def nextID():
	global nextAvailableID
	nextAvailableID += 1;
	return nextAvailableID-1

class Timeline(object):
	def __init__(self,screen,interpolate=False):
		self.frame = 0
		self.endFrame = 48
		self.height = 100
		self.color = [0,0,0]
		self.currentColor = [255,0,0]
		self.keyColor = [0,0,255]
		
		self.fps = 24
		self.playing = False
		self.keyframes = []
		self.interpolate = interpolate
		
		self.calcDim(screen)
	
	def addKeyframe(self):
		if self.frame not in self.keyframes:
			self.keyframes.append(self.frame)
	
	def clearKeyframes(self):
		self.keyframes = []
	
	def getTop(self):
		return self.top
	
	def getFrame(self):
		return self.frame
	
	def getInterpolate(self):
		return self.interpolate
	
	def nextFrame(self):
		if self.frame < self.endFrame:
			self.frame+=1
	
	def prevFrame(self):
		if self.frame > 0:
			self.frame-=1
	
	def getPlaying(self):
		return self.playing
	
	def togglePlaying(self):
		self.playing = not self.playing
	
	def play(self,clock):
		clock.tick(self.fps)
		self.frame+=1
		if self.frame>self.endFrame:
			self.frame = 0
	
	def calcDim(self,screen):
		self.left = 0
		self.right = screen.getWidth()
		self.top = screen.getHeight()-self.height
		self.bottom = screen.getHeight()
		
		self.area = [self.left,self.top,screen.getWidth(),self.height]
		
		self.lineSize = (self.right-15)-(self.left+15)		
	
	def draw(self,screen):
		#Draw window
		screen.fill(screen.getWindowBgColor(),self.area)
		pygame.draw.line(screen.getScreen(),screen.getWindowEdgeColor(),(0,self.top),(self.right,self.top),1)
		
		#Draw timeline
		pygame.draw.line(screen.getScreen(),self.color,(self.left+15,self.top+25),(self.right-15,self.top+25),1)
		pygame.draw.line(screen.getScreen(),self.color,(self.left+15,self.top+29),(self.right-15,self.top+29),1)
		pygame.draw.line(screen.getScreen(),self.color,(self.left+15,self.top+22),(self.left+15,self.top+32),1)
		pygame.draw.line(screen.getScreen(),self.color,(self.right-15,self.top+22),(self.right-15,self.top+32),1)
		
		#Draw keyframes:
		for frame in self.keyframes:
			kfPos = self.left+16+int((self.lineSize-2)*(float(frame)/self.endFrame))	#Keyframe Position
			pygame.draw.line(screen.getScreen(),self.keyColor,(kfPos,self.top+23),(kfPos,self.top+31))
		
		#Draw current frame marker
		cfPos = self.left+16+int((self.lineSize-2)*(float(self.frame)/self.endFrame))	#Current Frame Position
		pygame.draw.line(screen.getScreen(),self.currentColor,(cfPos,self.top+23),(cfPos,self.top+31))
		
		#Write frame numbers
		screen.blit(font.render("Frame: %d/%d"%(self.frame,self.endFrame),True,screen.getTextColor()),(self.left+18,self.top+40))

class Info(object):
	def __init__(self,screen,timeline,menu):
		self.width = 150
		self.calcDim(screen,timeline,menu)
		self.refImageMove = False
	
	def getWidth(self):
		return self.width
	
	def getRefImageMove(self):
		return self.refImageMove
	
	def setRefImageMove(self,val):
		self.refImageMove = val
	
	def click(self,pos):
		if pygame.rect.Rect([self.left+12,self.top+96,32,16]).collidepoint(pos):
			loadRefDialog()
		elif refImage != None:
			if pygame.rect.Rect([self.left+48,self.top+96,28,16]).collidepoint(pos):
				refImage.toggleVisiblity()
			if pygame.rect.Rect([self.left+46,self.top+113,14,14]).collidepoint(pos):
				if refImage.getSize() > 1:
					refImage.setSize(refImage.getSize()-1)
			elif pygame.rect.Rect([self.left+64,self.top+113,14,14]).collidepoint(pos):
				refImage.setSize(refImage.getSize()+1)
			elif pygame.rect.Rect([self.left+12,self.top+130,34,16]).collidepoint(pos):
				self.refImageMove = True
			else:
				return False
#		elif pygame.rect.Rect([self.left+68,self.top+25,40,16]).collidepoint(pos):
#			changeInputMode("Numeric")
		else:
			return False
		return True
	
	def calcDim(self,screen,timeline,menu):
		self.left = screen.getWidth()-self.width
		self.right = screen.getWidth()
		self.top = menu.getHeight()
		self.bottom = timeline.getTop()
		
		self.area = [self.left,self.top,self.right-self.left,self.bottom-self.top]
	
	def draw(self,screen,selected):
		#Draw window
		screen.fill(screen.getWindowBgColor(),self.area)
		pygame.draw.line(screen.getScreen(),screen.getWindowEdgeColor(),(self.left,self.top),(self.left,self.bottom),1)
		
		#Write bone info:
		if selected == None:
			screen.blit(font.render("No bone selected.",True,screen.getTextColor()),(self.left+10,self.top+10))
		else:
			#screen.fill(screen.getFieldColor(),[self.left+68,self.top+25,40,16])
			#screen.fill(screen.getFieldColor(),[self.left+52,self.top+43,40,16])
			screen.blit(font.render("Bone "+str(selected.getID()),True,screen.getTextColor()),(self.left+10,self.top+10))
			screen.blit(font.render("Rotation:  %.2f"%(math.degrees(selected.getRot())),True,screen.getTextColor()),(self.left+15,self.top+28))
			screen.blit(font.render("Scale:  %.2f"%(selected.getSize()),True,screen.getTextColor()),(self.left+15,self.top+46))
		
		if refImage == None:
			screen.blit(font.render("No reference image.",True,screen.getTextColor()),(self.left+10,self.top+82))
		else:
			screen.blit(font.render("Reference image loaded.",True,screen.getTextColor()),(self.left+10,self.top+82))
			if refImage.isVisible():
				pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[self.left+48,self.top+96,28,16],1)
				screen.blit(font.render("Hide",True,screen.getTextColor()),(self.left+50,self.top+98))
			else:
				pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[self.left+48,self.top+96,34,16],1)
				screen.blit(font.render("Show",True,screen.getTextColor()),(self.left+50,self.top+98))
			screen.blit(font.render("Scale:",True,screen.getTextColor()),(self.left+10,self.top+114))
			pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[self.left+46,self.top+113,14,14],1)
			pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[self.left+64,self.top+113,14,14],1)
			screen.blit(font.render("-",True,screen.getTextColor()),(self.left+51,self.top+114))
			screen.blit(font.render("+",True,screen.getTextColor()),(self.left+68,self.top+114))
			pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[self.left+12,self.top+130,34,16],1)
			screen.blit(font.render("Move",True,screen.getTextColor()),(self.left+14,self.top+132))
			
		pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[self.left+12,self.top+96,32,16],1)
		screen.blit(font.render("Load",True,screen.getTextColor()),(self.left+14,self.top+98))

class Menu(object):
	def __init__(self,screen):
		self.currentFile = None
		self.height = 18
		self.selected = None
		self.calcDim(screen)
	
	def calcDim(self,screen):
		self.left = 0
		self.right = screen.getWidth()
		self.top = 0
		self.bottom = self.height
		
		self.area = [self.left,self.top,self.right,self.bottom]
	
	def getHeight(self):
		return self.height
	
	def click(self,pos):
		if self.selected == None:
			if pos[1] > self.bottom:
				return False
			x = self.left+4+font.size("File   ")[0]
			if pos[0]<x:
				self.selected = "File"
				return
			x+= font.size("Edit   ")[0]
			if pos[0]<x:
				self.selected = "Edit"
				return
			x+= font.size("View   ")[0]
			if pos[0]<x:
				self.selected = "View"
				return
			x+= font.size("Help   ")[0]
			if pos[0]<x:
				self.selected = "Help"
				return
		elif self.selected == "File":
			if pygame.rect.Rect([self.left+4,self.bottom,50,68]).collidepoint(pos):
				if pos[1]<self.bottom+20:
					global root, timeline
					timeline.clearKeyframes()
					root = Bone(0,100,pos=[150,150])
					self.selected = None
				elif pos[1]<self.bottom+36:
					loadDialog()
				elif pos[1]<self.bottom+52:
					saveDialog()
				elif pos[1]<self.bottom+68:
					pygame.quit()
					exit()
			else:
				self.selected = None
		elif self.selected == "Edit":
			if pygame.rect.Rect([32,self.bottom,78,68]).collidepoint(pos):		#yes 32 is a hard coded value, if it makes problems then I'll fix it. #LazyCoding #Problems
				pass
			else:
				self.selected = None
		elif self.selected == "View":
			if pygame.rect.Rect([62,self.bottom,74,68]).collidepoint(pos):
				pass
			else:
				self.selected = None
		elif self.selected == "Help":
			if pygame.rect.Rect([self.left+4,self.bottom,50,68]).collidepoint(pos):
				pass
			else:
				self.selected = None
	
	def draw(self,screen):
		#Draw window
		screen.fill(screen.getWindowBgColor(),self.area)
		pygame.draw.line(screen.getScreen(),screen.getWindowEdgeColor(),(self.left,self.bottom),(self.right,self.bottom),1)
		
		#Render different menus
		x = self.left+4
		screen.blit(font.render("File",True,screen.getTextColor()),(x,self.top+4))
		x+= font.size("File   ")[0]
		screen.blit(font.render("Edit",True,screen.getTextColor()),(x,self.top+4))
		x+= font.size("Edit   ")[0]
		screen.blit(font.render("View",True,screen.getTextColor()),(x,self.top+4))
		x+= font.size("View   ")[0]
		screen.blit(font.render("Help",True,screen.getTextColor()),(x,self.top+4))
		
		#Show submenu
		if self.selected == "File":
			screen.fill(screen.getWindowBgColor(),[self.left+4,self.bottom,50,68])
			pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[self.left+4,self.bottom,50,68],1)
			screen.blit(font.render("New",True,screen.getTextColor()),(self.left+6,self.bottom+4))
			screen.blit(font.render("Load",True,screen.getTextColor()),(self.left+6,self.bottom+20))
			screen.blit(font.render("Save",True,screen.getTextColor()),(self.left+6,self.bottom+36))
			screen.blit(font.render("Exit",True,screen.getTextColor()),(self.left+6,self.bottom+52))
		elif self.selected == "Edit":
			x=self.left+4+font.size("File   ")[0]
			screen.fill(screen.getWindowBgColor(),[x,self.bottom,78,84])
			pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[x,self.bottom,78,84],1)
			screen.blit(font.render("Undo",True,screen.getTextColor()),(x+2,self.bottom+4))
			screen.blit(font.render("Redo",True,screen.getTextColor()),(x+2,self.bottom+20))
			screen.blit(font.render("Add Bone",True,screen.getTextColor()),(x+2,self.bottom+36))
			screen.blit(font.render("Remove Bone",True,screen.getTextColor()),(x+2,self.bottom+52))
			screen.blit(font.render("Preferences",True,screen.getTextColor()),(x+2,self.bottom+68))
		elif self.selected == "View":
			x=self.left+4+font.size("File   Edit   ")[0]
			screen.fill(screen.getWindowBgColor(),[x,self.bottom,74,68])
			pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[x,self.bottom,74,68],1)
			screen.blit(font.render("Zoom In",True,screen.getTextColor()),(x+2,self.bottom+4))
			screen.blit(font.render("Zoom Out",True,screen.getTextColor()),(x+2,self.bottom+20))
			screen.blit(font.render("Reset Zoom",True,screen.getTextColor()),(x+2,self.bottom+36))
			screen.blit(font.render("Fullscreen",True,screen.getTextColor()),(x+2,self.bottom+52))
		elif self.selected == "Help":
			x=self.left+4+font.size("File   Edit   View   ")[0]
			screen.fill(screen.getWindowBgColor(),[x,self.bottom,44,36])
			pygame.draw.rect(screen.getScreen(),screen.getWindowEdgeColor(),[x,self.bottom,44,36],1)
			screen.blit(font.render("About",True,screen.getTextColor()),(x+2,self.bottom+4))
			screen.blit(font.render("Help",True,screen.getTextColor()),(x+2,self.bottom+20))

## Class that contains the pygame screen and information on how to draw things.
class Screen(object):
	## Constructor
	def __init__(self,x,y):
		self.x = x
		self.y = y
		
		self.edgeThickness = 1
		self.edgeAA = True
		self.edgeColor = [0,0,255]
		
		self.vertSize = 3
		self.vertThickness = 0
		self.vertColor = [0,0,128]
		
		self.selColor = [255,198,0]
		self.modColor = [0,198,255]
		self.bgColor = [255,255,255]
		
		self.windowBgColor = [200,200,200]
		self.windowEdgeColor = [100,100,100]
		self.textColor = [0,0,0]
		self.fieldColor = [230,230,230]
		
		self.screen = pygame.display.set_mode([x,y])
	
	## Fills the screen.
	#
	#  @param color (R,G,B) color to fill the screen with.
	#  @param rect Rect-like object describing the area to fill, if <c>None<c> fills entire screen.
	#  @param special_flags Pygame special flags.
	def fill(self,color,rect=None, special_flags=0):
		self.screen.fill(color,rect,special_flags)
	
	def blit(self,source,dest):
		self.screen.blit(source,dest)
	
	## Updates the screen.
	def update(self):
		pygame.display.update()
	
	## Returns the pygame screen.
	def getScreen(self):
		return self.screen
	
	## Returns how thick edges should be drawn.
	def getEdgeThickness(self):
		return self.edgeThickness
	
	## Returns whether edges should be anti-aliased or not.
	def getEdgeAA(self):
		return self.edgeAA
	
	## Returns what color edges should be.
	def getEdgeColor(self):
		return self.edgeColor
	
	def getVertSize(self):
		return self.vertSize
	
	def getVertThickness(self):
		return self.vertThickness
	
	def getVertColor(self):
		return self.vertColor
	
	def getSelColor(self):
		return self.selColor
	
	def getModColor(self):
		return self.modColor
	
	def getBgColor(self):
		return self.bgColor
	
	def getWindowEdgeColor(self):
		return self.windowEdgeColor
	
	def getWindowBgColor(self):
		return self.windowBgColor
	
	def getTextColor(self):
		return self.textColor
	
	def getFieldColor(self):
		return self.fieldColor
	
	def getWidth(self):
		return self.x
	
	def getHeight(self):
		return self.y
	
	def setWidth(self,width):
		self.x = width
	
	def setHeight(self,height):
		self.y = height

## Base class for bones.
#
#  This is a basic bone with no starting restrictions on rotation or size.
class Bone(object):
	## Constructor
	#
	#  @param pos The position of the anchor for this bone
	#  @param rot The initial rotation for this bone.
	def __init__(self,rot,size,pos=None):
		self.pos = pos
		self.parentRot = 0
		self.rot = rot					#Rotation in radians
		self.size = size				#Length of Armature in pixels
		self.rotLimit = [None,None]		#[minRot,maxRot]
		self.sizeLimit = [None,None]
		self.ID = nextID()
		
		self.keyframes = {}
		
		self.children = []
		if self.pos!=None:
			self.calcEnd()
	
	def addRotKeyframe(self,frame):
		if self.keyframes.has_key(frame):
			self.keyframes[frame].addRotation(self.getRot())
		else:
			self.keyframes[frame] = keyframe(frame)
			self.keyframes[frame].addRotation(self.getRot())
	
	def addScaleKeyframe(self,frame):
		if self.keyframes.has_key(frame):
			self.keyframes[frame].addScale(self.getSize())
		else:
			self.keyframes[frame] = keyframe(frame)
			self.keyframes[frame].addScale(self.getSize())
	
	def transform(self,frame,interpolate=False):
		if self.keyframes.has_key(frame):
				rot = self.keyframes[frame].getRotation()
				size = self.keyframes[frame].getScale()
				if rot != None:
					self.rot = rot
				if size != None:
					self.size = size
		elif interpolate:
			keys = self.keyframes.keys()
			keys.sort()
			for i in xrange(len(keys)-1):
				if keys[i]<frame<keys[i+1]:
					startFrame = i
					break
			else:
				for child in self.children:
					child.transform(frame,interpolate)
				return
			#rotate
			startRot = self.keyframes[keys[startFrame]].getRotation()
			endRot = self.keyframes[keys[startFrame+1]].getRotation()
			self.rot = startRot + (endRot-startRot)*(float(frame-keys[startFrame])/(keys[startFrame+1]-keys[startFrame]))
		self.calcEnd()
		for child in self.children:
			child.transform(frame,interpolate)
	
	def getID(self):
		return self.ID
	
	def getPos(self):
		return self.pos
	
	def getRot(self):
		return self.rot
	
	def getSize(self):
		return self.size
	
	def rotate(self,amt):
		self.rot+=amt
		self.calcEnd()
	
	def scale(self,amt):
		self.size*=amt
		self.calcEnd()
	
	def move(self,amt):
		if self.pos!=None:
			self.pos[0]+=amt[0]
			self.pos[1]+=amt[1]
			self.calcEnd()
	
	def setRot(self,rot):
		self.rot=rot-self.parentRot
		self.calcEnd()
	
	def setSize(self,size):
		self.size=size
		self.calcEnd()
	
	def setPos(self,pos):
		self.pos = pos
		self.calcEnd()
	
	def addChild(self,child):
		self.children.append(child)
	
	def delete(self,child):
		for item in self.children:
			if item == child:
				self.children.remove(child)
			else:
				item.delete(child)
	
	def calcEnd(self):
		self.endX = int(self.pos[0]+(math.cos(self.parentRot+self.rot)*self.size))
		self.endY = int(self.pos[1]+(math.sin(self.parentRot+self.rot)*self.size))
	
	## Checks if this bone was clicked on
	#
	#  Returns a reference to self
	#  Maybe will return True for if a vertice was selected or False if an edge was?
	def click(self,pos,tolerance):
		#Check vertex first:
		if (pos[0]>self.endX-tolerance) and (pos[0]<self.endX+tolerance):
			if (pos[1]>self.endY-tolerance) and (pos[1]<self.endY+tolerance):
				#return [self,True]
				return self
		##if edge detection were to be implemented it would be like this:
		#dxm = pos[0] - self.pos[0]
		#dym = pos[1] - self.pos[1]
		#dxl = self.endX - self.pos[0]
		#dyl = self.endY - self.pos[1]
		#if (dxm*dyl)-(dym*dxl) == 0:
		#Then there was a click.
		#This uses the cross product of two vectors.
		for child in self.children:
			sel = child.click(pos,tolerance)
			if sel != None:
				return sel
		return None
	
	def draw(self,screen,pos=None,rot=None):
		if pos==None and self.pos==None:
			print "Bone error!!"
			return
		elif self.pos==None:
			self.pos=pos
			self.calcEnd()
		elif pos!=None and self.pos!=pos:
			self.pos=pos
			self.calcEnd()
		if rot!=None:
			self.parentRot=rot
			self.calcEnd()
		
		#Draw edge first:
		if screen.getEdgeAA():
			pygame.draw.aaline(screen.getScreen(),screen.getEdgeColor(),self.pos,[self.endX,self.endY],True)
		else:
			pygame.draw.line(screen.getScreen(),screen.getEdgeColor(),self.pos,[self.endX,self.endY],screen.getEdgeThickness())
		
		pygame.draw.circle(screen.getScreen(),screen.getVertColor(),[self.endX,self.endY],screen.getVertSize(),screen.getVertThickness())
		
		for child in self.children:
			child.draw(screen,[self.endX,self.endY],self.parentRot+self.rot)

class keyframe(object):
	def __init__(self,frame):
		self.frame = frame
		self.rotation = None
		self.scale = None
	
	def getFrame(self):
		return self.frame
	
	def getRotation(self):
		return self.rotation
	
	def getScale(self):
		return self.scale
	
	def addRotation(self,value):
		self.rotation=value
	
	def addScale(self,value):
		self.scale=value
	
	def remRotation(self):
		self.rotation=None
	
	def remScale(self):
		self.scale=None

class image(object):
	def __init__(self,img,pos,size=1,alpha=255):
		self.sprite = img
		self.pos = pos
		self.size = size
		self.alpha = alpha
		self.visible = True
	
	def getSprite(self):
		return pygame.transform.scale(self.sprite,(self.sprite.get_width()*self.size,self.sprite.get_height()*self.size))
	
	def getPos(self):
		return self.pos
	
	def setPos(self,pos):
		self.pos = pos
	
	def getSize(self):
		return self.size
	
	def setSize(self,size):
		self.size = size
	
	def getAlpha(self):
		return self.alpha
	
	def setAlpha(self,alpha):
		self.alpha = alpha
	
	def isVisible(self):
		return self.visible
	
	def toggleVisiblity(self):
		self.visible = not self.visible

pygame.init()

root = Bone(0,100,pos=[150,150])
root.addChild(Bone(math.radians(45),50))
screen = Screen(640,480)
timeline = Timeline(screen,True)
menu = Menu(screen)
info = Info(screen,timeline,menu)
clock = pygame.time.Clock()

font = pygame.font.SysFont("DejaVuSansCondensed.ttf",16)

selected = None
rotate = False
scale = False
hybrid = False
move = False
prevRot = None
prevScale = None
prev = None
amt = 0

refImage = None
refImageShown = True

while True:
	if not timeline.getPlaying():
		clock.tick(60)
	else:
		timeline.play(clock)
		root.transform(timeline.getFrame(),timeline.getInterpolate())
	
	screen.fill(screen.getBgColor())
	
	if refImage != None and refImage.isVisible():
		screen.blit(refImage.getSprite(),refImage.getPos())
	
	if rotate:
		selected.rotate(amt)
	elif scale:
		selected.scale(amt)
	elif move:
		root.move(amt)
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		elif event.type == KEYDOWN:
			if event.key == K_SPACE:
				#screen.edgeAA = not screen.edgeAA
				timeline.togglePlaying()
				selected = None
			elif event.key == K_a:
				if rotate:
					selected.addRotKeyframe(timeline.getFrame())
					timeline.addKeyframe()
					rotate = False
				elif scale:
					selected.addScaleKeyframe(timeline.getFrame())
					timeline.addKeyframe()
					scale = False
			elif event.key == K_r:
				if selected != None and rotate == False and scale == False and move == False:
					rotate = True
					amt = 0
					prevRot = selected.getRot()
				else:
					rotate = False
			elif event.key == K_s:
				if selected != None and scale == False and rotate == False and move == False:
					scale = True
					amt = 1
					prevScale = selected.getSize()
				else:
					scale = False
			elif event.key == K_g:
				if not move and selected != None and not scale and not rotate:
						prev = root.getPos()
						move = True
						amt = [0,0]
				else:
					move = False
			elif event.key == K_ESCAPE:
				if rotate:
					rotate = False
					selected.setRot(prevRot)
				elif scale:
					scale = False
					selected.setSize(prevScale)
				elif hybrid:
					hybrid = False
					selected.setRot(prevRot)
					selected.setSize(prevScale)
				elif move:
					move = False
					root.setPos(prev)
			elif event.key == K_RETURN:
				if rotate:
					rotate = False
				elif scale:
					scale = False
				elif hybrid:
					hybrid = False
				elif move:
					move = False
			elif event.key == K_UP:
				if rotate:
					amt = -0.01
				elif scale:
					amt = 1.01
				elif move:
					amt[1]=-1
			elif event.key == K_DOWN:
				if rotate:
					amt = 0.01
				elif scale:
					amt = .99
				elif move:
					amt[1]=1
			elif event.key == K_RIGHT:
				if rotate:
					amt = 0.01
				elif scale:
					amt = 1.01
				elif hybrid:
					pass
				elif move:
					amt[0]=1
				else:
					timeline.nextFrame()
					root.transform(timeline.getFrame(),timeline.getInterpolate())
			elif event.key == K_LEFT:
				if rotate:
					amt = -0.01
				elif scale:
					amt = .99
				elif hybrid:
					pass
				elif move:
					amt[0]=-1
				else:
					timeline.prevFrame()
					root.transform(timeline.getFrame(),timeline.getInterpolate())
			elif event.key == K_e:
				if selected != None:
					temp = Bone(0,50)
					selected.addChild(temp)
					selected = temp
			elif event.key == K_BACKSPACE or event.key == K_DELETE:
				if selected != None:
					root.delete(selected)
					selected = None
		elif event.type == KEYUP:
			if event.key == K_UP or event.key == K_DOWN:
				if rotate:
					amt = 0
				elif scale:
					amt = 1
				elif move:
					amt[1] = 0
			elif event.key == K_RIGHT or event.key == K_LEFT:
				if rotate:
					amt = 0
				elif scale:
					amt = 1
				elif move:
					amt[0] = 0
		
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				if event.pos[1] > timeline.getTop():
					pass
				else:
					if not rotate and not scale and not move:
						if selected != None:
							if not menu.click(event.pos):
								prevSel = selected
								selected = root.click(event.pos,4)
								if selected == prevSel:
									hybrid = True
									prevRot = selected.getRot()
									prevScale = selected.getSize()
						elif info.getRefImageMove():
							info.setRefImageMove(False)
						else:
							if not menu.click(event.pos) and not info.click(event.pos):
								selected = root.click(event.pos,4)
		elif event.type == MOUSEBUTTONUP:
			if event.button == 1:
				if hybrid:
					hybrid = False
		elif event.type == MOUSEMOTION:
			if event.buttons[0]:
				if scale:
					x=event.pos[0]-selected.getPos()[0]
					y=event.pos[1]-selected.getPos()[1]
					selected.setSize(math.sqrt(x**2+y**2))
				elif rotate:
					x=event.pos[0]-selected.getPos()[0]
					y=event.pos[1]-selected.getPos()[1]
					if x!=0:
						if x>=0:
							selected.setRot(math.atan(float(y)/x))
						else:
							selected.setRot(math.atan(float(y)/x)+(math.pi))
				elif hybrid:
					x=event.pos[0]-selected.getPos()[0]
					y=event.pos[1]-selected.getPos()[1]
					selected.setSize(math.sqrt(x**2+y**2))
					if x!=0:
						if x>=0:
							selected.setRot(math.atan(float(y)/x))
						else:
							selected.setRot(math.atan(float(y)/x)+(math.pi))
				elif move:
					root.setPos(list(event.pos))
			if info.getRefImageMove():
				refImage.setPos(event.pos)
	
	root.draw(screen)
	
	if selected != None:
		#if selected[1]:
		if not rotate and not scale and not hybrid and not move:
			pygame.draw.circle(screen.getScreen(),screen.getSelColor(),[selected.endX,selected.endY],screen.getVertSize(),screen.getVertThickness())
		else:
			pygame.draw.circle(screen.getScreen(),screen.getModColor(),[selected.endX,selected.endY],screen.getVertSize(),screen.getVertThickness())
	
	timeline.draw(screen)
	info.draw(screen,selected)
	menu.draw(screen)
	
	screen.update()
