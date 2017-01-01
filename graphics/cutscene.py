from overworld import GraphicObject
from level import loadGameObject, loadNPC

import config

## Contains all the information to play a cutscene.
class Cutscene(object):

    ## Constructor.
    #
    #  @param actions A list containing actions in the order they happen for this
    #      cutscene. Each action is a list containing the type of action followed
    #      by arguments describing how that action should take place.
    #  @param graphicsEngine A reference to a GraphicsEngine object.
    #  @param player A reference to a Player object.
    def __init__(self, actions, graphicsEngine, player):
        self.actions = actions
        self.currentAction = 0
        self.graphicsEngine = graphicsEngine
        self.player = player
        self.playing = False
        self.timer = 0.0
        self.timerStop = 0.0

    ## Starts the cutscene.
    def play(self):
        self.player.setCanMove(False)
        self.playing = True

    ## Stops and resets the cutscene.
    def stop(self):
        self.currentAction = 0
        self.timer = 0.0
        self.timerStop = 0.0
        self.player.setCanMove(True)
        self.playing = False

    ## Pauses the cutscene.
    def pause(self):
        self.playing = False

    ## Updates the cutscene and runs all of its internal code.
    def update(self,tick):
        if not self.playing:
            return

        if self.timerStop != 0:
            self.timer += tick
            if self.timer >= self.timerStop:
                self.timerStop = 0.0
                self.currentAction += 1
            else:
                return

        while True:
            if self.currentAction>=len(self.actions):
                self.stop()
                return

            action = self.actions[self.currentAction]

            if action[0] == "wait":
                if action[1] == "dialog":
                    if self.graphicsEngine.getDialog():
                        return
                    else:
                        self.currentAction += 1
                else:
                    self.timerStop = float(action[0])
                    return
            elif action[0] == "bg":
                self.graphicsEngine.setBackground(pygame.image.load(action[1]).convert())
            elif action[0] == "add":
                if action[1] == "object":
                    filer = open(config.AssetPath+action[6],'r')
                    lines = filer.readlines()

                    for i in xrange(len(lines)):	#Strip Tabs and New Lines
                		lines[i] = lines[i].lstrip("\t").rstrip("\n")

                    for i in xrange(len(lines)):
                        if line == "<GameObject "+action[2]+">":
                            break

                    temp = {}
                    loadGameObject(temp,lines,i)

                    temp

                    filer.close()

                elif action[1] == "NPC":
                    pass
            elif action[0] == "set":
                if action[1] == "state":
                    pass
                elif action[1] == "vel":
                    pass
            elif action[0] == "dialog":
                pass
