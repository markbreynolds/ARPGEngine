## @package gui
#  Documentation for the Graphical User Interface Module.
#
#  This module contains the code related GUIs and overlays.
#
##  Goals: V 0.1.0a - Done
#    -# Armor Tab - Done
#      - Display Gold - Done
#      - Show Current Equipment - Done
#      - Show Stats with equipment bonuses - Done
#    -# Party Tab - Done
#      - Make Icon - Done
#      - Character Sheet - Done
#         - View Stat Info - Done
#         - View Character Status Effects - Done
#      - Switch Characters - Done
#      - Show Active Combat Characters - Done
#    -# Migrate Character Creation - Done
#
## <b>Goals: V 0.2.0a</b>
#
#    -# Inventory Tab - Done
#      - Make Items Usable - Done
#      - When an equipable is selected, show stat differences between current. - Done
#    -# Party Tab - Done
#      - View Abilities - Done
#      - Level Up - Done
#    -# Pause/Main %Menu - Done
#      - Pause - Done
#      - Overlay Main %Menu - Done
#    -# Shops - Done
#      - Buy - Done
#      - Sell - Done
#
"""
## Goals: V 0.3.0a
#
#    -# Map Tab
#      - World Map
#      - <b>Show Current Position</b>
#      - <b>Local Map</b>
#        - <b>Dynamic for Current Room</b>
#    -# Quest Tab
#      - View Quest Details
#      - Abandon Sub-Quests
#      - View Completed Quests

"""

import pygame
from pygame.locals import *

import errors
import config

## Standard default font, @todo Check for legal issues with distribution of fonts.
font = pygame.font.Font(config.AssetPath+"Fonts/visitor1.ttf",10)

## Font used for titles, @todo Check for legal issues with distribution of fonts.
titleFont = pygame.font.Font(config.AssetPath+"Fonts/visitor1.ttf",12)

## Bold default font, @todo Check for legal issues with distribution of fonts.
boldFont = pygame.font.Font(config.AssetPath+"Fonts/visitor1.ttf",10)
boldFont.set_italic(True)

## A class that contains all icons used throughout GUIs and the game.
#
#  Icons are stored this way to allow universal access from anywhere to the same icons giving a more put together and cohesive look.
class Icons():
	#  @todo Fix BootArmor Icon.
	#  @todo Fix HeadArmor Icon.
	#  @todo Maybe fix Gold Icon?
	cont = None
	cursor = None
	cursorBlink = None
	cursorTab = None
	cursorTabBlink = None
	cursorChar = None
	cursorCharBlink = None
	iconBG = None
	iconBGE = None
	iconBGSmall = None
	lock = None

	headArmor = None
	bodyArmor = None
	legsArmor = None
	bootArmor = None
	arm1Armor = None
	arm2Armor = None

	gold = None

	inventory = None
	armor = None
	party = None
	globe = None
	quests = None

	warrior = None
	warriorSmall = None
	archer = None
	archerSmall = None
	mage = None
	mageSmall = None

	rightArrow = None
	leftArrow = None
	upArrow = None
	downArrow = None
	circ = None

	##  Sets the Icons variable to an instance of this class.
	@staticmethod
	def load():
		errors.debug("Loading Icons")
		Icons.cont = pygame.image.load(config.AssetPath+"Icons/Cont.png").convert_alpha()
		Icons.cursor = pygame.image.load(config.AssetPath+"Icons/Cursor.png").convert_alpha()
		Icons.cursorBlink = pygame.image.load(config.AssetPath+"Icons/CursorBlink.png").convert_alpha()
		Icons.cursorTab = pygame.image.load(config.AssetPath+"Icons/CursorTab.png").convert_alpha()
		Icons.cursorTabBlink = pygame.image.load(config.AssetPath+"Icons/CursorTabBlink.png").convert_alpha()
		Icons.cursorChar = pygame.image.load(config.AssetPath+"Icons/CursorChar.png").convert_alpha()
		Icons.cursorCharBlink = pygame.image.load(config.AssetPath+"Icons/CursorCharBlink.png").convert_alpha()
		Icons.cursor.fill(config.ColorSel,special_flags=BLEND_RGBA_MULT)
		Icons.cursorBlink.fill(config.ColorSel,special_flags=BLEND_RGBA_MULT)
		Icons.cursorTab.fill(config.ColorSel,special_flags=BLEND_RGBA_MULT)
		Icons.cursorTabBlink.fill(config.ColorSel,special_flags=BLEND_RGBA_MULT)
		Icons.cursorChar.fill(config.ColorSel,special_flags=BLEND_RGBA_MULT)
		Icons.cursorCharBlink.fill(config.ColorSel,special_flags=BLEND_RGBA_MULT)
		Icons.iconBG = pygame.image.load(config.AssetPath+"Icons/IconBG.png").convert()
		Icons.iconBGE = pygame.image.load(config.AssetPath+"Icons/IconBG.png").convert()
		Icons.iconBGE.fill([32,255,32],special_flags=BLEND_RGBA_MULT)
		Icons.iconBGSmall = pygame.image.load(config.AssetPath+"Icons/IconBGSmall.png").convert()
		Icons.lock = pygame.image.load(config.AssetPath+"Icons/Locked.png").convert_alpha()

		Icons.headArmor = pygame.image.load(config.AssetPath+"Icons/HeadArmor.png").convert_alpha()
		Icons.bodyArmor = pygame.image.load(config.AssetPath+"Icons/BodyArmor.png").convert_alpha()
		Icons.legsArmor = pygame.image.load(config.AssetPath+"Icons/LegsArmor.png").convert_alpha()
		Icons.bootArmor = pygame.image.load(config.AssetPath+"Icons/BootArmor.png").convert_alpha()
		Icons.arm1Armor = pygame.image.load(config.AssetPath+"Icons/Arm1Armor.png").convert_alpha()
		Icons.arm2Armor = pygame.image.load(config.AssetPath+"Icons/Arm2Armor.png").convert_alpha()

		Icons.gold = pygame.image.load(config.AssetPath+"Icons/Gold.png").convert_alpha()

		Icons.inventory = pygame.image.load(config.AssetPath+"Icons/Inven.png").convert_alpha()
		Icons.armor = pygame.image.load(config.AssetPath+"Icons/Armor.png").convert_alpha()
		Icons.party = pygame.image.load(config.AssetPath+"Icons/Party.png").convert_alpha()
		Icons.globe = pygame.image.load(config.AssetPath+"Icons/Map.png").convert_alpha()
		Icons.quests = pygame.image.load(config.AssetPath+"Icons/Quests.png").convert_alpha()

		Icons.warrior = pygame.image.load(config.AssetPath+"Icons/Warrior.png").convert()
		Icons.warriorSmall = pygame.image.load(config.AssetPath+"Icons/WarriorSmall.png").convert()
		Icons.archer = pygame.image.load(config.AssetPath+"Icons/Archer.png").convert()
		Icons.archerSmall = pygame.image.load(config.AssetPath+"Icons/ArcherSmall.png").convert()
		Icons.mage = pygame.image.load(config.AssetPath+"Icons/Mage?.png").convert()
		Icons.mageSmall = pygame.image.load(config.AssetPath+"Icons/MageSmall?.png").convert()

		Icons.rightArrow = pygame.image.load(config.AssetPath+"Icons/RightArrow.png").convert_alpha()
		Icons.leftArrow = pygame.transform.flip(Icons.rightArrow,True,False)
		Icons.upArrow = pygame.image.load(config.AssetPath+"Icons/UpArrow.png").convert_alpha()
		Icons.downArrow = pygame.transform.flip(Icons.upArrow,False,True)
		Icons.circ = pygame.image.load(config.AssetPath+"Icons/Circ.png").convert_alpha()

## Helpful for scrolling text.
#
#  Draws the text at an offset and then crops it in order to make it appear to scroll.
#  @param text Text that is to be scrolled.
#  @param size How many pixels the @c text needs to fit in.
#  @param amount How many pixels to scroll for this iteration.
#  @param color Text color.
def scrollText(text,size,amount,color=config.ColorFont):
	cropped=pygame.Surface((size,font.size(text)[1]),SRCALPHA)
	if font.size(text)[0]>size:
		if amount<0:
			cropped.blit(font.render(text,False,color),[0,0])
		elif amount>=font.size(text)[0]-size:
			cropped.blit(font.render(text,False,color),[-(font.size(text)[0]-size),0])
		else:
			cropped.blit(font.render(text,False,color),[-amount,0])
	else:
		cropped.blit(font.render(text,False,color),[0,0])
	return cropped

## Base class for menu objects.
#
#  Attempts to define some basic functions and variables that are common among menus.
class Menu(object):

	## Constructor.
	#
	#  @param bottom How many items down there are.
	#  @param right How many items to the right there are.
	def __init__(self,bottom,right):
		self.pos=[0,0]

		# Creates delay between each time the cursor is moved when a direction is being held.
		self.move=0.0
		self.bottom=bottom
		self.right=right
		self.menu=0
		self.close=False
		self.value=None

	## Returns whether or not the menu has been closed.
	def closed(self):
		return self.close

	## Returns the "value" of the menu.
	#
	#  This is useful in cases where the player needs to make a decision, and we need to know what that decision is after it is made.
	def getValue(self):
		return self.value

	## Move the cursor up.
	def SelUp(self):
		if self.move>=.25:
			if self.pos[1]==0:
				self.pos[1]=self.bottom
			else:
				self.pos[1]-=1
			self.move=0.0

	## Move the cursor down.
	def SelDown(self):
		if self.move>=.25:
			if self.pos[1]>=self.bottom:
				self.pos[1]=0
			else:
				self.pos[1]+=1
			self.move=0.0

	## Move the cursor left.
	def SelLeft(self):
		if self.move>=.25:
			if self.pos[0]==0:
				self.pos[0]=self.right
			else:
				self.pos[0]-=1
			self.move=0.0

	## Move the cursor right.
	def SelRight(self):
		if self.move>=.25:
			if self.pos[0]>=self.right:
				self.pos[0]=0
			else:
				self.pos[0]+=1
			self.move=0.0

	## Selects the current item.
	#
	#  This function is also responsible for dealing with changing to submenus, as well as setting appropriate return values in @c value.
	def Select(self):
		return

	## Moves up a level in submenus or else closes the menu.
	def Cancel(self):
		if self.menu==0:
			self.close=True
		else:
			self.menu-=1

	## Draws all components of the window.
	#
	#  This includes drawing the window itself, cursor, text, and all icons.
	#  @param screen An object representing the screen, either a pygame.Surface or a ScaledScreen.
	def draw(self,screen):
		return

	## Updates the window.
	def update(self,screen,tick):
		self.move+=tick
		self.draw(screen)

## Base class for HUD objects.
#
#  Attempts to define some basic functions and variables that are common among HUDs.
class Hud(object):

	## Constructor
	#
	#  @param pos The positiont the window should be drawn at.
	#  @param data A dictionary of data to be displayed using the format, key+value().  i.e. `data = {"Money: ":getMoney}`, where getMoney is a fuction with no arguments or one argument @c self.
	#  @param width The width of this window. If set to none, will auto-detect using the starting values of data[key]().
	#  @param height The height of this window. If set to none, will auto-detect using the starting values of data[key]().
	def __init__(self,pos,data={},width=None,height=None):
		self.data = data
		self.x = pos[0]
		self.y = pos[1]

		self.autoSize()
		if width != None:
			self.width = width
		if height != None:
			self.height = height

	## Adds additional data to the HUD.
	#
	#  @note This will resize your window undoing any manual sizing.
	def addData(self,key,value):
		self.data[key]=value
		self.autoSize()

	## Auto resizes the window to fit contents.
	def autoSize(self):
		tempData = []
		for key in self.data.keys():
			tempData.append(key+str(self.data[key]()))

		self.width=font.size(max(tempData,key=len))[0]+6
		self.height=len(tempData)*9+6

	def draw(self,screen):
		tempData = []
		for key in self.data.keys():
			tempData.append(key+str(self.data[key]()))
		screen.fill(config.Color,(self.x,self.y,self.width,self.height))
		y = self.y+3
		for data in tempData:
			screen.blit(font.render(data,True,config.ColorFont),(self.x+3,y))
			y+=9

	## Updates the window.
	def update(self,screen):
		self.draw(screen)

## Main %Menu Class
#
#  Contains information for the main menu as well as function for drawing it, and its submenus.
class MainMenu(Menu):

	## Constructor.
	def __init__(self):
		Menu.__init__(self,3,1)

	## Selects the current item.
	def Select(self):
		if self.menu == 0:
			if self.pos[1] == 0:
				self.menu=1
				self.bottom=2
			elif self.pos[1]==1:
				return
			elif self.pos[1]==2:
				return
			elif self.pos[1]==3:
				self.close=True
				self.value="Exit"
		if self.menu == 1:
			if self.pos[1] == 0:
				self.close=True
				self.value="New Single"
			elif self.pos[1]==1:
				self.close=True
				self.value="Load Single"
			elif self.pos[1]==2:
				self.menu=0
				self.pos[1]=0
				self.bottom=3

	## Moves up a level in submenus or else closes the menu.
	def Cancel(self):
		if self.menu == 0:
			self.close=True
			self.value="Exit"
		elif self.menu==1:
			self.menu=0
			self.pos[1]=0
			self.bottom=3

	## Draws all components of the screen.
	#
	#  @param screen An object representing the screen, either a pygame.Surface or a ScaledScreen.
	def draw(self,screen):
		screen.fill(config.ColorDark,[114,126,97,64])
		screen.fill(config.Color,[115,127,95,62])
		if self.menu == 0:
			self.drawMain(screen)
		elif self.menu==1:
			self.drawSingle(screen)

	## Draws the main menu on the screen.
	#
	#  @param screen An object representing the screen, either a pygame.Surface or a ScaledScreen.
	def drawMain(self,screen):
		if self.pos[1] == 0:
			screen.blit(titleFont.render("Single Player",False,config.ColorSel),(120,130))
		else:
			screen.blit(titleFont.render("Single Player",False,config.ColorFont),(120,130))
		if self.pos[1] == 1:
			screen.blit(titleFont.render("Multiplayer",False,config.ColorSel),(120,144))
		else:
			screen.blit(titleFont.render("Multiplayer",False,config.ColorFont),(120,144))
		if self.pos[1] == 2:
			screen.blit(titleFont.render("Options",False,config.ColorSel),(120,158))
		else:
			screen.blit(titleFont.render("Options",False,config.ColorFont),(120,158))
		if self.pos[1] ==3 :
			screen.blit(titleFont.render("Exit",False,config.ColorSel),(120,172))
		else:
			screen.blit(titleFont.render("Exit",False,config.ColorFont),(120,172))

	## Draws the single player menu on the screen.
	#
	#  @param screen An object representing the screen, either a pygame.Surface or a ScaledScreen.
	def drawSingle(self,screen):
		if self.pos[1] == 0:
			screen.blit(titleFont.render("New Game",False,config.ColorSel),(120,130))
		else:
			screen.blit(titleFont.render("New Game",False,config.ColorFont),(120,130))
		if self.pos[1] == 1:
			screen.blit(titleFont.render("Load Game",False,config.ColorSel),(120,144))
		else:
			screen.blit(titleFont.render("Load Game",False,config.ColorFont),(120,144))
		if self.pos[1] == 2:
			screen.blit(titleFont.render("Back",False,config.ColorSel),(120,158))
		else:
			screen.blit(titleFont.render("Back",False,config.ColorFont),(120,158))

## Dialog Class
#
#  Contains information for displaying and formating dialog.
class Dialog(object):
	## Constructor
	#
	#  @param talking The NPC the player is talking to.
	#  @param player A reference to the current Player.
	#  @param speed How fast the dialog should move.
	def __init__(self,talking,player,speed=1):
		self.talking=talking
		self.player=player
		self.speed=speed
		self.current=talking.getDialog()
		self.action = None
		self.preAction = None

		self.formattedText = []
		self.formattedOptions = []
		self.bold =[]

		for i in range(len(self.current.getText())):
			self.formattedText.append(self.RegEx(self.current.getText()[i]))
		for i in range(len(self.current.getOptions())):
			self.formattedOptions.append(self.RegEx(self.current.getOptions()[i]))

		self.LineWrap()
		self.Format()

		self.x=0
		self.y=0
		self.count=0.0

		self.longest=-1
		self.sel=0

		self.cont=False
		self.options=False
		self.shop=False
		self.sleep=False
		self.trigger=False
		self.quest=False
		self.branch=False
		self.branchDialog=None
		self.preBranchDialog=None

		if self.current.getPreAction()!=None:
			self.action = self.current.getPreAction()
		if self.current.getPreBranch()!=None:
			self.branchDialog = self.current.getPreBranch()

	## Returns "Buy" if the player wants to buy something and "Sell" if the player wants to sell something.
	def getShop(self):
		return self.shop

	## Returns if the player is sleeping.
	def getSleep(self):
		return self.sleep

	## Returns if a trigger has been triggered by dialogue.
	def getTrigger(self):
		return self.trigger

	## Returns if a quest action has occurred.
	def getQuest(self):
		return self.quest

	## Returns if a branch is being attepted.
	def getBranch(self):
		return self.branch

	## Executes a branch when necessary.
	#
	#  @param branch Whether or not the branch should be executed.
	def shouldBranch(self,branch):
		#if branch and self.branchDialog != None:
		if branch:
			self.current = self.branchDialog
			self.branchDialog = None
			self.longest=-1
			self.sel=0
			self.bold=[]
			self.formattedText = []
			self.formattedOptions = []

			self.action = self.preAction
			self.branchDialog = self.preBranchDialog
			self.preAction = None
			self.preBranchDialog = None

			if self.current != None and type(self.current) != str:
				for i in range(len(self.current.getText())):
					self.formattedText.append(self.RegEx(self.current.getText()[i]))
				for i in range(len(self.current.getOptions())):
					self.formattedOptions.append(self.RegEx(self.current.getOptions()[i]))

				if self.current.getPreAction()!=None:
					if self.action==None:
						self.action = self.current.getPreAction()
					else:
						self.preAction = self.current.getPreAction()
				if self.current.getPreBranch()!=None:
					if self.branchDialog==None:
						self.branchDialog = self.current.getPreBranch()
					else:
						self.preBranchDialog = self.c

			self.LineWrap()
			self.Format()
		else:
			self.action = self.preAction
			self.branchDialog = self.preBranchDialog
			self.preAction = None
			self.preBranchDialog = None
#		elif branch:
#			errors.warning("Dialog is missing branch.")

	## A "Regular Expression"-like function that replaces variables in text with their actual value at runtime.
	#
	#  Currently only replaces "$PNAME" with the players name.
	#
	#  @param text Text to be replaced
	def RegEx(self,text):
		text = text.replace("$PNAME",self.player.getName())
		return text

	## Formats text to make it bold or apply other effects.
	#
	#  Currently supports:
	#  +Bold @c <b>
	def Format(self):
		for i in range(len(self.formattedText)):
			if self.formattedText[i].find("<b>")!=-1:
				self.bold.append([self.formattedText[i].find("<b>"),self.formattedText[i].find("</b>")-3,i])
				self.formattedText[i] = self.formattedText[i].replace("<b>","")
				self.formattedText[i] = self.formattedText[i].replace("</b>","")

	## Breaks up text into multiple lines.
	def LineWrap(self):
		append=""
		i=0
		while i < len(self.formattedText):
			self.formattedText[i]=append+self.formattedText[i]
			if font.size(self.formattedText[i])[0]<=304:
				append=""
				i+=1
				continue
			words = self.formattedText[i].split(" ")
			for j in range(len(words)-1):
				if font.size(str(" ").join(words[:j]))[0]<=304 and font.size(str(" ").join(words[:j+1]))[0]>304:
					self.formattedText[i]=str(" ").join(words[:j])
					if i != len(self.formattedText)-1:
						append=str(" ").join(words[j:])+" "
					else:
						append=""
						self.formattedText.append(str(" ").join(words[j:]))
					break
			i+=1
		del i

	## Moves the cursor up one item.
	def SelUp(self):
		if self.count >= .25 and self.options:
			if self.sel <=0:
				self.sel = len(self.current.getOptions())-1
			else:
				self.sel-=1
			self.count=0

	## Moves the cursor down one item.
	def SelDown(self):
		if self.count >= .25 and self.options:
			if self.sel >= len(self.current.getOptions())-1:
				self.sel=0
			else:
				self.sel+=1
			self.count=0

	## Either select an option or continue through the dialog.
	#
	#  Which of these two things will happens just depends on the context, this allows pressing the "Action" button
	#  to call the same function in a dialog regardless of context.
	def Cont(self):
		if not self.options:
			if self.y>=len(self.formattedText):
				if self.current.getOptions()!=[]:
					self.options=True
				else:
					self.action = self.current.getLinks()[0]
					self.branchDialog = self.current.getBranches()[0]
					self.current = None
			elif (self.y+1)%5==0 and self.x>=len(self.formattedText[self.y]):
				self.y+=1
				self.x=0
				self.count=0.0
			else:
				self.x+=10
				self.count=0.0
		else:
			self.action = self.current.getActions()[self.sel]
			self.branchDialog = self.current.getBranches()[self.sel]
			self.current = self.current.getLinks()[self.sel]
			self.options=False
			self.x=0
			self.y=0
			self.count=0.0
			self.longest=-1
			self.sel=0
			self.bold=[]
			self.formattedText = []
			self.formattedOptions = []

			if self.current != None and type(self.current) != str:
				for i in range(len(self.current.getText())):
					self.formattedText.append(self.RegEx(self.current.getText()[i]))
				for i in range(len(self.current.getOptions())):
					self.formattedOptions.append(self.RegEx(self.current.getOptions()[i]))

				if self.current.getPreAction()!=None:
					if self.action==None:
						self.action = self.current.getPreAction()
					else:
						self.preAction = self.current.getPreAction()
				if self.current.getPreBranch()!=None:
					if self.branchDialog==None:
						self.branchDialog = self.current.getPreBranch()
					else:
						self.preBranchDialog = self.current.getPreBranch()

			self.LineWrap()
			self.Format()

	## Draws the dialog text on the screen.
	#
	#  @param screen An object representing the screen, either a pygame.Surface or a ScaledScreen.
	def convoText(self,screen):	#Displays text for talking
		if self.count >=.05 and self.y<len(self.formattedText) and ((self.y+1)%5!=0 or self.x<len(self.formattedText[self.y])):
			self.x+=1
			if self.x>=len(self.formattedText[self.y])-1 and (self.y+1)%5!=0:
				self.x-=len(self.formattedText[self.y])-1
				self.y+=1
			self.count -=.05

		if self.y<len(self.formattedText) and self.x<len(self.formattedText[self.y]):
			screen.fill(config.ColorDark,[4,179,312,59])
			screen.fill(config.Color,[5,180,310,57])
			if self.talking.getIcon() != None:
				if self.talking.getName()!=None:
					pass
			else:
				if self.talking.getName()!=None:
					screen.fill(config.ColorDark,[4,164,10+titleFont.size(self.talking.getName())[0],15])
					screen.fill(config.Color,[5,165,8+titleFont.size(self.talking.getName())[0],13])
					screen.blit(titleFont.render(self.talking.getName()+":",False,config.ColorFont),[8,166])

			if self.bold == []:	#if not bold...
				for i in range(self.y/5*5,self.y):
					screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
				screen.blit(font.render(self.formattedText[self.y][:self.x],False,config.ColorFont),[8,181+((self.y%5)*12)])
			else:				#if bold..
				for i in range(self.y/5*5,self.y):
					for j in self.bold:
						if i == j[2]:
							screen.blit(font.render(self.formattedText[i][0:j[0]],False,config.ColorFont),[8,181+((i%5)*12)])
							screen.blit(font.render(self.formattedText[i][j[0]:j[1]],False,config.ColorBold),[8+font.size(self.formattedText[i][0:j[0]])[0],181+((i%5)*12)])
							screen.blit(font.render(self.formattedText[i][j[1]:],False,config.ColorFont),[8+font.size(self.formattedText[i][0:j[1]])[0],181+((i%5)*12)])
							break
					else:
						screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
				for j in self.bold:
					if self.y==j[2]:
						if self.x>j[0]:
							screen.blit(font.render(self.formattedText[self.y][0:j[0]],False,config.ColorFont),[8,181+((self.y%5)*12)])
							screen.blit(font.render(self.formattedText[self.y][j[0]:min(j[1],self.x)],False,config.ColorBold),[8+font.size(self.formattedText[self.y][0:j[0]])[0],181+((self.y%5)*12)])
							screen.blit(font.render(self.formattedText[self.y][j[1]:self.x],False,config.ColorFont),[8+font.size(self.formattedText[self.y][0:min(j[1],self.x)])[0],181+((self.y%5)*12)])
							break
				else:
					screen.blit(font.render(self.formattedText[self.y][:self.x],False,config.ColorFont),[8,181+((self.y%5)*12)])
		else:
			screen.fill(config.ColorDark,[4,179,312,59])
			screen.fill(config.Color,[5,180,310,57])
			if self.talking.getIcon() != None:
				if self.talking.getName()!=None:
					pass
			else:
				if self.talking.getName()!=None:
					screen.fill(config.ColorDark,[4,164,10+titleFont.size(self.talking.getName())[0],15])
					screen.fill(config.Color,[5,165,8+titleFont.size(self.talking.getName())[0],13])
					screen.blit(titleFont.render(self.talking.getName()+":",False,config.ColorFont),[8,166])
			if self.bold == []:	#if not bolded...
				if self.y-5>=0:
					if (self.y+1)%5==0:
						if self.y!=len(self.formattedText):
							for i in range(self.y/5*5,self.y+1):
								screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
						else:	#Deals with case when the text ends on the fourth line
							for i in range(self.y/5*5,self.y):
								screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
					else:
						for i in range(self.y/5*5,self.y):
							screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
				else:
					if (self.y+1)%5==0:
						if self.y!=len(self.formattedText):
							for i in range(0,self.y+1):
								screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
						else:	#Deals with case when the text ends on the fourth line
							for i in range(0,self.y):
								screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])

					else:
						for i in range(0,self.y):
							screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
			else:	#if bolded...
				if self.y-5>=0:
					if (self.y+1)%5==0:
						if self.y!=len(self.formattedText):
							for i in range(self.y/5*5,self.y+1):
								for j in self.bold:
									if i == j[2]:
										screen.blit(font.render(self.formattedText[i][0:j[0]],False,config.ColorFont),[8,181+((i%5)*12)])
										screen.blit(font.render(self.formattedText[i][j[0]:j[1]],False,config.ColorBold),[8+font.size(self.formattedText[i][0:j[0]])[0],181+((i%5)*12)])
										screen.blit(font.render(self.formattedText[i][j[1]:],False,config.ColorFont),[8+font.size(self.formattedText[i][0:j[1]])[0],181+((i%5)*12)])
									else:
										screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
						else:	#Deals with case when the text ends on the fourth line
							for i in range(self.y/5*5,self.y):
								for j in self.bold:
									if i == j[2]:
										screen.blit(font.render(self.formattedText[i][0:j[0]],False,config.ColorFont),[8,181+((i%5)*12)])
										screen.blit(font.render(self.formattedText[i][j[0]:j[1]],False,config.ColorBold),[8+font.size(self.formattedText[i][0:j[0]])[0],181+((i%5)*12)])
										screen.blit(font.render(self.formattedText[i][j[1]:],False,config.ColorFont),[8+font.size(self.formattedText[i][0:j[1]])[0],181+((i%5)*12)])
									else:
										screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
					else:
						for i in range(self.y/5*5,self.y):
							for j in self.bold:
								if i == j[2]:
									screen.blit(font.render(self.formattedText[i][0:j[0]],False,config.ColorFont),[8,181+((i%5)*12)])
									screen.blit(font.render(self.formattedText[i][j[0]:j[1]],False,config.ColorBold),[8+font.size(self.formattedText[i][0:j[0]])[0],181+((i%5)*12)])
									screen.blit(font.render(self.formattedText[i][j[1]:],False,config.ColorFont),[8+font.size(self.formattedText[i][0:j[1]])[0],181+((i%5)*12)])
								else:
									screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
				else:
					if (self.y+1)%5==0:
						if self.y!=len(self.formattedText):
							for i in range(0,self.y+1):
								for j in self.bold:
									if i == j[2]:
										screen.blit(font.render(self.formattedText[i][0:j[0]],False,config.ColorFont),[8,181+((i%5)*12)])
										screen.blit(font.render(self.formattedText[i][j[0]:j[1]],False,config.ColorBold),[8+font.size(self.formattedText[i][0:j[0]])[0],181+((i%5)*12)])
										screen.blit(font.render(self.formattedText[i][j[1]:],False,config.ColorFont),[8+font.size(self.formattedText[i][0:j[1]])[0],181+((i%5)*12)])
									else:
										screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
						else:	#Deals with case when the text ends on the fourth line
							for i in range(0,self.y):
								for j in self.bold:
									if i == j[2]:
										screen.blit(font.render(self.formattedText[i][0:j[0]],False,config.ColorFont),[8,181+((i%5)*12)])
										screen.blit(font.render(self.formattedText[i][j[0]:j[1]],False,config.ColorBold),[8+font.size(self.formattedText[i][0:j[0]])[0],181+((i%5)*12)])
										screen.blit(font.render(self.formattedText[i][j[1]:],False,config.ColorFont),[8+font.size(self.formattedText[i][0:j[1]])[0],181+((i%5)*12)])
									else:
										screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
					else:
						for i in range(0,self.y):
							for j in self.bold:
								if i == j[2]:
									screen.blit(font.render(self.formattedText[i][0:j[0]],False,config.ColorFont),[8,181+((i%5)*12)])
									screen.blit(font.render(self.formattedText[i][j[0]:j[1]],False,config.ColorBold),[8+font.size(self.formattedText[i][0:j[0]])[0],181+((i%5)*12)])
									screen.blit(font.render(self.formattedText[i][j[1]:],False,config.ColorFont),[8+font.size(self.formattedText[i][0:j[1]])[0],181+((i%5)*12)])
								else:
									screen.blit(font.render(self.formattedText[i],False,config.ColorFont),[8,181+((i%5)*12)])
			if not self.options:
				if self.count >=1 and self.y>=len(self.formattedText):
					self.count=0
				screen.blit(Icons.cont,[309,230+int(self.count*2)])

	## Draws the dialog options on the screen.
	#
	#  @param screen An object representing the screen, either a pygame.Surface or a ScaledScreen.
	def convoOptions(self,screen):
		if self.longest==-1:
			for item in self.formattedOptions:
				if font.size(item)[0]>self.longest:
					self.longest=font.size(item)[0]
		screen.fill(config.ColorDark,[311-self.longest,175-(len(self.formattedOptions)*12),self.longest+5,(len(self.formattedOptions)*12)+3])
		screen.fill(config.Color,[312-self.longest,176-(len(self.formattedOptions)*12),self.longest+3,(len(self.formattedOptions)*12)+1])
		for i in range(len(self.current.getOptions())):
			if i == self.sel:
				screen.blit(font.render(self.formattedOptions[i],False,config.ColorSel),[314-font.size(self.formattedOptions[i])[0],(177-len(self.formattedOptions)*12)+12*i])
			else:
				screen.blit(font.render(self.formattedOptions[i],False,config.ColorFont),[314-font.size(self.formattedOptions[i])[0],(177-len(self.formattedOptions)*12)+12*i])

	## Updates the dialog object so that it is drawn properly.
	def update(self,screen,tick):
		if self.action != None:
			if self.action=="Buy":
				self.shop = "Buy"
			elif self.action=="Sell":
				self.shop = "Sell"
			elif self.action=="Sleep":
				self.sleep = True
			elif self.action.startswith("Trigger"):
				self.trigger = self.action.split(" ",1)[1]
			elif self.action.startswith("Quest"):
				self.quest = self.action.split(" ")[1:]
			elif self.action.startswith("Branch"):
				self.branch = self.action.split(" ")[1:]
			else:
				errors.warning("Undefined Action: "+self.action)
			self.action=None
		else:
			self.shop=False
			self.sleep=False
			self.trigger=False
			self.quest=False
			self.branch=False
		if self.current==None:
				return False
		## Old method of actions, deprecated as of 0.2.0a
		elif type(self.current) == str:
			errors.info("Deprecated action style: "+self.current)
			if self.current=="@BUY":
				self.shop = "Buy"
				return False
			elif self.current=="@SELL":
				self.shop = "Sell"
				return False
			elif self.current=="@SLEEP":
				self.sleep = True
				return False
			elif self.current.startswith("@TRIGGER"):
				self.trigger = self.current.split(" ",1)[1]
				return False
			elif self.current.startswith("@QUEST"):
				self.quest = self.current.split(" ")[1:]
				return False
			else:
				errors.warning("Undefined Action: "+self.current)
		self.count+=tick
		self.convoText(screen)
		if self.options:
			self.convoOptions(screen)


class InvenMenu(Menu):
	def __init__(self,player,levelName):
		self.player=player
		self.levelName=levelName

		# Constants:

		## The X position of this window's origin.
		self.winX = 64									#Old = 89
		## The X portion of this window's size.
		self.winSizeX = 192								#Old = 132
		## How many item slots there are in a row.
		self.invenSizeX = (self.winSizeX/30)

		#**********#

		self.pos=[0,0]
		self.tab=0		#0-inventory, 1-Character, 2-Quests, 3-Map
		self.menu=0		#Which sub-menu is open
		self.subPos=0	#Sub-menu cursor position
		self.sel=None	#Selected Item
		self.move=0.0	#time since cursor last moved
		self.blink=0.0	#time since cursor last blinked
		self.size=player.getInventory().getSize()

		self.status=""
		self.statusScroll=0.0
		self.selScroll=0.0

		self.close=False

	def Cancel(self):
		if self.menu==0:
			self.close=True
		elif self.menu==1:
			self.menu=0
		elif self.menu==2:
			self.menu=0
			if self.tab==2:
				self.pos=[0,0]
		elif self.menu==3:
			self.menu=0
		elif self.menu==4:
			if self.tab==2:
				self.menu = 2
			else:
				self.menu=0
		elif self.menu==5:
			self.menu = 2

	def Select(self):
		reset=True
		if self.pos[0]==-1:
			return
		if self.tab==0:		#Inventory
			if len(self.player.getInventory().getItems())-1>=(self.pos[1]*self.invenSizeX)+self.pos[0]:
				item=self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]]
			else:
				item=None
			if self.menu==0:
				if item==None:
					return
				if len(self.player.getInventory().getItems())-1>=(self.pos[1]*self.invenSizeX)+self.pos[0]:
					self.menu=1
					if item.getType()!="Equipment" and item.getUsable()==False:
						self.subPos = 1
						reset = False
			elif self.menu==1:		#Menu
				self.menu=0
				if item==None:
					return
				if self.subPos == 0:
					if item.getType()=="Equipment":
						if item.getEquiped():
							self.player.unequip(item)
						else:
							self.player.equip(item)
					else:
						if item.getTarget():
							self.menu=4
				elif self.subPos == 1:
					self.menu=2
					self.sel=[self.pos[0],self.pos[1]]
				elif self.subPos == 2:
					self.menu=3
			elif self.menu==2:		#Move Item
				src = self.sel[1]*self.invenSizeX + self.sel[0]
				dst = self.pos[1]*self.invenSizeX + self.pos[0]
				self.player.getInventory().move(src,dst)
				self.menu=0
				self.sel=None
			elif self.menu==3:		#Drop Confirm
				if self.subPos==0:	#Confirmed
					self.player.getInventory().remove(item)
				self.menu=0
			elif self.menu==4:		#Use Item Target
				if self.subPos==0:
					if self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]].use(self.player):
						self.player.getInventory().remove(self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]])
				else:
					if self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]].use(self.player.getParty()[self.subPos-1]):
						self.player.getInventory().remove(self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]])
						self.menu=0
					else:
						reset = False
		elif self.tab==2:		#Party
			if self.menu==0 and self.pos[0]!=-1:	#In Party
				if self.pos[1]==0:
					self.sel = self.player
					self.menu=2
				else:
					self.menu = 1
			elif self.menu==1:	#In Menu
				if self.subPos==0:		#To View
					self.sel = self.player.getParty()[self.pos[1]-1]
					self.pos[1]=0
					self.menu=2
				elif self.subPos==1:	#To Move
					self.menu=3
					self.sel = self.pos[1]-1
			elif self.menu==2:	#In Character Sheet
				if self.pos[1]==1:
					if self.sel.getBattleObject().getExp() >= self.sel.getBattleObject().getExpNext():
						self.menu=4
				elif self.pos[1]>=9:
					self.menu=5
			elif self.menu==3:	#In Move
				temp = self.player.getParty()[self.sel]
				self.player.getParty()[self.sel]=self.player.getParty()[self.pos[1]-1]
				self.player.getParty()[self.pos[1]-1] = temp
				self.menu = 0
			elif self.menu==4:	#Level up stat view
				if self.sel.isPlayer():
					if self.player.getSkillLevelUp():
						self.menu = 6
					else:
						self.menu = 2
						self.sel.levelUp()
				else:
					self.menu = 2
					self.sel.levelUp()
			elif self.menu==5:	#Skill Assign
				if self.subPos == 0:
					skill = None
				else:
					skill = self.sel.getJob().getUnlockedSkills()[self.subPos-1]
					if skill.getLevel()<=0:
						return
				if self.pos[1] == 9:
					self.sel.setSkill("S1",skill)
				elif self.pos[1] == 10:
					self.sel.setSkill("S1U",skill)
				elif self.pos[1] == 11:
					self.sel.setSkill("S1R",skill)
				elif self.pos[1] == 12:
					self.sel.setSkill("S1L",skill)
				elif self.pos[1] == 13:
					self.sel.setSkill("S1D",skill)
				self.menu = 2
			elif self.menu==6:	#Level up skill
				self.sel.getJob().getUnlockedSkills()[self.subPos].levelUp()
				self.sel.levelUp()
				self.menu = 2
		if reset:
			self.subPos=0


	def SelUp(self):
		if self.move>=.25:				#Move one space every 1/4 of a second
			self.statusScroll=-30		#Dont Scroll for 1.5 seconds (30/20) See "self.statusScroll+="
			self.selScroll=-30

			if self.pos[0]==-1:
				self.pos[1]=0
				if self.tab==0:
					self.tab=4
				else:
					self.tab-=1
			else:
				if self.tab==0:		#Inventory
					if self.menu==0 or self.menu==2:
						if self.pos[1]==0:
							if self.size==0:
								self.pos[1]=2
							else:
								self.pos[1]=5
						else:
							self.pos[1]-=1
					elif self.menu==1:
						if self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]].getType()!="Equipment" and self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]].getUsable()==False:
							if self.subPos==1:
								self.subPos=2
							else:
								self.subPos-=1
						else:
							if self.subPos==0:
								self.subPos=2
							else:
								self.subPos-=1
					elif self.menu==4:
						if self.subPos<=0:
							self.subPos = len(self.player.getParty())
						else:
							self.subPos -= 1
				elif self.tab==2:	#Party
					if self.menu==0 or self.menu==3:
						if self.pos[1]==0:
							self.pos[1]=len(self.player.getParty())
						else:
							self.pos[1]-=1
					elif self.menu==1:
						if self.subPos==0:
							self.subPos=1
						else:
							self.subPos-=1
					elif self.menu==2:
						if self.pos[1]==0:
							if self.sel.isPlayer():
								self.pos[1]=13
							else:
								self.pos[1]=8
						else:
							self.pos[1]-=1
					elif self.menu==5:
						if self.subPos==0:
							self.subPos=len(self.sel.getJob().getUnlockedSkills())
						else:
							self.subPos-=1
					elif self.menu==6:
						if self.subPos==0:
							self.subPos=len(self.sel.getJob().getUnlockedSkills())-1
						else:
							self.subPos-=1
				elif self.tab == 4:
					if self.pos[1] <= 0:
						self.pos[1] = len(self.player.getQuests())-1
					else:
						self.pos[1] -= 1
			self.move=0.0

	def SelDown(self):
		if self.move>=.25:
			self.statusScroll=-30
			self.selScroll=-30

			if self.pos[0]==-1:
				self.pos[1]=0
				if self.tab==4:
					self.tab=0
				else:
					self.tab+=1
			else:
				if self.tab==0:		#Inventory
					if self.menu==0 or self.menu==2:
						if self.size==0:
							if self.pos[1]==2:
								self.pos[1]=0
							else:
								self.pos[1]+=1
						else:
							if self.pos[1]==5:
								self.pos[1]=0
							else:
								self.pos[1]+=1
					elif self.menu==1:
						if self.subPos==2:
							if self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]].getType()!="Equipment" and self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]].getUsable()==False:
								self.subPos=1
							else:
								self.subPos=0
						else:
							self.subPos+=1
					elif self.menu==4:
						if self.subPos>=len(self.player.getParty()):
							self.subPos = 0
						else:
							self.subPos += 1
				elif self.tab==2:	#Party
					if self.menu==0 or self.menu==3:
						if self.pos[1]>=len(self.player.getParty()):
							self.pos[1]=0
						else:
							self.pos[1]+=1
					elif self.menu==1:
						if self.subPos == 1:
							self.subPos=0
						else:
							self.subPos+=1
					elif self.menu==2:
						if self.sel.isPlayer():
							if self.pos[1]==13:
								self.pos[1]=0
							else:
								self.pos[1]+=1
						else:
							if self.pos[1]==8:
								self.pos[1]=0
							else:
								self.pos[1]+=1
					elif self.menu==5:
						if self.subPos>=len(self.sel.getJob().getUnlockedSkills()):
							self.subPos=0
						else:
							self.subPos+=1
					elif self.menu==6:
						if self.subPos>=len(self.sel.getJob().getUnlockedSkills())-1:
							self.subPos=0
						else:
							self.subPos+=1
				elif self.tab == 4:
					if self.pos[1] >= len(self.player.getQuests())-1:
						self.pos[1] = 0
					else:
						self.pos[1] += 1
			self.move=0.0

	def SelRight(self):
		if self.move>=.25:
			self.statusScroll=-30
			self.selScroll=-30

			if self.tab==0:		#Inventory
				if self.menu==0:
					if self.pos[0]==self.invenSizeX-1:
						self.pos[0]=-1
					else:
						self.pos[0]+=1
				elif self.menu==2:
					if self.pos[0]==self.invenSizeX-1:
						self.pos[0]=0
					else:
						self.pos[0]+=1
				elif self.menu==3:
					self.subPos=abs(self.subPos-1)
			elif self.tab==2:	#Party
				if self.menu==0:
					self.pos[0]=-(self.pos[0]+1)
				if self.menu==2:
					if self.pos[0]==1:
						self.pos[0]=0
					else:
						self.pos[0]+=1
			elif self.tab==4:	#Quests
				if len(self.player.getQuests())>0:
					self.pos[0]=-(self.pos[0]+1)
			self.move=0.0

	def SelLeft(self):
		if self.move>=.25:
			self.statusScroll=-30
			self.selScroll=-30

			if self.tab==0:		#Inventory
				if self.menu==0:
					if self.pos[0]==-1:
						self.pos[0]=self.invenSizeX-1
					else:
						self.pos[0]-=1
				elif self.menu==2:
					if self.pos[0]==0:
						self.pos[0]=self.invenSizeX-1
					else:
						self.pos[0]-=1
				elif self.menu==3:
					self.subPos=abs(self.subPos-1)
			elif self.tab==2:	#Party
				if self.menu==0:
					self.pos[0]=-(self.pos[0]+1)
				elif self.menu==2:
					if self.pos[0]==0:
						self.pos[0]=1
					else:
						self.pos[0]-=1
			elif self.tab==4:	#Quests
				if len(self.player.getQuests())>0:
					self.pos[0]=-(self.pos[0]+1)
			self.move=0.0

	def drawInventory(self,screen):
		for x in range(0,self.invenSizeX):
			for y in range(0,6):
				screen.blit(Icons.iconBG,[self.winX+9+(x*30),33+(y*30)])

		if self.size==0:
			for x in range(0,self.invenSizeX):
				for y in range(3,6):
					screen.blit(Icons.lock,[self.winX+9+(x*30),33+(y*30)])
		x=self.winX+9
		y=33
		for item in self.player.getInventory().getItems():
			if item == None:
				if x >= self.winX+self.winSizeX-33:
					x=self.winX+9
					y+=30
				else:
					x+=30
				continue
			if item.getEquiped():
				screen.blit(Icons.iconBGE,[x,y])
			screen.blit(item.getSprite(),[x,y])

			if item.getAmount()>1:
				#print font.size(str(item.getAmount()))[0]
				screen.blit(font.render(str(item.getAmount()),False,config.ColorFont),[x+22-font.size(str(item.getAmount()))[0],y+14])

			if self.pos==[(x-self.winX+9)/30,(y-33)/30]:
				#debugInfo.setText(str(item.getEquiped()))
				if item.getDescription()!="":
					self.status=item.getName()+" - "+item.getDescription()
				else:
					self.status=item.getName()

			if x >= self.winX+self.winSizeX-60:
				x=self.winX+9
				y+=30
			else:
				x+=30

	def menuInventory(self,screen):
		if self.pos[0]==-1:
			self.status="Inventory"
		screen.fill(config.Color,[self.winX+self.winSizeX-1,40,14,18])		# Lighten current tab.

		self.drawInventory(screen)

		if self.menu==1:	#Item Menu
			screen.fill((config.ColorDark),[self.winX+2+(self.pos[0]*30),59+(self.pos[1]*30),38,38])
			screen.fill((config.Color),[self.winX+3+(self.pos[0]*30),60+(self.pos[1]*30),36,36])
			if len(self.player.getInventory().getItems())-1>=(self.pos[1]*self.invenSizeX)+self.pos[0]:
				item = self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]]
				if item.getType()=="Equipment":
					if self.subPos==0:
						screen.blit(font.render("Equip",False,config.ColorSel),[self.winX+5+(self.pos[0]*30),61+(self.pos[1]*30)])
					else:
						screen.blit(font.render("Equip",False,config.ColorFont),[self.winX+5+(self.pos[0]*30),61+(self.pos[1]*30)])
					self.status=""
					for stat in item.getStats():
						statVal = item.getStats()[stat]
						comp = self.player.getInventory().getComparison(item,stat)
						if comp>0:
							comp="+"+str(comp)
						else:
							comp=str(comp)
						if statVal>0:
							self.status+= stat+": +"+str(statVal)+"("+comp+"), "
						else:
							self.status+= stat+": "+str(statVal)+"("+comp+"), "
					self.status = self.status.rstrip(", ")
				else:
					if item.getUsable():
						if self.subPos==0:
							screen.blit(font.render("Use",False,config.ColorSel),[self.winX+5+(self.pos[0]*30),61+(self.pos[1]*30)])
						else:
							screen.blit(font.render("Use",False,config.ColorFont),[self.winX+5+(self.pos[0]*30),61+(self.pos[1]*30)])
					else:
						screen.blit(font.render("Use",False,config.ColorDisable),[self.winX+5+(self.pos[0]*30),61+(self.pos[1]*30)])
				if self.subPos==1:
					screen.blit(font.render("Move",False,config.ColorSel),[self.winX+5+(self.pos[0]*30),73+(self.pos[1]*30)])
				else:
					screen.blit(font.render("Move",False,config.ColorFont),[self.winX+5+(self.pos[0]*30),73+(self.pos[1]*30)])
				if self.subPos==2:
					screen.blit(font.render("Drop",False,config.ColorSel),[self.winX+5+(self.pos[0]*30),85+(self.pos[1]*30)])
				else:
					screen.blit(font.render("Drop",False,config.ColorFont),[self.winX+5+(self.pos[0]*30),85+(self.pos[1]*30)])
		elif self.menu==2:	#Move Item
			self.status = "Move where?"
			screen.blit(Icons.cursor,[self.winX+9+(self.pos[0]*30),33+(self.pos[1]*30)])
			temp=Icons.cursor.copy()
			temp.fill((255,255,255,127+abs(int(self.blink*127))),special_flags=BLEND_RGBA_MULT)
			screen.blit(temp,[self.winX+9+(self.sel[0]*30),33+(self.sel[1]*30)])
		elif self.menu==3: #Drop Item Confirm
			screen.fill((config.ColorDark),[119,107,82,26])
			screen.fill((config.Color),[120,108,80,24])
			screen.blit(font.render("Destroy item?",False,config.ColorFont),[124,110])
			if self.subPos==0:
				screen.blit(font.render("Yes",False,config.ColorSel),[132,122])
			else:
				screen.blit(font.render("Yes",False,config.ColorFont),[132,122])
			if self.subPos==1:
				screen.blit(font.render("No",False,config.ColorSel),[167,122])
			else:
				screen.blit(font.render("No",False,config.ColorFont),[167,122])
		elif self.menu==4:
			screen.fill((config.Color),[self.winX+3,32,self.winSizeX-6,176])

			self.drawParty(screen,self.subPos)

			self.status = "Use on who?"

			if self.subPos <3:
				screen.blit(Icons.cursorChar,[self.winX+4,33+(38*self.subPos)])
				temp=Icons.cursorCharBlink.copy()
				temp.fill((255,255,255,abs(int(self.blink*255))),special_flags=BLEND_RGBA_MULT)
				screen.blit(temp,[self.winX+4,33+(38*self.subPos)])
			else:
				screen.blit(Icons.cursorChar,[self.winX+4,33+(38*3)])
				temp=Icons.cursorCharBlink.copy()
				temp.fill((255,255,255,abs(int(self.blink*255))),special_flags=BLEND_RGBA_MULT)
				screen.blit(temp,[self.winX+4,33+(38*3)])

		if self.pos[0]!=-1 and self.menu!=4:
			screen.blit(Icons.cursor,[self.winX+9+(self.pos[0]*30),33+(self.pos[1]*30)])
			temp=Icons.cursorBlink.copy()
			temp.fill((255,255,255,abs(int(self.blink*255))),special_flags=BLEND_RGBA_MULT)
			screen.blit(temp,[self.winX+9+(self.pos[0]*30),33+(self.pos[1]*30)])

	## Draws the armor submenu.
	def menuArmor(self,screen):
		if self.pos[0]==-1:
			self.status="Armor"
		screen.fill(config.Color,[self.winX+self.winSizeX-1,65,14,18])
		if self.menu == 0:
			screen.fill(config.ColorDark,(91,31,46,16))
			screen.fill(config.Color,(92,32,44,14))
			screen.blit(Icons.gold,(122,33))
			gold = self.player.getInventory().getGold()
			if gold < 10000:
				screen.blit(font.render(str(gold),False,config.ColorFont),(94,35))
			elif gold < 1000000:
				screen.blit(font.render("%.1fK"%(gold/1000.0),False,config.ColorFont),(94,35))
			else:
				screen.blit(font.render("%.1fM"%(gold/1000000.0),False,config.ColorFont),(94,35))

			head = self.player.getInventory().getHead()
			body = self.player.getInventory().getBody()
			legs = self.player.getInventory().getLegs()
			boot = self.player.getInventory().getBoot()
			arm1 = self.player.getInventory().getArm1()
			arm2 = self.player.getInventory().getArm2()

			battle = self.player.getBattleObject()
			stats = {"Atk":battle.getAtk(),"Def":battle.getDef(),"Spd":battle.getSpd(),"Vit":battle.getVit(),"Mag":battle.getMag(),"Res":battle.getRes(),"Con":battle.getCon(),"Mnd":battle.getMnd()}

			screen.blit(Icons.iconBG,(168,80))
			if head == None:
				screen.blit(Icons.headArmor,(168,80))
			else:
				screen.blit(head.getSprite(),(168,80))

			screen.blit(Icons.iconBG,(168,105))
			if body == None:
				screen.blit(Icons.bodyArmor,(168,105))
			else:
				screen.blit(body.getSprite(),(168,105))

			screen.blit(Icons.iconBG,(168,130))
			if legs == None:
				screen.blit(Icons.legsArmor,(168,130))
			else:
				screen.blit(legs.getSprite(),(168,130))

			screen.blit(Icons.iconBG,(168,155))
			if boot == None:
				screen.blit(Icons.bootArmor,(168,155))
			else:
				screen.blit(boot.getSprite,(168,155))

			screen.blit(Icons.iconBG,(193,105))
			if arm1 == None:
				screen.blit(Icons.arm1Armor,(193,105))
			else:
				screen.blit(arm1.getSprite(),(193,105))

			screen.blit(Icons.iconBG,(143,105))
			if arm2 == None:
				screen.blit(Icons.arm2Armor,(143,105))
			else:
				screen.blit(arm2.getSprite(),(143,105))
			#	for stat in arm2.getStats():
			#		stats[stat]+=arm2.getStats()[stat]

			screen.blit(font.render("Atk: "+str(stats["Atk"]),False,config.ColorFont),(94,80))
			screen.blit(font.render("Def: "+str(stats["Def"]),False,config.ColorFont),(94,90))
			screen.blit(font.render("Spd: "+str(stats["Spd"]),False,config.ColorFont),(94,100))
			screen.blit(font.render("Vit: "+str(stats["Vit"]),False,config.ColorFont),(94,110))

			screen.blit(font.render("Mag: "+str(stats["Mag"]),False,config.ColorFont),(94,130))
			screen.blit(font.render("Res: "+str(stats["Res"]),False,config.ColorFont),(94,140))
			screen.blit(font.render("Con: "+str(stats["Con"]),False,config.ColorFont),(94,150))
			screen.blit(font.render("Mnd: "+str(stats["Mnd"]),False,config.ColorFont),(94,160))

	def drawParty(self,screen,pos):
		screen.fill(config.ColorDark,[self.winX+4,33,self.winSizeX-8,35])	#Draw Player Stat Box
		screen.fill(config.Color,[self.winX+5,34,self.winSizeX-10,33])		#Fill
		screen.fill(config.ColorDark,[self.winX+7,36,29,29])	#Draw Icon Outline
		screen.fill(config.Color,[self.winX+8,37,27,27])
		screen.blit(self.player.getIcon(),[self.winX+8,37])

		i=0

		if pos < 4:
			game = self.player.getBattleObject()

			if pos==0:
				self.status="See more about "+self.player.getName()
				screen.blit(scrollText(self.player.getName(),self.winSizeX-46,self.selScroll),[self.winX+39,36])
				if self.selScroll>=font.size(self.player.getName())[0]-46:
					self.selScroll=-30
			else:
				screen.blit(scrollText(self.player.getName(),self.winSizeX-46,0),[self.winX+39,36])

			screen.blit(font.render(str(game.getLevel()),False,config.ColorFont),[self.winX+10,55])

			screen.fill([64,0,0],[self.winX+55,49+(38*i),(self.winSizeX-78)+2,3])	#Health Bar
			screen.fill([255,0,0],[self.winX+56,50+(38*i),int(float(game.getHP())/game.getHPM()*(self.winSizeX-78)),1])
			screen.fill([0,0,64],[self.winX+55,59+(38*i),(self.winSizeX-78)+2,3])	#Mana Bar
			screen.fill([0,0,255],[self.winX+56,60+(38*i),int(float(game.getMP())/game.getMPM()*(self.winSizeX-78)),1])
			screen.blit(font.render("HP: "+game.getHPS()+"/"+str(game.getHPMS()),False,config.ColorFont),[self.winX+39,46+(38*i)])
			screen.blit(font.render("MP: "+game.getMPS()+"/"+str(game.getMPMS()),False,config.ColorFont),[self.winX+39,56+(38*i)])

			if self.player.getClass().getName()=="Warrior":
				screen.blit(Icons.warriorSmall,(self.winX+self.winSizeX-18,53))
			elif self.player.getClass().getName()=="Archer":
				screen.blit(Icons.archerSmall,(self.winX+self.winSizeX-18,53))
			elif self.player.getClass().getName()=="Mage":
				screen.blit(Icons.mageSmall,(self.winX+self.winSizeX-18,53))

			i=1
		if len(self.player.getParty())>0:
			for n in range(max(pos-4,0),min(max(3,pos),len(self.player.getParty()))):
				#print n
				character = self.player.getParty()[n]

				if n <3:
					screen.fill(config.ColorDark,[self.winX+4,33+(38*i),self.winSizeX-8,35])	#Draw Character Stat Box
					screen.fill(config.Color,[self.winX+5,34+(38*i),self.winSizeX-10,33])		#Fill
					screen.fill(config.ColorDark,[self.winX+7,36+(38*i),29,29])		#Draw Icon Outline
					screen.fill(config.Color,[self.winX+8,37+(38*i),27,27])
				else:
					screen.fill(config.Color,[self.winX+4,33+(38*i),self.winSizeX-8,35])		#Not in battle so grayed out
					screen.fill(config.ColorDark,[self.winX+5,34+(38*i),self.winSizeX-10,33])
					screen.fill(config.ColorDark,[self.winX+7,36+(38*i),29,29])
					screen.fill(config.ColorDark,[self.winX+8,37+(38*i),27,27])
				screen.blit(character.getIcon(),[self.winX+8,37+(38*i)])

				game = character.getBattleObject()

				if pos==i or (pos>3 and i==3):
					self.status="See more about "+character.getName()
					screen.blit(scrollText(character.getName(),86,self.selScroll),[self.winX+39,36+(38*i)])
					if self.selScroll>=font.size(character.getName())[0]-46:
						self.selScroll=-30
				else:
					screen.blit(scrollText(character.getName(),86,0),[self.winX+39,36+(38*i)])

				screen.blit(font.render(str(game.getLevel()),False,config.ColorFont),[self.winX+10,55+(38*i)])

				screen.fill([64,0,0],[self.winX+55,49+(38*i),self.winSizeX-76,3])	#Health Bar
				screen.fill([255,0,0],[self.winX+56,50+(38*i),int(float(game.getHP())/game.getHPM()*(self.winSizeX-78)),1])
				screen.fill([0,0,64],[self.winX+55,59+(38*i),self.winSizeX-76,3])	#Mana Bar
				screen.fill([0,0,255],[self.winX+56,60+(38*i),int(float(game.getMP())/game.getMPM()*(self.winSizeX-78)),1])
				screen.blit(font.render("HP: "+game.getHPS()+"/"+game.getHPMS(),False,config.ColorFont),[self.winX+39,46+(38*i)])
				screen.blit(font.render("MP: "+game.getMPS()+"/"+game.getMPMS(),False,config.ColorFont),[self.winX+39,56+(38*i)])

				if character.getClass().getName()=="Warrior":
					screen.blit(Icons.warriorSmall,(self.winX+self.winSizeX-18,53+(38*i)))
				elif character.getClass().getName()=="Archer":
					screen.blit(Icons.archerSmall,(self.winX+self.winSizeX-18,53+(38*i)))
				elif character.getClass().getName()=="Mage":
					screen.blit(Icons.mageSmall,(self.winX+self.winSizeX-18,53+(38*i)))

				if self.menu==3 and n==self.sel:
					temp=Icons.cursorChar.copy()
					temp.fill((255,255,255,127+abs(int(self.blink*127))),special_flags=BLEND_RGBA_MULT)
					screen.blit(temp,[93,33+(38*i)])

				i+=1
				if i>3:
					break

		if len(self.player.getParty())>=4 and pos <= len(self.player.getParty())-1:
			if pos <3:
				character = self.player.getParty()[3]
			else:
				character = self.player.getParty()[pos]

			screen.fill(config.Color,[self.winX+4,185,self.winSizeX-8,25])			#Draw Character Stat Box
			screen.fill(config.ColorDark,[self.winX+5,186,self.winSizeX-10,24])		#Fill (Inactive)
			screen.fill(config.ColorDark,[self.winX+7,188,29,22])		#Draw Icon Outline
			screen.fill(config.ColorDark,[self.winX+8,189,27,21])
			screen.blit(character.getIcon(),[self.winX+9,189],area=[0,0,25,22])

			game = character.getBattleObject()
			screen.blit(scrollText(character.getName(),86,0),[self.winX+39,36+(38*i)])

			screen.fill([64,0,0],[self.winX+55,49+(38*i),self.winSizeX-76,3])	#Health Bar
			screen.fill([255,0,0],[self.winX+56,50+(38*i),int(float(game.getHP())/game.getHPM()*(self.winSizeX-78)),1])
			screen.blit(font.render("HP: "+game.getHPS()+"/"+game.getHPMS(),False,config.ColorFont),[self.winX+39,46+(38*i)])

			if character.getClass()=="Warrior":
				screen.blit(Icons.warriorSmall,(self.winX+self.winSizeX-18,53+(38*i)),area=[0,0,12,5])
			elif character.getClass()=="Archer":
				screen.blit(Icons.archerSmall,(self.winX+self.winSizeX-18,53+(38*i)),area=[0,0,12,5])
			elif character.getClass()=="Mage":
				screen.blit(Icons.mageSmall,(self.winX+self.winSizeX-18,53+(38*i)),area=[0,0,12,5])

	def drawCharacter(self,screen):
		screen.fill(config.ColorDark,[self.winX+7,36,29,29])	#Draw Icon Outline
		screen.fill(config.Color,[self.winX+8,37,27,27])
		screen.blit(self.sel.getIcon(),[self.winX+8,37])
		screen.blit(titleFont.render(self.sel.getName(),False,config.ColorFont),[self.winX+39,36])
		if self.pos[1]==0:
			screen.blit(font.render(self.sel.getClass().getName(),False,config.ColorSel),[self.winX+39,47])
			self.status=self.sel.getClass().getDescription()
		else:
			screen.blit(font.render(self.sel.getClass().getName(),False,config.ColorFont),[self.winX+39,47])

		game = self.sel.getBattleObject()

		screen.fill([0,64,0],[self.winX+73,58,self.winSizeX-81,3])	#Experience Bar
		screen.fill([0,255,0],[self.winX+74,59,int(float(min(game.getExp(),game.getExpNext()))/game.getExpNext()*(self.winSizeX-83)),1])
		if self.pos[1]==1:
			screen.blit(font.render("Level: "+str(game.getLevel()),False,config.ColorSel),[self.winX+39,55])
			if game.getExp()>=game.getExpNext():
				self.status="Level up! Press [Accept] to level up."
			else:
				self.status="Level: "+str(game.getLevel())+", "+str(game.getExpNext()-game.getExp())+" exp until next level!"
		else:
			screen.blit(font.render("Level: "+str(game.getLevel()),False,config.ColorFont),[self.winX+39,55])

		screen.fill([64,0,0],[self.winX+23,69,self.winSizeX-31,3])	#Health Bar
		screen.fill([255,0,0],[self.winX+24,70,int(float(game.getHP())/game.getHPM()*(self.winSizeX-33)),1])
		screen.fill([0,0,64],[self.winX+23,78,self.winSizeX-31,3])	#Mana Bar
		screen.fill([0,0,255],[self.winX+24,79,int(float(game.getMP())/game.getMPM()*(self.winSizeX-33)),1])
		if self.pos[1]==2:
			screen.blit(font.render("HP: "+str(game.getHP())+"/"+str(game.getHPM()),False,config.ColorSel),[self.winX+7,66])
			self.status="Health: "+str(game.getHP())
		else:
			screen.blit(font.render("HP: "+str(game.getHP())+"/"+str(game.getHPM()),False,config.ColorFont),[self.winX+7,66])
		if self.pos[1]==3:
			screen.blit(font.render("MP: "+str(game.getMP())+"/"+str(game.getMPM()),False,config.ColorSel),[self.winX+7,75])
			self.status="Mana: "+str(game.getMP())
		else:
			screen.blit(font.render("MP: "+str(game.getMP())+"/"+str(game.getMPM()),False,config.ColorFont),[self.winX+7,75])

		status = game.getStatus()
		statusT = ""		#status Text
		if status==0:
			statusT="Normal, "
		if status&0b1:
			statusT+="Poisoned, "
		if status&0b10:
			statusT+="Paralyzed, "
		if status&0b100:
			statusT+="Frozen, "
		if status&0b1000:
			statusT+="Burned, "
		statusT=statusT[0:-2]

		if self.pos[1]==4:
			screen.blit(font.render("Status:",False,config.ColorSel),[self.winX+7,84])
			screen.blit(scrollText(statusT,77,self.selScroll,config.ColorSel),[self.winX+47,84])
			if self.selScroll>=font.size(statusT)[0]-37:
				self.selScroll=-30

			if status==0:
				self.status="Normal - This character is healthy."
			else:
				self.status=""
				if status&0b1:
					self.status+="Poisoned - This character will take damage over time, "
				if status&0b10:
					self.status+="Paralyzed - This character will be unable to move in battle, "
				if status&0b100:
					self.status+="Frozen - This character will move slower in battle, "
				if status&0b1000:
					self.status+="Burned - This character will take damage over time in battle, "
				self.status=self.status[0:-2]+'.'
		else:
			screen.blit(font.render("Status:",False,config.ColorFont),[self.winX+7,84])
			screen.blit(scrollText(statusT,77,0),[self.winX+47,84])

		screen.fill(config.ColorDark,[self.winX+5,97,self.winSizeX-10,1])

		if self.pos[0]==0:
			if self.pos[1]==5:
				screen.blit(font.render("Atk: "+str(game.getAtkN()),False,config.ColorSel),[self.winX+7,103])
				self.status="Physical Attack - Affects how much damage physical attacks do."
			else:
				screen.blit(font.render("Atk: "+str(game.getAtkN()),False,config.ColorFont),[self.winX+7,103])

			if self.pos[1]==6:
				screen.blit(font.render("Spd: "+str(game.getSpdN()),False,config.ColorSel),[self.winX+7,112])
				self.status="Speed - Affects movement and physical attack speed in battles."
			else:
				screen.blit(font.render("Spd: "+str(game.getSpdN()),False,config.ColorFont),[self.winX+7,112])

			if self.pos[1]==7:
				screen.blit(font.render("Mag: "+str(game.getMagN()),False,config.ColorSel),[self.winX+7,130])
				self.status="Magic Attack - Affects how much damage magical attacks do."
			else:
				screen.blit(font.render("Mag: "+str(game.getMagN()),False,config.ColorFont),[self.winX+7,130])

			if self.pos[1]==8:
				screen.blit(font.render("Con: "+str(game.getConN()),False,config.ColorSel),[self.winX+7,139])
				self.status="Concentration - Makes it harder for abilities to be interupted, as well as affecting magical attack speed in battles."
			else:
				screen.blit(font.render("Con: "+str(game.getConN()),False,config.ColorFont),[self.winX+7,139])
		else:
			screen.blit(font.render("Atk: "+str(game.getAtkN()),False,config.ColorFont),[self.winX+7,103])
			screen.blit(font.render("Spd: "+str(game.getSpdN()),False,config.ColorFont),[self.winX+7,112])
			screen.blit(font.render("Mag: "+str(game.getMagN()),False,config.ColorFont),[self.winX+7,130])
			screen.blit(font.render("Con: "+str(game.getConN()),False,config.ColorFont),[self.winX+7,139])

		if self.pos[0]==1:
			if self.pos[1]==5:
				screen.blit(font.render("Def: "+str(game.getDefN()),False,config.ColorSel),[self.winX+(self.winSizeX/2),103])
				self.status="Physical Defense - Affects how much damage is taken from physical attacks."
			else:
				screen.blit(font.render("Def: "+str(game.getDefN()),False,config.ColorFont),[self.winX+(self.winSizeX/2),103])

			if self.pos[1]==6:
				screen.blit(font.render("Vit: "+str(game.getVitN()),False,config.ColorSel),[self.winX+(self.winSizeX/2),112])
				self.status="Vitality - Affects Health."
			else:
				screen.blit(font.render("Vit: "+str(game.getVitN()),False,config.ColorFont),[self.winX+(self.winSizeX/2),112])

			if self.pos[1]==7:
				screen.blit(font.render("Res: "+str(game.getResN()),False,config.ColorSel),[self.winX+(self.winSizeX/2),130])
				self.status="Resistance (Magic Defence) - Affects how much damage is take from magical attacks."
			else:
				screen.blit(font.render("Res: "+str(game.getResN()),False,config.ColorFont),[self.winX+(self.winSizeX/2),130])

			if self.pos[1]==8:
				screen.blit(font.render("Mnd: "+str(game.getMndN()),False,config.ColorSel),[self.winX+(self.winSizeX/2),139])
				self.status="Mind - Affects Mana."
			else:
				screen.blit(font.render("Mnd: "+str(game.getMndN()),False,config.ColorFont),[self.winX+(self.winSizeX/2),139])
		else:
			screen.blit(font.render("Def: "+str(game.getDefN()),False,config.ColorFont),[self.winX+(self.winSizeX/2),103])
			screen.blit(font.render("Vit: "+str(game.getVitN()),False,config.ColorFont),[self.winX+(self.winSizeX/2),112])
			screen.blit(font.render("Res: "+str(game.getResN()),False,config.ColorFont),[self.winX+(self.winSizeX/2),130])
			screen.blit(font.render("Mnd: "+str(game.getMndN()),False,config.ColorFont),[self.winX+(self.winSizeX/2),139])

		if self.sel.isPlayer():
			screen.fill(config.ColorDark,[self.winX+5,152,self.winSizeX-10,1])
			if self.pos[1]==9:
				if self.sel.getSkill("S1")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,158])
					self.status="[S1]: Not Assigned"
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1").getName(),False,config.ColorSel),[self.winX+7,158])
					self.status="[S1]: "+self.sel.getSkill("S1").getName()
				temp = Icons.circ.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+16,157))
			else:
				if self.sel.getSkill("S1")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,158])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1").getName(),False,config.ColorFont),[self.winX+7,158])
				screen.blit(Icons.circ,(self.winX+16,157))
			if self.pos[1]==10:
				if self.sel.getSkill("S1U")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,167])
					self.status="[S1]+[Up]: Not Assigned"
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1U").getName(),False,config.ColorSel),[self.winX+7,167])
					self.status="[S1]+[Up]: "+self.sel.getSkill("S1U").getName()
				temp = Icons.upArrow.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+16,168))
			else:
				if self.sel.getSkill("S1U")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,167])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1U").getName(),False,config.ColorFont),[self.winX+7,167])
				screen.blit(Icons.upArrow,(self.winX+16,168))
			if self.pos[1]==11:
				if self.sel.getSkill("S1R")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,176])
					self.status="[S1]+[Right]: Not Assigned"
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1R").getName(),False,config.ColorSel),[self.winX+7,176])
					self.status="[S1]+[Right]: "+self.sel.getSkill("S1R").getName()
				temp = Icons.rightArrow.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+14,175))
			else:
				if self.sel.getSkill("S1R")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,176])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1R").getName(),False,config.ColorFont),[self.winX+7,176])
				screen.blit(Icons.rightArrow,(self.winX+14,175))
			if self.pos[1]==12:
				if self.sel.getSkill("S1L")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,185])
					self.status="[S1]+[Left]: Not Assigned"
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1L").getName(),False,config.ColorSel),[self.winX+7,185])
					self.status="[S1]+[Left]: "+self.sel.getSkill("S1L").getName()
				temp = Icons.leftArrow.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+19,184))
			else:
				if self.sel.getSkill("S1L")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,185])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1L").getName(),False,config.ColorFont),[self.winX+7,185])
				screen.blit(Icons.leftArrow,(self.winX+19,184))
			if self.pos[1]==13:
				if self.sel.getSkill("S1D")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,194])
					self.status="[S1]+[Down]: Not Assigned"
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1D").getName(),False,config.ColorSel),[self.winX+7,194])
					self.status="[S1]+[Down]: "+self.sel.getSkill("S1D").getName()
				temp = Icons.downArrow.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+16,191))
			else:
				if self.sel.getSkill("S1D")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,194])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1D").getName(),False,config.ColorFont),[self.winX+7,194])
				screen.blit(Icons.downArrow,(self.winX+16,191))

	def menuParty(self,screen):
		screen.fill(config.Color,[self.winX+self.winSizeX-1,90,14,18])		#Lighten current tab
		if self.menu == 0 or self.menu == 1 or self.menu==3:

			self.drawParty(screen,self.pos[1])

			if self.pos[0]!=-1:
				if self.pos[1] <3:
					screen.blit(Icons.cursorChar,[self.winX+4,33+(38*self.pos[1])])
					temp=Icons.cursorCharBlink.copy()
					temp.fill((255,255,255,abs(int(self.blink*255))),special_flags=BLEND_RGBA_MULT)
					screen.blit(temp,[self.winX+4,33+(38*self.pos[1])])
				else:
					screen.blit(Icons.cursorChar,[self.winX+4,33+(38*3)])
					temp=Icons.cursorCharBlink.copy()
					temp.fill((255,255,255,abs(int(self.blink*255))),special_flags=BLEND_RGBA_MULT)
					screen.blit(temp,[self.winX+4,33+(38*3)])

			if self.menu == 1:
				if self.pos[1]<3:
					screen.fill(config.ColorDark,[139,69+(38*self.pos[1]),32,26])
					screen.fill(config.Color,[140,70+(38*self.pos[1]),30,24])
					if self.subPos == 0:
						screen.blit(font.render("View",False,config.ColorSel),[142,72+(38*self.pos[1])])
					else:
						screen.blit(font.render("View",False,config.ColorFont),[142,72+(38*self.pos[1])])
					if self.subPos == 1:
						screen.blit(font.render("Move",False,config.ColorSel),[142,82+(38*self.pos[1])])
					else:
						screen.blit(font.render("Move",False,config.ColorFont),[142,82+(38*self.pos[1])])
				else:
					screen.fill(config.ColorDark,[139,183,32,26])
					screen.fill(config.Color,[140,184,30,24])
					if self.subPos == 0:
						screen.blit(font.render("View",False,config.ColorSel),[142,186])
					else:
						screen.blit(font.render("View",False,config.ColorFont),[142,186])
					if self.subPos == 1:
						screen.blit(font.render("Move",False,config.ColorSel),[142,196])
					else:
						screen.blit(font.render("Move",False,config.ColorFont),[142,196])
			elif self.menu == 3:	#Switch Characters
				self.status = "Switch with whom?"



		elif self.menu == 2:
			self.drawCharacter(screen)

		elif self.menu == 4:
			self.drawCharacter(screen)
			statChange = self.sel.getJob().getStatChange()

			screen.blit(font.render("+1",False,config.ColorSel),[self.winX+self.winSizeX-22,55])	#Level went up by 1

			screen.blit(font.render("+"+str(statChange["HP"]),False,config.ColorSel),[self.winX+self.winSizeX-22,66])
			screen.blit(font.render("+"+str(statChange["MP"]),False,config.ColorSel),[self.winX+self.winSizeX-22,75])

			screen.blit(font.render("+"+str(statChange["Atk"]),False,config.ColorSel),[self.winX+(self.winSizeX/2)-18,103])
			screen.blit(font.render("+"+str(statChange["Spd"]),False,config.ColorSel),[self.winX+(self.winSizeX/2)-18,112])
			screen.blit(font.render("+"+str(statChange["Mag"]),False,config.ColorSel),[self.winX+(self.winSizeX/2)-18,130])
			screen.blit(font.render("+"+str(statChange["Con"]),False,config.ColorSel),[self.winX+(self.winSizeX/2)-18,139])
			screen.blit(font.render("+"+str(statChange["Def"]),False,config.ColorSel),[self.winX+self.winSizeX-22,103])
			screen.blit(font.render("+"+str(statChange["Vit"]),False,config.ColorSel),[self.winX+self.winSizeX-22,112])
			screen.blit(font.render("+"+str(statChange["Res"]),False,config.ColorSel),[self.winX+self.winSizeX-22,130])
			screen.blit(font.render("+"+str(statChange["Mnd"]),False,config.ColorSel),[self.winX+self.winSizeX-22,139])

			self.status="Press [Accept] to continue."

		elif self.menu == 5:
			if self.subPos!=0:
				skill = self.sel.getJob().getUnlockedSkills()[self.subPos-1]
				if skill.getLevel()>0:
					color = config.ColorFont
					colorB= config.ColorSel
				else:
					color = config.ColorDisable
					colorB= config.ColorDisable
				screen.blit(titleFont.render(skill.getName(),False,colorB),[self.winX+7,32])
				screen.blit(font.render(str(skill.getType()),False,color),[self.winX+7,43])
				screen.blit(font.render("Level: "+str(skill.getLevel())+"",False,color),[self.winX+7,55])
				if skill.isActiveSkill():
					screen.blit(font.render("Cost: "+str(skill.getCost())+" MP",False,color),[self.winX+(self.winSizeX/2)+9,55])
				y=68
				for line in skill.getDescription():
					screen.blit(font.render(line,False,color),[self.winX+7,y])
					y+=9
			#screen.blit(font.render("HP: "+str(game.getHP())+"/"+str(game.getHPM()),False,config.ColorFont),[96,66])
			#screen.blit(font.render("MP: "+str(game.getMP())+"/"+str(game.getMPM()),False,config.ColorFont),[96,75])
			#screen.blit(font.render("Status:",False,config.ColorFont),[96,84])

			screen.fill(config.ColorDark,[self.winX+5,97,self.winSizeX-10,1])

			if self.subPos == 0:
				screen.blit(font.render("None",False,config.ColorSel),[self.winX+7,100])
				self.status = "No Skill"
			else:
				screen.blit(font.render("None",False,config.ColorFont),[self.winX+7,100])

			x = self.winX+7
			y = 110
			for n in range(max(self.subPos-4,0),min(max(5,self.subPos+1),len(self.sel.getJob().getUnlockedSkills()))):
				skill = self.sel.getJob().getUnlockedSkills()[n]
				if skill.getLevel()>0:
					if self.subPos == n+1:
						screen.blit(font.render(skill.getName(),False,config.ColorSel),[x,y])
						self.status = skill.getInfo()
					else:
						screen.blit(font.render(skill.getName(),False,config.ColorFont),[x,y])
				else:
					if self.subPos == n+1:
						screen.blit(font.render(skill.getName(),False,config.ColorSel),[x,y])
						self.status = "This skill hasn't been learned yet."
					else:
						screen.blit(font.render(skill.getName(),False,config.ColorDisable),[x,y])
				y+=9
#			for skill in self.sel.getJob().getSkills():
#				if skill.getUnlocked():
#					if skill.getLevel()>0:
#						if self.subPos == i:
#							screen.blit(font.render(skill.getName(),False,config.ColorSel),[x,y])
#							self.status = skill.getInfo()
#						else:
#							screen.blit(font.render(skill.getName(),False,config.ColorFont),[x,y])
#					else:
#						if self.subPos == i:
#							screen.blit(font.render(skill.getName(),False,config.ColorSel),[x,y])
#							self.status = "This skill hasn't been learned yet."
#						else:
#							screen.blit(font.render(skill.getName(),False,config.ColorDisable),[x,y])
#					i+=1
#					y+=9

			screen.fill(config.ColorDark,[self.winX+5,152,self.winSizeX-10,1])
			if self.pos[1]==9:
				if self.sel.getSkill("S1")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,158])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1").getName(),False,config.ColorSel),[self.winX+7,158])
				temp = Icons.circ.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+16,157))
			else:
				if self.sel.getSkill("S1")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,158])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1").getName(),False,config.ColorFont),[self.winX+7,158])
				screen.blit(Icons.circ,(self.winX+16,157))
			if self.pos[1]==10:
				if self.sel.getSkill("S1U")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,167])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1U").getName(),False,config.ColorSel),[self.winX+7,167])
				temp = Icons.upArrow.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+16,168))
			else:
				if self.sel.getSkill("S1U")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,167])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1U").getName(),False,config.ColorFont),[self.winX+7,167])
				screen.blit(Icons.upArrow,(self.winX+16,168))
			if self.pos[1]==11:
				if self.sel.getSkill("S1R")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,176])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1R").getName(),False,config.ColorSel),[self.winX+7,176])
				temp = Icons.rightArrow.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+14,175))
			else:
				if self.sel.getSkill("S1R")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,176])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1R").getName(),False,config.ColorFont),[self.winX+7,176])
				screen.blit(Icons.rightArrow,(self.winX+14,175))
			if self.pos[1]==12:
				if self.sel.getSkill("S1L")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,185])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1L").getName(),False,config.ColorSel),[self.winX+7,185])
				temp = Icons.leftArrow.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+19,184))
			else:
				if self.sel.getSkill("S1L")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,185])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1L").getName(),False,config.ColorFont),[self.winX+7,185])
				screen.blit(Icons.leftArrow,(self.winX+19,184))
			if self.pos[1]==13:
				if self.sel.getSkill("S1D")==None:
					screen.blit(font.render("S1  :",False,config.ColorSel),[self.winX+7,194])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1D").getName(),False,config.ColorSel),[self.winX+7,194])
				temp = Icons.downArrow.copy()
				temp.fill(config.ColorSel,special_flags=BLEND_MULT)
				screen.blit(temp,(self.winX+16,191))
			else:
				if self.sel.getSkill("S1D")==None:
					screen.blit(font.render("S1  :",False,config.ColorFont),[self.winX+7,194])
				else:
					screen.blit(font.render("S1  : "+self.sel.getSkill("S1D").getName(),False,config.ColorFont),[self.winX+7,194])
				screen.blit(Icons.downArrow,(self.winX+16,191))

		elif self.menu == 6:
			skill = self.sel.getJob().getUnlockedSkills()[self.subPos]
			screen.blit(titleFont.render(skill.getName(),False,config.ColorSel),[self.winX+7,32])
			screen.blit(font.render(str(skill.getType()),False,config.ColorFont),[self.winX+7,43])
			screen.blit(font.render("Level: "+str(skill.getLevel()+1)+"",False,config.ColorFont),[self.winX+7,55])
			if skill.isActiveSkill():
				screen.blit(font.render("Cost: "+str(skill.getNextCost())+" MP",False,config.ColorFont),[self.winX+(self.winSizeX/2)+9,55])
			y=68
			for line in skill.getDescription():
				screen.blit(font.render(line,False,config.ColorFont),[self.winX+7,y])
				y+=9

			screen.fill(config.ColorDark,[self.winX+5,97,self.winSizeX-10,1])

			x = self.winX+7
			y = 101
			for n in range(max(self.subPos-4,0),min(max(6,self.subPos+2),len(self.sel.getJob().getUnlockedSkills()))):
				skill = self.sel.getJob().getUnlockedSkills()[n]
				if self.subPos == n:
					screen.blit(font.render(skill.getName(),False,config.ColorSel),[x,y])
					self.status = "Level up "+skill.getName()+"?"
				else:
					screen.blit(font.render(skill.getName(),False,config.ColorFont),[x,y])
				y+=9

			screen.fill(config.ColorDark,[self.winX+5,152,self.winSizeX-10,1])

			x=self.winX+7
			y=156
			for change in self.sel.getJob().getUnlockedSkills()[self.subPos].getChanges():
				screen.blit(font.render(change,False,config.ColorFont),[x,y])
				y+=9

		if self.pos[0]==-1:
			self.status="Party Info"

	def menuMap(self,screen):
		if self.pos[0]==-1:
			self.status="Map"
		screen.fill(config.Color,[self.winX+self.winSizeX-1,115,14,18])

	def menuQuest(self,screen):
		screen.fill(config.Color,[self.winX+self.winSizeX-1,140,14,18])		# Lighten current tab.

		y = 35
		i = 0
		quests = self.player.getQuests().values()
		quests.sort(key=lambda x:x.getSort())
		for quest in quests:
			if self.pos[1] == i:
				screen.blit(font.render(quest.getName(),False,config.ColorSel),[self.winX+7,y])
				screen.blit(titleFont.render(quest.getName(),False,config.ColorSel),[self.winX+7,103])
				screen.blit(font.render(quest.getType()+" Quest",False,config.ColorFont),[self.winX+7,114])
				if quest.getCompleted():
					screen.blit(font.render("Completed!",False,config.ColorBold),[self.winX+7,128])
				else:
					screen.blit(font.render(quest.getCurrentName(),False,config.ColorFont),[self.winX+7,128])
					for j in xrange(len(quest.getCurrentDescription())):
						screen.blit(font.render(quest.getCurrentDescription()[j],False,config.ColorFont),[self.winX+7,142+(9*j)])
					if quest.isRewardVisible():
						tmp = []
						for reward in quest.getRewards():
							if reward == None:
								tmp.append("None")
							elif reward.startswith("Gold"):
								tmp.append(reward.split(" ")[-1]+" Gold")
							elif reward.startswith("Exp"):
								tmp.append(reward.split(" ")[-1]+" XP")
							elif reward.startswith("Item"):
								tmp.append(reward.split(" ")[1])
						if len(tmp)>1:
							self.status="Rewards: "+", ".join(tmp)
						else:
							self.status="Reward: "+tmp[0]
			else:
				if quest.getCompleted():
					screen.blit(font.render(quest.getName(),False,config.ColorDisable),[self.winX+7,y])
				else:
					screen.blit(font.render(quest.getName(),False,config.ColorFont),[self.winX+7,y])
			y+=9
			i+=1

		screen.fill(config.ColorDark,[self.winX+5,97,self.winSizeX-10,1])

		if self.pos[0]==-1:
			self.status="Quests"

	def draw(self,screen):
		screen.fill(config.ColorDark,[self.winX,14,self.winSizeX,212])
		screen.fill(config.Color,[self.winX+1,30,self.winSizeX-2,180])	#Main Window
		screen.fill(config.Color,[self.winX+1,16,self.winSizeX-2,12])	#Area Name Window
		screen.fill(config.Color,[self.winX+1,212,self.winSizeX-2,12])	#Status Window
		screen.fill(config.ColorDark,[self.winX+self.winSizeX-1,39,15,20])
		screen.fill(config.ColorDark,[self.winX+self.winSizeX-1,64,15,20])
		screen.fill(config.ColorDark,[self.winX+self.winSizeX-1,89,15,20])
		screen.fill(config.ColorDark,[self.winX+self.winSizeX-1,114,15,20])
		screen.fill(config.ColorDark,[self.winX+self.winSizeX-1,139,15,20])

		screen.blit(font.render(self.levelName,False,config.ColorFont),[self.winX+6,18])

		if self.tab==0:	#Inventory Tab
			self.menuInventory(screen)
		elif self.tab==1: #Armor Tab
			self.menuArmor(screen)
		elif self.tab==2:	#Party Info Tab
			self.menuParty(screen)
		elif self.tab==3:	#World Map Tab
			self.menuMap(screen)
		elif self.tab==4:	#Quests Tab
			self.menuQuest(screen)

		#Icons
		screen.blit(Icons.inventory,(self.winX+self.winSizeX,43))
		screen.blit(Icons.armor,(self.winX+self.winSizeX,68))
		screen.blit(Icons.party,(self.winX+self.winSizeX,93))
		screen.blit(Icons.globe,(self.winX+self.winSizeX,117))
		screen.blit(Icons.quests,(self.winX+self.winSizeX,142))

		if self.pos[0]==-1:
			screen.blit(Icons.cursorTab,[self.winX+self.winSizeX-1,40+(self.tab*25)])
			temp=Icons.cursorTabBlink.copy()
			temp.fill((255,255,255,abs(int(self.blink*255))),special_flags=BLEND_RGBA_MULT)
			screen.blit(temp,[self.winX+self.winSizeX-1,40+(self.tab*25)])

		screen.blit(scrollText(self.status,self.winSizeX-12,self.statusScroll),[self.winX+6,214])
		if self.statusScroll>font.size(self.status)[0]-80:
			self.statusScroll=-30
		#if font.size(self.status)[0]>120:
		#	cropped=pygame.Surface((120,12),SRCALPHA)
		#	if self.statusScroll<0:
		#		cropped.blit(font.render(self.status,False,config.ColorFont),[0,0])
		#		screen.blit(cropped,[95,214])
		#	elif self.statusScroll>=font.size(self.status)[0]-120:
		#		cropped.blit(font.render(self.status,False,config.ColorFont),[-(font.size(self.status)[0]-120),0])
		#		screen.blit(cropped,[95,214])
		#		if self.statusScroll>font.size(self.status)[0]-90:
		#			self.statusScroll=-30
		#	else:
		#		cropped.blit(font.render(self.status,False,config.ColorFont),[-self.statusScroll,0])
		#		screen.blit(cropped,[95,214])
		#else:
		#	screen.blit(font.render(self.status,False,config.ColorFont),[95,214])

	def update(self,screen,tick):
		self.status=""
		self.move+=tick
		self.blink+=tick
		self.statusScroll+=tick*20
		self.selScroll+=tick*20
		if self.blink >=1:
			self.blink=-1

		self.draw(screen)

		return self.close

class CharacterCreator(Menu):
	def __init__(self,player,inputDump):
		Menu.__init__(self,6,1)

		self.playerClass = player
		self.inputDump = inputDump

		self.editing = True
		self.editingName = False
		self.timer = 0

		self.name = "Markus Calarkus"	#Change to ""
		self.job = 0
		self.clothingType=1
		self.clothingColor=0
		self.hairType=1
		self.hairColor=0

		self.jobs = ["Warrior","Archer"]
		self.colors = [[255,0,0],[255,127,0],[255,255,0],[127,255,0],[0,255,0],[0,255,127],[0,255,255],[0,127,255],[0,0,255],[255,255,255],[127,127,127],[100,50,0]]
		#self.hairTypes=3
		self.hairTypes=1
		self.clothingTypes=1

		self.preview = self.playerClass("Null",self.clothingType,self.colors[self.clothingColor],self.hairType,self.colors[self.hairColor],job=self.jobs[self.job],preview=True)
		self.preview.setState("Walk")
		self.preview.setDirection(2)

	def SelRight(self):
		if self.move >=.25 and not self.editingName:
			if self.pos[1] == 1:
				if self.clothingType >= self.clothingTypes:
					self.clothingType = 1
				else:
					self.clothingType+= 1
			elif self.pos[1] == 2:
				if self.clothingColor == len(self.colors)-1:
					self.clothingColor = 0
				else:
					self.clothingColor+= 1
			elif self.pos[1] == 3:
				if self.hairType == self.hairTypes:
					self.hairType = 1
				else:
					self.hairType+= 1
			elif self.pos[1] == 4:
				if self.hairColor == len(self.colors)-1:
					self.hairColor = 0
				else:
					self.hairColor+=1
			elif self.pos[1] == 5:
				if self.job >= len(self.jobs)-1:
					self.job = 0
				else:
					self.job+=1
			elif self.pos[1] == 6:
				self.pos[0] = abs(self.pos[0]-1)
			d = self.preview.getDirection()
			f = self.preview.getGraphicObject().getFrame()
			self.preview = self.playerClass("Null",self.clothingType,self.colors[self.clothingColor],self.hairType,self.colors[self.hairColor],job=self.jobs[self.job],preview=True)
			self.preview.setState("Walk")
			self.preview.setDirection(d)
			self.preview.getGraphicObject().setFrame(f)
			self.move=0.0

	def SelLeft(self):
		if self.move>=0.25 and not self.editingName:
			if self.pos[1] == 1:
				if self.clothingType == 1:
					self.clothingType = self.clothingTypes
				else:
					self.clothingType-= 1
			elif self.pos[1] == 2:
				if self.clothingColor == 0:
					self.clothingColor = len(self.colors)-1
				else:
					self.clothingColor-= 1
			elif self.pos[1] == 3:
				if self.hairType == 1:
					self.hairType = self.hairTypes
				else:
					self.hairType-= 1
			elif self.pos[1] == 4:
				if self.hairColor == 0:
					self.hairColor = len(self.colors)-1
				else:
					self.hairColor-= 1
			elif self.pos[1] == 5:
				if self.job == 0:
					self.job = len(self.jobs)-1
				else:
					self.job-= 1
			elif self.pos[1] == 6:
				self.pos[0] = abs(self.pos[0]-1)
			d = self.preview.getDirection()
			f = self.preview.getGraphicObject().getFrame()
			self.preview = self.playerClass("Null",self.clothingType,self.colors[self.clothingColor],self.hairType,self.colors[self.hairColor],job=self.jobs[self.job],preview=True)
			self.preview.setState("Walk")
			self.preview.setDirection(d)
			self.preview.getGraphicObject().setFrame(f)
			self.move=0.0

	def SelUp(self):
		if not self.editingName:
			Menu.SelUp(self)

	def SelDown(self):
		if not self.editingName:
			Menu.SelDown(self)

	def updateName(self):
		for event in self.inputDump:
			if event[1] == "Down":
				if self.editingName:
					if event[0].startswith("Raw_"):
						char = event[0][4:]
						if len(char) == 1:
							if (pygame.key.get_mods() & KMOD_LSHIFT)|(pygame.key.get_mods() & KMOD_RSHIFT):
								self.name += char.capitalize()
							else:
								self.name += char
						else:
							if event[0] == "Raw_backspace":
								self.name = self.name[0:-1]
							elif event[0] == "Raw_space":
								self.name += " "
					elif event[0] == "Accept":
						self.editingName = False
		self.inputDump.clear()

	def Select(self):
		if self.pos[1] == 0:
			self.editingName = not self.editingName
			self.inputDump.clear()
		elif self.pos[1] == 6:
			self.close = True
			if self.pos[0] == 0:
				self.value = "Main"
			elif self.pos[0] == 1:
				self.value = "Play"
				self.player=self.playerClass(self.name,self.clothingType,self.colors[self.clothingColor],self.hairType,self.colors[self.hairColor],job=self.jobs[self.job])
		else:
			self.move=0.25
			self.SelRight()

	def Cancel(self):
		if self.editingName:
			self.editingName = False
		else:
			self.move=0.25
			self.SelLeft()

	def getPlayer(self):
		return self.player

	def update(self,screen,tick):
		screen.fill(config.ColorDark,[4,4,122,147])
		screen.fill(config.Color,[5,5,120,145])
		if self.pos[1] == 0:
			if self.editingName:
				self.updateName()
				screen.blit(font.render("Name: "+self.name+"|",False,config.ColorSel,config.Color),(10,10))
			else:
				screen.blit(font.render("Name: "+self.name,False,config.ColorSel,config.Color),(10,10))
		else:
			screen.blit(font.render("Name: "+self.name,False,config.ColorFont,config.Color),(10,10))
		if self.pos[1] == 1:
			screen.blit(font.render("Clothing: "+str(self.clothingType),False,config.ColorSel,config.Color),(10,26))
		else:
			screen.blit(font.render("Clothing: "+str(self.clothingType),False,config.ColorFont,config.Color),(10,26))
		if self.pos[1] == 2:
			screen.blit(font.render("Color: "+str(self.clothingColor),False,config.ColorSel,config.Color),(10,38))
		else:
			screen.blit(font.render("Color: "+str(self.clothingColor),False,config.ColorFont,config.Color),(10,38))
		if self.pos[1] == 3:
			screen.blit(font.render("Hair: "+str(self.hairType),False,config.ColorSel,config.Color),(10,54))
		else:
			screen.blit(font.render("Hair: "+str(self.hairType),False,config.ColorFont,config.Color),(10,54))
		if self.pos[1] == 4:
			screen.blit(font.render("Color: "+str(self.hairColor),False,config.ColorSel,config.Color),(10,66))
		else:
			screen.blit(font.render("Color: "+str(self.hairColor),False,config.ColorFont,config.Color),(10,66))
		if self.pos[1] == 5:
			screen.blit(font.render("Class: "+self.jobs[self.job],False,config.ColorSel,config.Color),(10,82))
		else:
			screen.blit(font.render("Class: "+self.jobs[self.job],False,config.ColorFont,config.Color),(10,82))
		if self.pos[1] == 6:
			if self.pos[0] == 0:
				screen.blit(font.render("Back",False,config.ColorSel,config.Color),(10,138))
				screen.blit(font.render("Ok",False,config.ColorFont,config.Color),(50,138))
			elif self.pos[0]==1:
				screen.blit(font.render("Back",False,config.ColorFont,config.Color),(10,138))
				screen.blit(font.render("Ok",False,config.ColorSel,config.Color),(50,138))
		else:
			screen.blit(font.render("Back",False,config.ColorFont,config.Color),(10,138))
			screen.blit(font.render("Ok",False,config.ColorFont,config.Color),(50,138))

		#if str(self.preview.getClass())=="Warrior":
		#	screen.blit(Icons.warriorSmall,(44,22))
		#elif str(self.preview.getClass())=="Archer":
		#	screen.blit(Icons.archerSmall,(44,22))
		#elif str(self.preview.getClass())=="Mage":
		#	screen.blit(Icons.mageSmall,(44,22))

		if len(self.name)>14:
			screen.fill(config.ColorDark,[4,224,313,14])
			screen.fill(config.Color,[5,225,311,12])
			screen.blit(font.render("*Warning:Your name is long, it may not display properly",False,config.ColorBold),(9,226))

		self.timer += tick
		if self.timer >= 2:
			if self.preview.getDirection() == 3:
				self.preview.setDirection(0)
			else:
				self.preview.setDirection(self.preview.getDirection()+1)
			self.timer = 0
		self.preview.update(tick)
		screen.blit(pygame.transform.scale2x(self.preview.getSprite()),(150,50))
		screen.fill(config.ColorDark,[152,14,29,29])
		screen.fill(config.Color,[153,15,27,27])
		screen.blit(self.preview.getIcon(),[153,15])
		self.move+=tick

## Heads Up Display for Battles
#
#  Doesn't subclass HUD because HUD seems to be kinda bulky/look funny with auto-resize.
#  Also has no support for bars or any other graphics.
class BattleHUD(object):

	## Constructor
	#  @param allyTeam A list containing each character on the ally team.
	def __init__(self,allyTeam):
		self.allyTeam = allyTeam

	## Updates the the list of characters to show.
	def update(self,allyTeam):
		self.allyTeam = allyTeam

	## Draws the hud.
	def draw(self,screen):
		x=5
		for ally in self.allyTeam:
			if len(ally.getName())>14:
				width=86
			else:
				width = font.size(ally.getName())[0]+2
			width=max(width,font.size("HP: "+ally.getHPS()+"/"+ally.getHPMS())[0]+2,76)
			width=max(width,font.size("MP: "+ally.getMPS()+"/"+ally.getMPMS())[0]+2,76)
			screen.fill(config.ColorDark,[x-1,4,width+2,27])
			screen.fill(config.Color,[x,5,width,25])
			screen.blit(font.render(ally.getName(),True,config.ColorFont),(x+2,5))
			screen.fill([64,0,0],[x+18,15,56,3])	#Health Bar
			screen.fill([255,0,0],[x+19,16,int(float(ally.getHP())/ally.getHPM()*54),1])
			screen.fill([0,0,64],[x+18,24,56,3])	#Mana Bar
			screen.fill([0,0,255],[x+19,25,int(float(ally.getMP())/ally.getMPM()*54),1])
			screen.blit(font.render("HP: "+ally.getHPS()+"/"+ally.getHPMS(),True,config.ColorFont),(x+2,12))
			screen.blit(font.render("MP: "+ally.getMPS()+"/"+ally.getMPMS(),True,config.ColorFont),(x+2,21))
			x+=width+5

## The pause menu for the overworld and battles.
class PauseMenu(Menu):

	## Constructor
	def __init__(self):
		Menu.__init__(self,2,1)

	## Selects the current item.
	def Select(self):
		if self.menu == 0:
			if self.pos[1] == 0:
				self.close=True
				self.value="Resume"
			elif self.pos[1]==1:
				return
			elif self.pos[1]==2:
				self.close=True
				self.value="Exit"

	## Moves up a level in submenus or else closes the menu.
	def Cancel(self):
		if self.menu == 0:
			self.close=True
			self.value="Resume"

	## Draws all components of the screen.
	#
	#  @param screen An object representing the screen, either a pygame.Surface or a ScaledScreen.
	def draw(self,screen):
		screen.fill(config.ColorDark,[114,126,97,49])
		screen.fill(config.Color,[115,127,95,47])
		if self.menu == 0:
			self.drawMain(screen)

	## Draws the main menu on the screen.
	#
	#  @param screen An object representing the screen, either a pygame.Surface or a ScaledScreen.
	def drawMain(self,screen):
		if self.pos[1] == 0:
			screen.blit(titleFont.render("Resume Game",False,config.ColorSel),(120,130))
		else:
			screen.blit(titleFont.render("Resume Game",False,config.ColorFont),(120,130))
		if self.pos[1] == 1:
			screen.blit(titleFont.render("Options",False,config.ColorSel),(120,144))
		else:
			screen.blit(titleFont.render("Options",False,config.ColorFont),(120,144))
		if self.pos[1] == 2:
			screen.blit(titleFont.render("Exit",False,config.ColorSel),(120,158))
		else:
			screen.blit(titleFont.render("Exit",False,config.ColorFont),(120,158))

## Menu for buying things in shops.
class ShopBuyMenu(Menu):

	## Constructor
	#  @param player The player's player.Player() reference.
	#  @param shop A list of items.Item() objects for sale.
	def __init__(self,player,shop):
		self.player=player
		self.shop = shop

		# Constants:

		## The X position of this window's origin.
		self.winX = 64									#Old = 89
		## The X portion of this window's size.
		self.winSizeX = 192								#Old = 132
		## How many item slots there are in a row.
		self.invenSizeX = (self.winSizeX/30)

		#**********#

		self.pos=[0,0]
		self.menu=0		#Which sub-menu is open
		self.subPos=0	#Sub-menu cursor position
		self.sel=None	#Selected Item
		self.move=0.0	#time since cursor last moved
		self.blink=0.0	#time since cursor last blinked
		#self.size=player.getInventory().getSize()

		self.status=""
		self.statusScroll=0.0
		self.selScroll=0.0

		self.close=False

	## Move the cursor up.
	def SelUp(self):
		if self.move>=.25:
			if self.menu == 0:
				if self.pos[1]==0:
					self.pos[1]=5
				else:
					self.pos[1]-=1
			elif self.menu == 1:
				if self.subPos==0:
					self.subPos=1
				else:
					self.subPos-=1
			self.move=0.0

	## Move the cursor down.
	def SelDown(self):
		if self.move>=.25:
			if self.menu == 0:
				if self.pos[1]>=5:
					self.pos[1]=0
				else:
					self.pos[1]+=1
			elif self.menu == 1:
				if self.subPos==1:
					self.subPos=0
				else:
					self.subPos+=1
			self.move=0.0

	## Move the cursor left.
	def SelLeft(self):
		if self.move>=.25:
			if self.menu == 0:
				if self.pos[0]==0:
					self.pos[0]=self.invenSizeX-1
				else:
					self.pos[0]-=1
			self.move=0.0

	## Move the cursor right.
	def SelRight(self):
		if self.move>=.25:
			if self.menu == 0:
				if self.pos[0]>=self.invenSizeX-1:
					self.pos[0]=0
				else:
					self.pos[0]+=1
			self.move=0.0

	## Selects the current item.
	def Select(self):
		if self.menu == 0:
			if (self.pos[1]*self.invenSizeX)+self.pos[0]< len(self.shop):
				self.menu = 1
				self.sel = self.shop[(self.pos[1]*self.invenSizeX)+self.pos[0]]
		elif self.menu == 1:
			if self.subPos == 0:
				if self.player.getInventory().getGold()>=self.sel.getValue():
					if self.player.getInventory().addItem(self.sel):
						self.player.getInventory().spendGold(self.sel.getValue())
						self.menu = 0
					else:
						self.menu = 3
				else:
					self.menu = 2
			elif self.subPos == 1:
				self.menu = 0
		elif self.menu == 2:
			self.menu = 0
		elif self.menu == 3:
			self.menu = 0

	## Goes back one menu.
	def Cancel(self):
		if self.menu == 2:
			self.menu = 0
		else:
			Menu.Cancel(self)

	## Draws the menu
	def draw(self,screen):
		screen.fill(config.ColorDark,[self.winX,14,self.winSizeX,212])
		screen.fill(config.Color,[self.winX+1,30,self.winSizeX-2,180])	#Main Window
		screen.fill(config.Color,[self.winX+1,16,self.winSizeX-2,12])	#Area Name Window
		screen.fill(config.Color,[self.winX+1,212,self.winSizeX-2,12])	#Status Window

		screen.blit(font.render("Buy",False,config.ColorFont),[self.winX+6,18])
		screen.blit(font.render("Gold: "+self.player.getInventory().getGoldS()+"G",False,config.ColorFont),[self.winX+self.winSizeX-61,18])

		for x in range(0,self.invenSizeX):
			for y in range(0,6):
				screen.blit(Icons.iconBG,[self.winX+9+(x*30),33+(y*30)])

		x=0
		y=0
		for item in self.shop:
			screen.blit(item.getSprite(),[self.winX+9+(x*30),33+(y*30)])
			pItem = self.player.getInventory().hasItem(item)
			if pItem != None:
				amt = pItem.getAmount()
			else:
				amt = 0
			screen.blit(font.render(str(amt),False,config.ColorFont),[(x*30)+self.winX+28-font.size(str(item.getAmount()))[0],(y*30)+47])
			if self.pos == [x,y]:
				self.status=item.getName()+ ": "+str(item.getValue())+"G"
			x+=1
			if x >= self.invenSizeX:
				y+=1
				x =0

		if self.menu == 1:
			screen.fill((config.ColorDark),[self.winX+2+(self.pos[0]*30),59+(self.pos[1]*30),40,26])
			screen.fill((config.Color),[self.winX+3+(self.pos[0]*30),60+(self.pos[1]*30),38,24])

			if self.subPos==0:
				screen.blit(font.render("Buy",False,config.ColorSel),[self.winX+5+(self.pos[0]*30),61+(self.pos[1]*30)])
			else:
				screen.blit(font.render("Buy",False,config.ColorFont),[self.winX+5+(self.pos[0]*30),61+(self.pos[1]*30)])
			if self.subPos==1:
				screen.blit(font.render("Cancel",False,config.ColorSel),[self.winX+5+(self.pos[0]*30),73+(self.pos[1]*30)])
			else:
				screen.blit(font.render("Cancel",False,config.ColorFont),[self.winX+5+(self.pos[0]*30),73+(self.pos[1]*30)])

			if self.sel.getType()=="Equipment":
				self.status=""
				for stat in self.sel.getStats():
					statVal = self.sel.getStats()[stat]
					comp = self.player.getInventory().getComparison(self.sel,stat)
					if comp>0:
						comp="+"+str(comp)
					else:
						comp=str(comp)
					if statVal>0:
						self.status+= stat+": +"+str(statVal)+"("+comp+"), "
					else:
						self.status+= stat+": "+str(statVal)+"("+comp+"), "
				self.status = self.status.rstrip(", ")
			else:
				self.status=self.sel.getLongDescription()

		screen.blit(scrollText(self.status,self.winSizeX-12,self.statusScroll),[self.winX+6,214])
		if self.statusScroll>font.size(self.status)[0]-80:
			self.statusScroll=-30

		screen.blit(Icons.cursor,[self.winX+9+(self.pos[0]*30),33+(self.pos[1]*30)])
		temp=Icons.cursorBlink.copy()
		temp.fill((255,255,255,abs(int(self.blink*255))),special_flags=BLEND_RGBA_MULT)
		screen.blit(temp,[self.winX+9+(self.pos[0]*30),33+(self.pos[1]*30)])

		if self.menu == 2:
			screen.fill((config.ColorDark),[77,59,166,26])
			screen.fill((config.Color),[78,60,164,24])

			screen.blit(font.render("You don't have enough money!",False,config.ColorFont),[80,61])
			screen.blit(font.render("Ok",False,config.ColorSel),[153,73])
		if self.menu == 3:
			screen.fill((config.ColorDark),[77,59,166,26])
			screen.fill((config.Color),[78,60,164,24])

			screen.blit(font.render("You don't have enough space!",False,config.ColorFont),[80,61])
			screen.blit(font.render("Ok",False,config.ColorSel),[153,73])

	def update(self,screen,tick):
		self.status=""
		self.move+=tick
		self.blink+=tick
		self.statusScroll+=tick*20
		self.selScroll+=tick*20
		if self.blink >=1:
			self.blink=-1

		self.draw(screen)

		return self.close

## Menu for selling things in shops.
class ShopSellMenu(Menu):

	## Constructor
	#  @param player The player's player.Player() reference.
	def __init__(self,player):
		self.player=player

		# Constants:

		## The X position of this window's origin.
		self.winX = 64									#Old = 89
		## The X portion of this window's size.
		self.winSizeX = 192								#Old = 132
		## How many item slots there are in a row.
		self.invenSizeX = (self.winSizeX/30)

		#**********#

		self.pos=[0,0]
		self.menu=0		#Which sub-menu is open
		self.subPos=0	#Sub-menu cursor position
		self.sel=None	#Selected Item
		self.move=0.0	#time since cursor last moved
		self.blink=0.0	#time since cursor last blinked
		#self.size=player.getInventory().getSize()

		self.status=""
		self.statusScroll=0.0
		self.selScroll=0.0

		self.close=False

	## Move the cursor up.
	def SelUp(self):
		if self.move>=.25:
			if self.menu == 0:
				if self.pos[1]==0:
					self.pos[1]=5
				else:
					self.pos[1]-=1
			elif self.menu == 1:
				if self.subPos==0:
					self.subPos=1
				else:
					self.subPos-=1
			self.move=0.0

	## Move the cursor down.
	def SelDown(self):
		if self.move>=.25:
			if self.menu == 0:
				if self.pos[1]>=5:
					self.pos[1]=0
				else:
					self.pos[1]+=1
			elif self.menu == 1:
				if self.subPos==1:
					self.subPos=0
				else:
					self.subPos+=1
			self.move=0.0

	## Move the cursor left.
	def SelLeft(self):
		if self.move>=.25:
			if self.menu == 0:
				if self.pos[0]==0:
					self.pos[0]=self.invenSizeX-1
				else:
					self.pos[0]-=1
			self.move=0.0

	## Move the cursor right.
	def SelRight(self):
		if self.move>=.25:
			if self.menu == 0:
				if self.pos[0]>=self.invenSizeX-1:
					self.pos[0]=0
				else:
					self.pos[0]+=1
			self.move=0.0

	## Selects the current item.
	def Select(self):
		if self.menu == 0:
			if (self.pos[1]*self.invenSizeX)+self.pos[0]< len(self.player.getInventory().getItems()):
				self.menu = 1
				self.sel = self.player.getInventory().getItems()[(self.pos[1]*self.invenSizeX)+self.pos[0]]
		elif self.menu == 1:
			if self.subPos == 0:
				if self.sel.getValue()>=0:
					self.player.getInventory().addGold(self.sel.getValue())
					self.sel.setAmount(self.sel.getAmount()-1)
					if self.sel.getAmount() <= 0:
						self.player.getInventory().remove(self.sel)
					self.menu = 0
				else:
					self.menu = 2
			elif self.subPos == 1:
				self.menu = 0
		elif self.menu == 2:
			self.menu = 0

	## Goes back one menu.
	def Cancel(self):
		if self.menu == 2:
			self.menu = 0
		else:
			Menu.Cancel(self)

	## Draws this menu on the screen.
	def draw(self,screen):
		screen.fill(config.ColorDark,[self.winX,14,self.winSizeX,212])
		screen.fill(config.Color,[self.winX+1,30,self.winSizeX-2,180])	#Main Window
		screen.fill(config.Color,[self.winX+1,16,self.winSizeX-2,12])	#Area Name Window
		screen.fill(config.Color,[self.winX+1,212,self.winSizeX-2,12])	#Status Window

		screen.blit(font.render("Sell",False,config.ColorFont),[self.winX+6,18])
		screen.blit(font.render("Gold: "+self.player.getInventory().getGoldS()+"G",False,config.ColorFont),[self.winX+self.winSizeX-61,18])

		for x in range(0,self.invenSizeX):
			for y in range(0,6):
				screen.blit(Icons.iconBG,[self.winX+9+(x*30),33+(y*30)])

		x=0
		y=0
		for item in self.player.getInventory().getItems():
			screen.blit(item.getSprite(),[self.winX+9+(x*30),33+(y*30)])
			if item.getAmount()>1:
				screen.blit(font.render(str(item.getAmount()),False,config.ColorFont),[(x*30)+self.winX+31-font.size(str(item.getAmount()))[0],(y*30)+47])
			if self.pos == [x,y]:
				if item.getValue()>=0:
					self.status=item.getName()+ ": "+str(item.getValue())+"G"
				else:
					self.status=item.getName()+ ": N/A"
			x+=1
			if x >= self.invenSizeX:
				y+=1
				x =0

		if self.menu == 1:
			screen.fill((config.ColorDark),[self.winX+2+(self.pos[0]*30),59+(self.pos[1]*30),40,26])
			screen.fill((config.Color),[self.winX+3+(self.pos[0]*30),60+(self.pos[1]*30),38,24])

			if self.subPos==0:
				screen.blit(font.render("Sell",False,config.ColorSel),[self.winX+5+(self.pos[0]*30),61+(self.pos[1]*30)])
			else:
				screen.blit(font.render("Sell",False,config.ColorFont),[self.winX+5+(self.pos[0]*30),61+(self.pos[1]*30)])
			if self.subPos==1:
				screen.blit(font.render("Cancel",False,config.ColorSel),[self.winX+5+(self.pos[0]*30),73+(self.pos[1]*30)])
			else:
				screen.blit(font.render("Cancel",False,config.ColorFont),[self.winX+5+(self.pos[0]*30),73+(self.pos[1]*30)])

			if self.sel.getType()=="Equipment":
				self.status=""
				for stat in self.sel.getStats():
					statVal = self.sel.getStats()[stat]
					comp = self.player.getInventory().getComparison(self.sel,stat)
					if comp>0:
						comp="+"+str(comp)
					else:
						comp=str(comp)
					if statVal>0:
						self.status+= stat+": +"+str(statVal)+"("+comp+"), "
					else:
						self.status+= stat+": "+str(statVal)+"("+comp+"), "
				self.status = self.status.rstrip(", ")
			else:
				self.status=self.sel.getLongDescription()

		screen.blit(scrollText(self.status,self.winSizeX-12,self.statusScroll),[self.winX+6,214])
		if self.statusScroll>font.size(self.status)[0]-80:
			self.statusScroll=-30

		screen.blit(Icons.cursor,[self.winX+9+(self.pos[0]*30),33+(self.pos[1]*30)])
		temp=Icons.cursorBlink.copy()
		temp.fill((255,255,255,abs(int(self.blink*255))),special_flags=BLEND_RGBA_MULT)
		screen.blit(temp,[self.winX+9+(self.pos[0]*30),33+(self.pos[1]*30)])

		if self.menu == 2:
			screen.fill((config.ColorDark),[93,59,139,26])
			screen.fill((config.Color),[94,60,137,24])
			screen.blit(font.render("Sorry, I can't buy that!",False,config.ColorFont),[96,61])
			screen.blit(font.render("Ok",False,config.ColorSel),[146,73])

	def update(self,screen,tick):
		self.status=""
		self.move+=tick
		self.blink+=tick
		self.statusScroll+=tick*20
		self.selScroll+=tick*20
		if self.blink >=1:
			self.blink=-1

		self.draw(screen)

		return self.close
