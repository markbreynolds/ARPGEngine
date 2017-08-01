## @package main
#  Documentation for the Core Module.
#
#  This module contains the code related to the core and other module integration.
#
#  Please note that these goals are exactly that. They may or may not ever actually
#  be implemented.
#
## Goals: V 0.1.0a - Done
#
#    -# GUI - Done
#      - Inventory Tab - Done
#      - Party Tab - Done
#      - Migrate Character Creation - Done
#    -# Battle - Done
#      - Dynamic Weapons - Done
#      - HUD - Done
#    -# Triggers - Done
#      - Battle Trigger - Done
#    -# Documentation - Done
#      - package documentation for Triggers - Done
#      - package documentation for Graphics - Done
#      - package documentation for Battle - Done
#      - All new code must be documented as it is written.
#
##Goals: V 0.2.0a - Done
#    -# Player - Done
#      - Class Objects - Done
#    -# GUI - Done
#      - Pause/Main %Menu - Done
#      - Shops - Done
#    -# Make A Town - Done
#      - Shop - Done
#      - Inn - Done
#    -# Overworld - Done
#      - Fix Pushables (Press button for push) - Done
#      - Random Monster Encounters - Done
#    -# Battle - Done
#      - Battle Transistion - Done
#      - Abilities - Done
#    -# Dialog - Done
#      - Quest Add - Done
#      - Quest Update - Done
#      - Quest Check Branches - Done
#      - Item Check Branches - Done
#      - Predialog Branch - Done
#    -# <b>Quests</b>
#      - Talk-To Quests - Done
#      - Fetch Quests - Done
#	   - Go-To Quests - Done
#    -# Triggers - Done
#      - Quest Complete Trigger - Done
#    -# Documentation - Done
#      - package documentation for Game Engine - Done
#      - package documentation for Player - Done
#      - All new code must be documented as it is written.
#
## Goals: V 0.3.0a - Done
#    -# Triggers - Done
#      - Dialog Trigger - Done
#    -# <b>Skills</b>
#      - Melee Skills - Done
#      - Stat Skills - Done
#      - Buff Skills - Done
#      - Warrior Skills (5) - Done
#    -# Battle - Done
#      - Bow Weapon Style - Done
#    -# Enemies - Done
#      - Redo Slime Animations - Done
#    -# Items - Done
#      - Swords (3) - Done
#    -# <b>GUI</b>
#      - Version Number on Title Screen - Done
#    -# Documentation - Done
#      - package documentation for Game Object, Pushables, etc. - Done
#      - package documentation for NPC - Done
#      - All new code must be documented as it is written.
#
## Goals: V 0.4.0a
#    -# <b>Battle</b>
#      - <b>Physics</b>
#      - <b>Staff Weapon Style</b>
#    -# <b>Skills</b>
#      - <b>Archer Skills (5)</b>
#    -# <b>Items</b>
#      - <b>Bows (3)</b>
#    -# <b>Enemies</b>
#      - <b>Bat</b>
#      - <b>Abilities</b>
#      - <b>Slime Ability<b>
#    -# <b>Documentation</b>
#      - <b>package documentation for Items</b>
#      - <b>package documentation for Level</b>
#      - All new code must be documented as it is written.
#
## Goals: V 0.5.0a
#    -# <b>Skills</b>
#      - <b>Passive Skills</b>
#      - <b>Targeted Skills</b>
#      - <b>Mage Skills (5)</b>
#    -# <b>Items</b>
#      - <b>Staffs (3)</b>
#    -# <b>Enemies</b>
#      - <b>Skeleton</b>
#    -# <b>Sound</b>
#      - <b>Support background music</b>
#      - <b>Title BGM</b>
#      - <b>Village BGM</b>
#      - <b>Dungeon BGM</b>
#    -# <b>Saving</b>
#    -# <b>GUI</b>
#      - <b>Add Options</b>
#      - <b>Quiting Warning</b>
#      - <b>World Map</b>
#    -# <b>Documentation</b>
#      - <b>package documentation for GUI</b>
#      - All new code must be documented as it is written.
#
## Goals: V1.0.0a
#    -# <b>Enemies</b>
#      - <b>Skeleton Archer</b>
#      - <b>Bat Ability</b>
#      - <b>Skeleton Ability</b>
#    -# <b>Sound</b>
#      - <b>Support SFX</b>
#      - <b>Walking sounds</b>
#      - <b>Weapon sounds</b>
#      - <b>Monster sounds</b>
#    -# <b>Loading Save Files</b>
#
## Goals: Future
### Multiplayer Update:
#    -# <b>Overworld</b>
#      - <b>Network Objects</b>
#    -# <b>Battles</b>
#      - <b>Network Objects</b>
#    -# <b>Multiplayer</b>
#      - <b>In-Game Hosting</b>
#      - <b>Dedicated Server</b>
### Crafting Update:
#    -# <b>Overworld</b>
#      - <b>Harvestable Items</b>
#      - <b>Object Appearance Chance</b>
#    -# <b>GUI</b>
#      - <b>Crafting Menu</b>
#      - <b>Harvesting Dialog</b>
#    -# <b>Items</b>
#      - <b>Runtime Defined Items</b>
### Battle Update:
#    -# <b>Battle</b>
#      - <b>Block Attacks</b>
#      - <b>Dodge Attacks</b>
#      - <b>Jumping</b>
#      - <b>Aerial Attacks</b>
### Dungeon Update:
#    -# <b>GUI</b>
#      - <b>Minimap</b>
#    -# <b>A Dungeon</b>
#      - <b>Chests</b>
#      - <b>Puzzles</b>
#      - <b>Cutscene</b>
#      - <b>Mini Boss</b>
#      - <b>Boss</b>
### Cutscene Update:
#    -# <b>Triggers</b>
#      - <b>Cutscene Trigger</b>
#      - <b>QuestStateChange Trigger?</b>
#      - <b>Trigger Effect Classes</b>
#    -# <b>Cutscenes</b>
#      - <b>Actions</b>
#      - <b>Dialog</b>
#      - <b>Actions/Dialog Sync</b>
### Tools Update:
#    -# <b>Animation Editor</b<
#      - <b>View Animations</b>
#      - <b>Change Animation Parameters</b>
#      - <b>Basic Sprite Editing</b>
#    -# <b>Dialog Editor</b>
#    -# <b>Level Editor</b>
#    -# <b>Cutscene Editor</b>
### Misc Update:
#    -# <b>Compositor</b>
#      - <b>VFX</b>
#      - <b>Filter</b>
#    -# <b>Level</b>
#      - <b>Improve load times</b>
#    -# <b>Notifications</b>
#      - <b>Quest Notifications</b>
#      - <b>Item Get Notifications</b>
#      - >b>Party Change Notifications?</b>
### Test Update:
#    -# <b>Unit Tests</b>
#      - <b>InputEngine?</b>
#      - <b>GameEngine</b>
#      - <b>BattleEngine</b>
#      - <b>Player</b>
#      - <b>Level</b>
#      - <b>GraphicsEngine?</b>
#      - <b>BattleGraphicsEngine?</b>
#

import random
import pygame
from pygame.locals import *

pygame.init()

#import game
import input as Input
import errors
import config
from game.engine import GameEngine
from game.items.factory import ItemFactory
from game import level
from game import player
from battle.engine import BattleEngine
from battle.enemies.factory import EnemyFactory
from graphics import transitions
from graphics.scaled_screen import ScaledScreen
from graphics.overworld import GraphicsEngine
from graphics.battle import BattleGraphicsEngine, BattleGraphicObject
from graphics.gui import MainMenu, CharacterCreator, Icons

from game import npc
from battle.jobs.job import Warrior

"""
## Goals: V 0.2.0
#
#    -# Player
#      - Class Objects
#    -# GUI
#      - Pause/Main %Menu
#      - Shops
#    -# Battle
#      - Abilities
#      - Physics
#    -# Compositor
#      - VFX
#      - Filter
#    -# A Town
#      - Shop
#      - Inn
#      - Tavern
#    -# <b>Documentation</b>
#      - All new code must be documented as it is written.
"""

def loadNewArea(xml,Level):
	global gameEngine
	global graphicsEngine
	global clock

	gameEngine.clearActors()
	gameEngine.clearNPCs()
	gameEngine.clearTriggers()
	graphicsEngine.clearObjects()
	level.load(xml,Level,gameEngine,graphicsEngine)
	clock.tick()

def battleStart(Enemies,bg,farBG):
	global graphicsEngine
	global graphicsEngineB
	global battleEngine
	global Player
	global PlayerB
	global BATTLING

	graphicsEngineB = BattleGraphicsEngine(graphicsEngine.getScreen(),graphicsEngine.getIsScaled(),bg,farBG)
	battleEngine = BattleEngine(graphicsEngineB)
	PlayerB = Player.getBattleObject()

	x = len(Player.getParty())*50
	PlayerB.setX(x)
	PlayerB.setState("Idle")
	PlayerB.setDirection(1)
	PlayerB.playerStatus = True

#	if Player.getInventory().getArm1()!=None and PlayerB.getGraphicObject().weapon!=None:
#		if Player.getInventory().getArm1().getStyle() != PlayerB.getGraphicObject().weapon.getStyle():
#			PlayerB.updateWeapon(Player.getInventory().getArm1(),Player.constructBattleAnimations())
#	else:
#		if Player.getInventory().getArm1() != PlayerB.getGraphicObject().weapon:
#			PlayerB.updateWeapon(Player.getInventory().getArm1(),Player.constructBattleAnimations())
	PlayerB.updateWeapon(Player.getInventory().getArm1(),Player.constructBattleAnimations())

	battleEngine.addAlly(PlayerB)
	for ally in Player.getParty():
		x-=50
		allyb = ally.getBattleObject()
		allyb.setX(x)
		allyb.setState("Idle")
		allyb.setDirection(1)
		battleEngine.addAlly(allyb)

	x = 800
	for enemy in Enemies:
		if config.Difficulty <= 2:
			lvl = max(PlayerB.getLevel()+random.randint(-4,2),1)
		elif config.Difficulty == 3:
			lvl = max(PlayerB.getLevel()+random.randint(-2,4),1)
		elif config.Difficulty >= 4:
			lvl = max(PlayerB.getLevel()+random.randint(0,6),1)
		print lvl
		temp = EnemyFactory.createEnemy(enemy,lvl,x)
		battleEngine.addEnemy(temp)
		x-= 50

	graphicsEngineB.setFocus(PlayerB.getGraphicObject())
	graphicsEngineB.getHud().update(battleEngine.playerParty)

	BATTLING = True

	oldScreen = screen.screen.copy()
	battleEngine.update(0)
	newScreen = screen.screen.copy()
	transitions.blurTrans(clock,screen,oldScreen,newScreen)

screen = ScaledScreen(pygame.display.set_mode((640,480)),640,480)
#screen = ScaledScreen(pygame.display.set_mode((320,240)),320,240)
font = pygame.font.SysFont("Arial",12)
clock = pygame.time.Clock()
clock.tick()

gameEngine = GameEngine(loadNewArea,battleStart)
graphicsEngine = GraphicsEngine(screen,True)
inputEngine = Input.InputEngine()
errors.init(screen,level=config.LogVerbosity,quiet=False)

pygame.key.set_repeat(250,100)

Icons.load()

#allies=[player.Player("Markus Clarkus ",3,1,[0,255,255],1,[0,255,127],False).getBattleObject(),player.Player("Clark",3,1,[0,255,255],1,[0,255,127],False).getBattleObject()]
#enemies=[enemies.GreenSlime(1,100)]
#battle.BattleTest(screen,allies,enemies)

options = [["Levels/TestArea/Test.xml","Test1"],["Levels/TestArea/Test.xml","Test3"],["Levels/TestArea/TestVillage.xml","VillageMain"]]
choice = random.choice(options)
choice = ["Levels/TestArea/TestVillage.xml","VillageMain"]
#choice = ["Levels/TestArea/Test.xml","Test1"]
level.load(choice[0],choice[1],gameEngine,graphicsEngine)

transitions.fadeFromColor(screen,screen.screen.copy(),[0,0,0],.5)

menu = MainMenu()
while menu:
	for inp in inputEngine.getInput():
		if inp[0] == "Quit":
			pygame.quit()
			exit()
		elif inp[1] == "Down":
			if inp[0] == "Accept":
				menu.Select()
			elif inp[0] == "Cancel":
				menu.Cancel()

	move = inputEngine.getMove()
	if move[0]:
		menu.SelUp()
	if move[1]:
		menu.SelRight()
	if move[2]:
		menu.SelDown()
	if move[3]:
		menu.SelLeft()

	tick = clock.tick()/1000.0
	for item in gameEngine.actors:
		item.update(tick,gameEngine.moveCheck)
	for item in gameEngine.NPCs:
		item.update(tick,gameEngine.moveCheck)
	screen.blit(graphicsEngine.background,[0,0])
	for item in graphicsEngine.objects:
		item.update(tick)
		screen.blit(item.getSprite(),item.getPos())
	menu.update(screen,tick)

	if menu.closed():
		val = menu.getValue()
		if val == "Play":
			Player = menu.getPlayer()
			menu = False
		elif val == "New Single":
			menu = CharacterCreator(player.Player,inputEngine.setDump(True))
		elif val == "Exit":
			pygame.quit()
			exit()
		elif val == "Main":
			menu = MainMenu()


	screen.update()
	pygame.display.update()


#loadNewArea("Levels/TestArea/TestVillage.xml","VillageMain");Player.getGameObject().setPos([400,550])
#loadNewArea("Levels/TestArea/TestVillage.xml","VillageInn");Player.getGameObject().setPos([100,100])
loadNewArea("Levels/TestArea/Test.xml","Test1");Player.getGameObject().setPos([100,100])
graphicsEngine.setPlayer(Player.getGraphicObject())
gameEngine.setPlayer(Player.getGameObject())

#gui.debugInfo=graphics.TextObject("",[0,0])
#gui.debugInfo.layer = 2
#debugInfo = graphics.GraphicObject([[[pygame.image.load("sObjects/Lever1W1.png").convert_alpha()]]],[0.1])
#fpsCount = 1.0
#fps = []
#graphicsEngine.debug=gui.debugInfo

graphicsEngine.setFocus(Player.getGraphicObject())

Player.party.append(npc.BattleNPC("Jeorge",Warrior(1),1,(255,0,0),1,(255,127,0)))
Player.party.append(npc.BattleNPC("George",Warrior(1),1,(0,0,255),1,(0,127,255)))
Player.party.append(npc.BattleNPC("Jeorge",Warrior(1),1,(255,0,0),1,(255,127,0)))
Player.party.append(npc.BattleNPC("George",Warrior(1),1,(0,0,255),1,(0,127,255)))
Player.party.append(npc.BattleNPC("Jeorge",Warrior(1),1,(255,0,0),1,(255,127,0)))
#Player.party[1].getBattleObject().HpM = 1000
#Player.party[0].getBattleObject().ai = enemies.WandererAI(20,100)
#Player.party[1].getBattleObject().ai = enemies.WandererAI(20,100)
Player.party[0].getInventory().equip(ItemFactory.createItem("IronShortSword"))

PLAYING=True
BATTLING = False
pygame.key.set_repeat()

while PLAYING:
	tick = clock.tick(60)/1000.0
	if BATTLING:
		for event in inputEngine.getInput(tick):
			if event[0] == "Quit":
				PLAYING = False
			elif event[1] == "Down":
				if event[0] == "Accept":
					if PlayerB.getHP()>0:
						PlayerB.attack()
				elif event[0] == "Cancel":
					if PlayerB.getGraphicObject().currentAnimation.getNextAnimation() != None:
						errors.info(PlayerB.getGraphicObject().currentAnimation.getName()+", "+PlayerB.getGraphicObject().currentAnimation.getNextAnimation().getName())
					else:
						errors.info(PlayerB.getGraphicObject().currentAnimation.getName()+", None") #+PlayerB.getGraphicObject().currentAnimation.getNextAnimation())
				elif event[0].startswith("S1"):
					if Player.getSkill(event[0])!=None:
						PlayerB.useSkill(Player.getSkill(event[0]))
#					if Player.getSkill(event[0])!=None and Player.getSkill(event[0]).getType()=="Projectile":
#						proj = Player.getSkill(event[0]).use(PlayerB)
#						if proj:
#							battleEngine.addProjectile(proj)
			elif event[1] == "Up":
				if event[0] == "Accept":
					PlayerB.release(BattleGraphicObject)
		move=inputEngine.getMove()
		if move[1]:
			if PlayerB.getDirection()!=1:
				PlayerB.setDirection(1)
			if PlayerB.getState()=="Idle":
				PlayerB.setState("Run")
		if move[3]:
			if PlayerB.getDirection()!=0:
				PlayerB.setDirection(0)
			if PlayerB.getState()=="Idle":
				PlayerB.setState("Run")
		if (not move[1] and not move[3]) or (move[1] and move[3]):
			if PlayerB.getState()=="Run":
				PlayerB.setState("Idle")

		#battleEngine.getGraphicsEngine().setDebugInfo(str(PlayerB.graphicObject.state)+":"+str(PlayerB.graphicObject.getFrame()))
		battleEngine.getGraphicsEngine().setDebugInfo("BufDef:"+str(PlayerB.statBuffOffsets["Def"]))

		if battleEngine.update(tick):
			BATTLING = False
			loot = []
			for item in battleEngine.getLoot():
				loot.append(ItemFactory.createItem(item))
			battleEngine.getGraphicsEngine().victoryScreen(clock,inputEngine,battleEngine.getPlayerParty(),battleEngine.getGold(),battleEngine.getExp(),loot)
			oldScreen = screen.copy()
			graphicsEngine.update(0)
			newScreen = screen.copy()
			transitions.blurTrans(clock,screen,oldScreen,newScreen)
			Player.getInventory().addGold(battleEngine.getGold())
			for item in loot:
				Player.getInventory().addItem(item)
			for ally in battleEngine.getPlayerParty():
				ally.addExp(battleEngine.getExp())
	else:	#Overworld
		for inp in inputEngine.getInput():
			if inp[0] == "Quit":
				PLAYING = False
			elif inp[1] == "Down":
				if graphicsEngine.getInven() == False and graphicsEngine.getPause() == False and graphicsEngine.getShop() == False:
					if inp[0] == "Accept":
						if Player.getTalking():
							graphicsEngine.getTalking().Cont()
						else:
							gameEngine.interact(Player.getGameObject())
				elif graphicsEngine.getPause():
					if inp[0] == "Accept":
						graphicsEngine.getPause().Select()
					elif inp[0] == "Cancel":
						graphicsEngine.getPause().Cancel()
				elif graphicsEngine.getShop():
					if inp[0] == "Accept":
						graphicsEngine.getShop().Select()
					elif inp[0] == "Cancel":
						graphicsEngine.getShop().Cancel()
				else:
					if inp[0] == "Accept":
						graphicsEngine.getInven().Select()
					elif inp[0] == "Cancel":
						graphicsEngine.getInven().Cancel()
				if not Player.getTalking():
					if inp[0] == "Inven":
						graphicsEngine.toggleInven()
					if inp[0] == "Pause":
						graphicsEngine.togglePause()


		#tmp = None
		#for actor in gameEngine.Actors:
		#	if actor.ID == "Gate":
		#		tmp = actor
		#gui.debugInfo.setText(str(tmp.graphicObject.state)+":"+str(tmp.graphicObject.getFrame()))

		#gui.debugInfo.setText(str(Player.getGraphicObject().getPos()))
		#gui.debugInfo.setText(str(gameEngine.actors))

		#Average Framerate:
		#fpsCount -= tick
		#if fpsCount >0:
		#	fps.append(clock.get_fps())
		#else:
		#	fpsCount = 1.0
		#	gui.debugInfo.setText(str(sum(fps)/len(fps)))
		#	fps = []

		move = inputEngine.getMove()
		if graphicsEngine.getTalking():
			if move[0]:
				graphicsEngine.getTalking().SelUp()
			if move[2]:
				graphicsEngine.getTalking().SelDown()
		elif graphicsEngine.getPause():
			if move[0]:
				graphicsEngine.getPause().SelUp()
			if move[1]:
				graphicsEngine.getPause().SelRight()
			if move[2]:
				graphicsEngine.getPause().SelDown()
			if move[3]:
				graphicsEngine.getPause().SelLeft()
		elif graphicsEngine.getInven():
			if move[0]:
				graphicsEngine.getInven().SelUp()
			if move[1]:
				graphicsEngine.getInven().SelRight()
			if move[2]:
				graphicsEngine.getInven().SelDown()
			if move[3]:
				graphicsEngine.getInven().SelLeft()
		elif graphicsEngine.getShop():
			if move[0]:
				graphicsEngine.getShop().SelUp()
			if move[1]:
				graphicsEngine.getShop().SelRight()
			if move[2]:
				graphicsEngine.getShop().SelDown()
			if move[3]:
				graphicsEngine.getShop().SelLeft()
		elif Player.getCanMove():
			if move[0]:
				Player.setDirection(0)
			if move[2]:
				Player.setDirection(2)
			if move[1]:
				Player.setDirection(1)
			if move[3]:
				Player.setDirection(3)

			dire = inputEngine.getDirection()
			Player.getGameObject().setDirection(dire)

		if sum(move)!=0 and not Player.getGameObject().getMoving() and not graphicsEngine.getTalking() and not graphicsEngine.getInven() and not graphicsEngine.getPause() and not graphicsEngine.getShop():
			Player.setState("Walk")
			Player.getGraphicObject().setFrame(1)
			Player.getGameObject().setMoving(True)
		elif (sum(move)==0 and Player.getGameObject().getMoving()) or graphicsEngine.getTalking() or graphicsEngine.getInven() or graphicsEngine.getPause() or graphicsEngine.getShop():
			Player.setState("Idle")
			Player.getGameObject().setMoving(False)


		#tick = clock.tick()/1000.0

		if graphicsEngine.getTalking()==None and Player.getTalking():
			graphicsEngine.setTalking(Player.getTalking())
		elif graphicsEngine.getTalking()==False and Player.getTalking():
			graphicsEngine.resetTalking()
			Player.setTalking(False)

		if graphicsEngine.getPause():
			if graphicsEngine.getPause().closed():
				if graphicsEngine.getPause().getValue() == "Exit":
					PLAYING = False
				elif graphicsEngine.getPause().getValue() == "Resume":
					graphicsEngine.togglePause()

		if graphicsEngine.getSleep():
			gameEngine.sleep()
			graphicsEngine.resetSleep()

		if graphicsEngine.getTrigger():
			gameEngine.trigger(graphicsEngine.getTrigger())
			graphicsEngine.resetTrigger()

		if graphicsEngine.getQuest():
			gameEngine.questAction(graphicsEngine.getQuest())
			graphicsEngine.resetQuest()

		if graphicsEngine.getBranch():
			graphicsEngine.dialogBranch(gameEngine.branchCheck(graphicsEngine.getBranch()))

		gameEngine.update(tick)
		graphicsEngine.update(tick)

#Exit code:
pygame.quit()
exit()
