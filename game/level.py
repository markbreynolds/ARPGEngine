#level.py
#
# Current level loader appears to be very ineffiecent...
# Caching things like object images and level backgrounds would probably be a good idea.

import json
import time

import pygame

#from graphics import GraphicObject,Animation,AnimationFrame,loadAnimation
#from game import GameObject,Pushable
from game.engine import GameObject, Pushable
from graphics.animation import Animation, AnimationFrame, loadAnimation
from graphics.overworld import GraphicObject
from game.npc import NPC,sNPC,Dialog
from game import triggers
import errors
import config

def loadXML(xmlPath,level,GameEngine,GraphicEngine):
	errors.info("Loading level: "+level)
	totalStart = time.time()

	try:
		filer = open(xmlPath,"r")
	except IOError:
		errors.critical("Level file not found.")
		exit()

	lines = filer.readlines()

	started=False

	levelData = []

	for i in range(len(lines)):	#Strip Tabs and New Lines
		lines[i] = lines[i].lstrip("\t").rstrip("\n")

	for line in lines:	#Extract Level Data
		if not started:
			if line == "<Level "+level+">":
				started=True
			continue
		if line == "</Level>":
			break
		levelData.append(line)

	Name=None
	BG = None
	Mask=None
	Enemies=None
	BattleBG=None
	BattleFBG=None
	Triggers = []
	GameObjects = []
	NPCs = []
	i = 0

	start = time.time()
	while i < len(levelData):	#Isolate Triggers, NPCs, and GameObjects (GraphicObjects must be dealt with immediately because they are contained within GameObjects)
		temp = {}
		if levelData[i].startswith("<LevelName>"):
			Name=levelData[i].lstrip("<LevelName").lstrip(">").rstrip("/LevelName>").rstrip("<")
		elif levelData[i].startswith("<Background>"):
			BG=levelData[i].lstrip("<Background").lstrip(">").rstrip("/Background>").rstrip("<")
		elif levelData[i].startswith("<Mask>"):
			Mask=levelData[i].lstrip("<Mask").lstrip(">").rstrip("/Mask>").rstrip("<")
		elif levelData[i].startswith("<Enemies>"):
			Enemies = json.loads(levelData[i].lstrip("<Enemies").lstrip(">").rstrip("/Enemies>").rstrip("<"))
		elif levelData[i].startswith("<BattleBG>"):
			BattleBG = json.loads(levelData[i].lstrip("<BattleBG").lstrip(">").rstrip("/BattleBG>").rstrip("<"))
		elif levelData[i]=="<Trigger>":
			n=1
			while levelData[i+n]!="</Trigger>":
				key = levelData[i+n][1:levelData[i+n].find(">")]
				value = levelData[i+n][levelData[i+n].find(">")+1:levelData[i+n].find("<",levelData[i+n].find(">"))]
				temp[key]=json.loads(value)
				n+=1
			Triggers.append(temp)
			i+=n
		elif levelData[i].startswith("<GameObject"):
			path = levelData[i].lstrip("<GameObject").rstrip(">").lstrip(" ").split(" ")[0]
			if len(levelData[i].lstrip("<GameObject").rstrip(">").lstrip(" ").split(" "))>1:
				objectName = levelData[i].lstrip("<GameObject").rstrip(">").lstrip(" ").split(" ")[1]
			if path != "":
				tempFiler = file(config.AssetPath+path,"r")
				lines = tempFiler.readlines()
				started=False
				for j in range(len(lines)):	#Strip Tabs and New Lines
					lines[j] = lines[j].lstrip("\t").rstrip("\n")
				j=1
				for line in lines:	#Extract Level Data
					if not started:
						if line == "<GameObject "+objectName+">":
							started=True
						continue
					if line == "</GameObject>":
						break
					levelData.insert(i+j,line)
					j+=1

				#for line in levelData:
				#	print line

			i += loadGameObject(temp,levelData,i)

			GameObjects.append(temp)
			#i+=n
		elif levelData[i].startswith("<NPC"):
			path = levelData[i].lstrip("<NPC").rstrip(">").lstrip(" ").split(" ")[0]
			if len(levelData[i].lstrip("<NPC").rstrip(">").lstrip(" ").split(" "))>1:
				objectName = levelData[i].lstrip("<GameObject").rstrip(">").lstrip(" ").split(" ")[1]
			if path != "":
				tempFiler = file(config.AssetPath+path,"r")
				lines = tempFiler.readlines()
				started=False
				for j in range(len(lines)):	#Strip Tabs and New Lines
					lines[j] = lines[j].lstrip("\t").rstrip("\n")
				j=1
				for line in lines:	#Extract Level Data
					if not started:
						if line == "<NPC "+objectName+">":
							started=True
						continue
					if line == "</NPC>":
						break
					levelData.insert(i+j,line)
					j+=1

			i += loadNPC(temp,levelData,i)

			NPCs.append(temp)
		i+=1
	end = time.time()
	errors.debug("Took "+str(end-start)+" seconds to parse file.")
	if Name == None:
		errors.warning("Level has no Name attribute.")
		Name = "Unknown Area"
	GraphicEngine.setLevelName(Name)
	start = time.time()
	if BG == None:
		errors.error("Level has no Background attribute.")
	else:
		try:
			GraphicEngine.setBackground(pygame.image.load(config.AssetPath+BG).convert())
		except pygame.error:
			errors.error("Unable to load level background. (Line: "+str(i)+")")
	end = time.time()
	errors.debug("Took "+str(end-start)+" seconds to load background.")

	start = time.time()
	if Mask == None:
		errors.info("Level has no Mask attribute.")
	else:
		try:
			GameEngine.setMask(pygame.image.load(config.AssetPath+Mask).convert())
		except pygame.error:
			errors.error("Unable to load level mask. (Line: "+str(i)+")")
	end = time.time()
	errors.debug("Took "+str(end-start)+" seconds to load mask.")
	if Enemies != None and len(Enemies)>0:
		if BattleBG == None or len(BattleBG) == 0:
			errors.info("No battle backgrounds specified for this level.")
		else:
#			for i in xrange(len(BattleBG)):
#				for j in range(len(BattleBG[i])):
#					if BattleBG[i][j] != None:
#						try:
#							BattleBG[i][j] = pygame.image.load(BattleBG[i][j]).convert_alpha()
#						except pygame.error:
#							errors.error("Unable to load battle background for this level.")
#							BattleBG[i][j] = None
			GameEngine.setBattleBG(BattleBG)
			GameEngine.setEnemies(Enemies)
	else:
		GameEngine.setBattleBG([])
		GameEngine.setEnemies([])

	start = time.time()
	for trigger in Triggers:
		errors.debug("Adding "+trigger["Id"]+" trigger.")
		# Should probably be using a factory...
		if "Area" in trigger.keys() and trigger["Area"]!=None:
			trigger["Area"] = pygame.rect.Rect(trigger["Area"])
		if trigger["Effect"]=="State Set":
			del trigger["Effect"]
			GameEngine.addTrigger(triggers.StateSetTrigger(**trigger))
		elif trigger["Effect"]=="State Toggle":
			del trigger["Effect"]
			GameEngine.addTrigger(triggers.StateToggleTrigger(**trigger))
		elif trigger["Effect"]=="Area Change":
			del trigger["Effect"]
			GameEngine.addTrigger(triggers.AreaChangeTrigger(**trigger))
		elif trigger["Effect"]=="SBSC":
			del trigger["Effect"]
			GameEngine.addTrigger(triggers.SBSCTrigger(**trigger))
		elif trigger["Effect"]=="TBSC":
			del trigger["Effect"]
			GameEngine.addTrigger(triggers.TBSCTrigger(**trigger))
		elif trigger["Effect"]=="Battle":
			del trigger["Effect"]
			GameEngine.addTrigger(triggers.BattleTrigger(**trigger))
		elif trigger["Effect"]=="Item":
			del trigger["Effect"]
			GameEngine.addTrigger(triggers.ItemTrigger(**trigger))
		elif trigger["Effect"]=="Quest Complete":
			del trigger["Effect"]
			GameEngine.addTrigger(triggers.QuestCompleteTrigger(**trigger))
		elif trigger["Effect"]=="Dialog":
			del trigger["Effect"]
			trigger["Dialog"] = loadDialog(trigger["Dialog"])
			GameEngine.addTrigger(triggers.DialogTrigger(**trigger))
		else:
			errors.error("Undefined Trigger Effect")
	end = time.time()
	errors.debug("Took "+str(end-start)+" seconds to create triggers.")

	start = time.time()
	for obj in GameObjects:

		errors.debug("Adding "+obj["id"])
		#print str(obj["id"])+":"
		#for key in obj.keys():
		#	print key,obj[key]
		#for key in obj["graphicObject"].keys():
		#	print key,obj["graphicObject"][key]
		#for key in obj["graphicObject"]["animations"].keys():
		#	for i in range(0,4):
		#		if obj["graphicObject"]["animations"][key][i] != None:
		#			print key+str(i),len(obj["graphicObject"]["animations"][key][i].getFrames())
		#		else:
		#			print key+str(i),None
		#print "\n"

		for state in obj["mask"].keys():
			if obj["mask"][state] != None:
				img = pygame.image.load(config.AssetPath+str(obj["mask"][state]))
				#obj["mask"][state] = pygame.mask.from_threshold(img,[255,255,255],(127,127,127,127))
				img.set_colorkey((0,0,0))
				obj["mask"][state] = pygame.mask.from_surface(img)
		if obj["graphicObject"].keys().__contains__("flipX"):
			for state in obj["graphicObject"]["animations"].keys():
				i=0
				if obj["graphicObject"]["animations"][state][1].getNextAnimation() != None:
					nextAnimation = obj["graphicObject"]["animations"][state][1].getNextAnimation()[:-1]+"W"
				else:
					nextAnimation = None
				obj["graphicObject"]["animations"][state][3] = Animation(None,nextAnimation,state+"W")
				for frame in obj["graphicObject"]["animations"][state][1].getFrames():
					i+=1
					obj["graphicObject"]["animations"][state][3].addFrame(AnimationFrame(pygame.transform.flip(frame.image,True,False),frame.delay,None,i-1))
			del obj["graphicObject"]["flipX"]

		#Animation Linker:
		for state in obj["graphicObject"]["animations"].keys():
			for dire in range(0,4):
				if obj["graphicObject"]["animations"][state][dire] == None:
					continue
				nextState = obj["graphicObject"]["animations"][state][dire].getNextAnimation()
				if nextState == None or type(nextState)==Animation:
					continue
				if obj["graphicObject"]["animations"][nextState.rstrip("NESW")][dire].getName()==nextState:
					obj["graphicObject"]["animations"][state][dire].nextAnimation = obj["graphicObject"]["animations"][nextState.rstrip("NESW")][dire]
				else:
					errors.error("Animation linker is officially insufficient. \n(It was already unofficially insufficient, but now things just got worse)\n((Troublemaker: "+state+" -> "+nextState+"))")

		obj["graphicObject"] = GraphicObject(**obj["graphicObject"])
		GraphicEngine.addObject(obj["graphicObject"])
		if obj.keys().__contains__("pushable") and obj["pushable"]==True:
			del obj["pushable"]
			if obj["area"]!=None:
				obj["area"] = pygame.rect.Rect(obj["area"])
			GameEngine.addActor(Pushable(**obj))
		else:
			GameEngine.addActor(GameObject(**obj))
	end = time.time()
	errors.debug("Took "+str(end-start)+" seconds to create objects.")

	start = time.time()
	for npc in NPCs:
		if "AnimeXML" in npc:
			errors.debug("Adding sNPC: "+npc["Id"])
			if npc["Icon"]!=None:
				npc["Icon"]=pygame.image.load(npc["Icon"]).convert()
			npc["Dialog"]=loadDialog(npc["Dialog"])
			#print npc["Dialog"]
			temp = sNPC(**npc)
			GameEngine.addNPC(temp)
			GraphicEngine.addObject(temp.getGraphicObject())
		else:
			errors.debug("Adding NPC: "+npc["Id"])
			if npc["Icon"]!=None:
				npc["Icon"]=pygame.image.load(npc["Icon"]).convert()
			npc["Dialog"]=loadDialog(npc["Dialog"])
			#print npc["Dialog"]
			temp = NPC(**npc)
			GameEngine.addNPC(temp)
			GraphicEngine.addObject(temp.getGraphicObject())
	end = time.time()
	errors.debug("Took "+str(end-start)+" seconds to create NPCs.")

	filer.close()
	totalEnd = time.time()
	errors.info("Took "+str(totalEnd-totalStart)+" seconds to load level.")

## Converts XML data to a list of arguments to create a GameObject
#
#  @param temp A dictionary containing the object data extracted from the levelData.
#  @param levelData A list of strings representing the level data the object will
#      be loaded from.
#  @param i The line that the object starts on.
#
#  @returns int How many lines this object took in the levelData.
def loadGameObject(temp,levelData,i):
	temp["graphicObject"] = {}
	n=1
	while levelData[i+n]!="</GameObject>":
		key = levelData[i+n][1:levelData[i+n].find(">")]
		if key == "Mask":
			n+=1
			temp["mask"] = {}
			while levelData[i+n]!="</Mask>":
				state = levelData[i+n][7:levelData[i+n].find(">")]
				temp["mask"][state] = json.loads(levelData[i+n][levelData[i+n].find(">")+1:levelData[i+n].rfind("<")])
				n+=1
			n+=1
		elif key == "GraphicObject":
			if "animations" not in temp["graphicObject"]:
				temp["graphicObject"]["animations"] = {}
			n+=1
			while levelData[i+n]!="</GraphicObject>":
				if levelData[i+n].startswith("<State"):
					state = levelData[i+n][7:levelData[i+n].find(">")]
					temp["graphicObject"]["animations"][state] = [None,None,None,None]
					n+=1
					while levelData[i+n]!="</State>":
						#Retrieve Direction
						dire = int(levelData[i+n][11:levelData[i+n].find(">")])
						xml = levelData[i+n][levelData[i+n].find(">")+1:levelData[i+n].rfind("<")]
						if dire == 0:
							temp["graphicObject"]["animations"][state][dire] = loadAnimation(xml,state+"N")
						elif dire == 1:
							temp["graphicObject"]["animations"][state][dire] = loadAnimation(xml,state+"E")
						elif dire == 2:
							temp["graphicObject"]["animations"][state][dire] = loadAnimation(xml,state+"S")
						elif dire == 3:
							temp["graphicObject"]["animations"][state][dire] = loadAnimation(xml,state+"W")
						n+=1
					n+=1
				else:
					key = levelData[i+n][levelData[i+n].find("<")+1:levelData[i+n].find(">")]
					value = levelData[i+n][levelData[i+n].find(">")+1:levelData[i+n].rfind("<")]
					temp["graphicObject"][key] = json.loads(value)
					n+=1
			n+=1
		else:
			value = levelData[i+n][levelData[i+n].find(">")+1:levelData[i+n].find("<",levelData[i+n].find(">"))]
			temp[key[0].lower()+key[1:]]=json.loads(value)
			n+=1
	return n

## Converts XML data to a list of arguments to create a NPC
#
#  @param temp A dictionary containing the object data extracted from the levelData.
#  @param levelData A list of strings representing the level data the object will
#      be loaded from.
#  @param i The line that the object starts on.
#
#  @returns int How many lines this object took in the levelData.
def loadNPC(temp,levelData,i):
	n=1
	while levelData[i+n]!="</NPC>":
		key = levelData[i+n][1:levelData[i+n].find(">")]
		value = levelData[i+n][levelData[i+n].find(">")+1:levelData[i+n].find("<",levelData[i+n].find(">"))]
		if key == "Dialog":
			if value != "null":
				dialog=open(config.AssetPath+value,"r")
				lines=dialog.readlines()
				dialog=""
				for line in lines:
					dialog+=line.rstrip("\n")
				dialog.replace("\t","")
				temp["Dialog"]=json.loads(dialog)
			else:
				temp["Dialog"]=None
		elif key == "AnimeXML":
			temp["AnimeXML"]=value
		elif key == "Icon":
			if value=="null":
				temp["Icon"]=None
			else:
				temp["Icon"]=value
		else:
			temp[key]=json.loads(value)
		n+=1
	return n

def loadDialog(data):
	if data==None:
		return None
	elif type(data)==unicode:
		if data=="@BUY":
			return "@BUY"
		elif data=="@SELL":
			return "@SELL"
		elif data=="@SLEEP":
			return "@SLEEP"
		elif data.startswith("@TRIGGER"):
			return str(data)
		elif data.startswith("@QUEST"):
			return str(data)
	links=[]
	for link in data["Links"]:
		links.append(loadDialog(link))
	if "Branches" in data:
		branches=[]
		for branch in data["Branches"]:
			branches.append(loadDialog(branch))
		if len(branches)==0:
			branches = None
	else:
		branches = None
	if "PreBranch" in data:
		prebranch=loadDialog(data["PreBranch"])
	else:
		prebranch=None
	args={"Text":data["Text"],"Options":data["Options"],"Links":links,"Branches":branches,"PreBranch":prebranch}
	if "Actions" in data:
		args["Actions"] = data["Actions"]
	if "PreAction" in data:
		args["PreAction"] = data["PreAction"]
	dialog=Dialog(**args)
	return dialog

def load(xmlpath,level,GameEngine,GraphicEngine):
	loadXML(config.AssetPath+xmlpath,level,GameEngine,GraphicEngine)
	GameEngine.loadLevel(level)
	#GraphicEngine.loadLevel(level)
