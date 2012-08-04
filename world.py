##############################################################################
## Program Name (File Name): Manabots.py
## Programmer: Branden Youssef
## Purpose: GD 2 Phidgets Elements - Team 2
## Date: 8/1/12
## Additional Notes:
## 
##############################################################################
#Basic imports
from threading import *
from ctypes import *
from math import *
from time import sleep
from random import randint
import sys

#Panda specific imports
import direct.directbase.DirectStart 
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task 
from direct.actor import Actor 
from direct.interval.IntervalGlobal import * 

#World specific imports
from config import *
from Phidgets.phidgets_manager import *

#TO DO
#Fix the skipping of screens
#TO DO

class World(DirectObject):
    # Initialization Function
    def __init__(self): 
        print "Initializing World"
        
        # Set up the camera
        base.disableMouse()
        base.camera.setPos(0,-2.5,0)
        base.camera.setHpr(0,0,0)
        base.camLens.setFar(10000)
        base.setBackgroundColor( .5, .5, .5 )
        ## base.camera.place()
        # Declare variables
        self.ir = [False, False, False, False]
        self.touch = self.ir
        #Set sensor output variables to False
        self.earth = False
        self.wind = False
        self.fire = False
        self.water = False
        self.next = False
        self.practice = False
        self.help = False
        self.exit = False
        
        if TEST_MODE:
            self.accept( "q", self.irRec,[0])
            self.accept( "w", self.irRec,[1])
            self.accept( "e", self.irRec,[2])
            self.accept( "r", self.irRec,[3])
            self.accept( "a", self.touchRec,[0])
            self.accept( "s", self.touchRec,[1])
            self.accept( "d", self.touchRec,[2])
            self.accept( "f", self.touchRec,[3])
            self.accept( "escape", self.powerOff)               # exit the program
            
        if not TEST_MODE:
           # start the phidget manager
            self.phidget = Phidget()
            self.phidget.allLEDsOff()

            # accept sensor input
            self.accept( "touchRec", self.touchRec )        # received a touch sensor from the phidgets manager
            self.accept( "motionRec", self.motionRec )      # received a motion sensor from the phidgets manager
            self.accept( "irRec", self.irRec )              # received a ir sensor from the phidgets manager
            self.accept( "pressureRec", self.pressureRec )  # received a pressure plate sensor from the phidgets manager
            self.accept( "RFIDtagRec", self.rfidTagRec )    # received a rfid tag sensor from the phidgets manager
            
            # start polling
            self.phidget.startPolling()
        taskMgr.doMethodLater(0.125,self.checkSensors,"checkSensor")
        
        # start screen
        self.startScreen = loader.loadModel("Models/plane.egg")
        self.startScreen.reparentTo(render)
        self.startScreen.setScale(PLANE_SCALE)
        self.screen = 0

        # start the game
        taskMgr.doMethodLater(NEXT_DELAY,self.moveOn,"moveOn")
        taskMgr.add(self.exitGame,"exitGame")
        self.nextScreen()

###################### ENVIRONMENT ###########################################
    def moveOn(self,task):
        #activate nextScreen upon phase button press
        if self.next:
            print "Next screen"
            self.screen +=1
            self.nextScreen()
            return task.again
        else:
            return task.cont
    
    def exitGame(self,task):
        #prompt the player to end the game
        if self.exit:
            print "Exiting?"
            self.exitText = OnscreenText(text="Are you sure you want to leave?\nHit 'EXIT' again to confirm or 'NEXT' to cancel.", style=1, fg=(1,.7,0,1), pos=(0,0,0), scale = .1)
            s = Sequence(Wait(0.5)).start()
            self.exit = False
            if self.exit:
                self.powerOff()
            elif self.next:
                return task.cont
        
    ## def contTask(self,funcName,delay):
        ## function = "self."+funcName
        ## task = str(funcName)
        ## delay = int(delay)
        ## if delay == 0:
            ## taskMgr.add(function,task)
        ## else:
            ## taskMgr.doMethodLater(delay,function,task)
            
    ## def contTask(self):
        ## taskMgr.add(self.moveOn,"moveOn")
        
    def nextScreen(self):
        if self.screen == 0:
            self.startScreenTex = loader.loadTexture("Textures/startScreen.jpg")
            self.startScreen.setTexture(self.startScreenTex,1)
            self.startScreen.reparentTo(render)
        elif self.screen == 1:
            self.startScreenTex = loader.loadTexture("Textures/instructions.jpg")
            self.startScreen.setTexture(self.startScreenTex,1)
            self.startScreen.reparentTo(render)
        elif self.screen == 2:
            self.startScreenTex = loader.loadTexture("Textures/controls.jpg")
            self.startScreen.setTexture(self.startScreenTex,1)
            self.startScreen.reparentTo(render)
        elif self.screen ==3:
            self.phaseZero()
        elif self.screen ==4:
            self.phaseTwo()
        if TEST_MODE:
            if self.screen ==5:
                self.endRound()
            elif self.screen ==6:
                self.endGame()
            elif self.screen >=7:
                self.screen = 0
                self.nextScreen()
             
    def phaseZero(self):
        self.startScreen.detachNode()
        self.ui = loader.loadModel("Models/plane.egg")
        self.ui.reparentTo(render)
        self.uiTex = loader.loadTexture("Textures/ui.jpg")
        self.ui.setTexture(self.uiTex,1)
        self.ui.setPosHpr(0,0,0,0,0,0)
        self.ui.setScale(PLANE_SCALE)
        self.phaseOne()
        
    def phaseOne(self):
        self.ui.reparentTo(render)
        # Load petridish
        self.dish = loader.loadModel("Models/petridish.egg")
        self.dish.reparentTo(render)
        dishTex = loader.loadTexture("Textures/PetriDish.jpg")
        self.dish.setTexture(dishTex, 1)
        self.dish.setScale(0.00075/3)
        self.dish.setPosHpr(0,0,.325,0,0,0)
        # Load the nanobot
        self.robot = loader.loadModel("Models/NanoBot1.egg")
        self.robot.reparentTo(render)
        self.robot.setPosHpr(.175,0,-.125,180,270,0)
        self.robot.setScale(0.002*3)
        # Load the mana textures for mana in the dish
        self.manaTex = {"red" :  loader.loadTexture("Textures/HEX_Red.jpg"),
                        "yellow" : loader.loadTexture("Textures/HEX_Yellow.jpg"),
                        "blue" : loader.loadTexture("Textures/HEX_Blue.jpg"),
                        "green" : loader.loadTexture("Textures/HEX_Green.jpg") }
        # Spawn the grid and texture the individual mana
        self.hexGrid = loader.loadModel("Models/hexGrid.egg")
        self.hexGrid.reparentTo(render)
        self.hexGrid.setScale(.00045/3)
        self.hexGrid.setPosHpr(0,-1,.2,90,90,90)
        self.mana = []
        for j in xrange(NUM_RINGS):
            for i in xrange(NUM_GEMS[j]):
                self.mana.append(self.hexGrid.find("**/Hex"+str(j+1)+"_"+str(i+1)))
                ## print self.mana[-1]
                randElem = randint(0,3)
                if randElem == 0:
                    self.mana[i].setTexture(self.manaTex["red"],1)
                elif randElem == 1:
                    self.mana[i].setTexture(self.manaTex["yellow"],1)
                elif randElem == 2:
                    self.mana[i].setTexture(self.manaTex["blue"],1)
                elif randElem == 3:
                    self.mana[i].setTexture(self.manaTex["green"],1)
            ## self.hexGrid.place()
        #Prompt the player for their first choice
        
        
        #Prompt the player to perform the sequence
        
        
        #Prompt the player for their second choice
        
        
        #Prompt the player for the second sequence
        
        
        self.colorOne = "Red"
        self.colorTwo = "Green"
        self.loadedManaTex = [None,None]
        self.loadedManaTex[0] = loader.loadTexture("Textures/HEX_"+str(self.colorOne)+".jpg")
        self.loadedManaTex[1] = loader.loadTexture("Textures/HEX_"+str(self.colorTwo)+".jpg")
        ## self.phaseTwo()
        
    def phaseTwo(self):
        self.ui.reparentTo(render)
        # Move the petridish and rescale it
        self.dish.setScale(0.00075)
        self.dish.setPosHpr(0,0,0,0,0,0)
        # Move the robot and rescale it
        self.robot.setPosHpr(0,0,0,180,270,0)
        self.robot.setScale(0.002)
        # Load the loaded mana
        self.loadedMana = [None,None]
        for i in xrange(2):
            self.loadedMana[i] = loader.loadModel("Models/petridish.egg")
            self.loadedMana[i].reparentTo(render)
            self.loadedMana[i].setTexture(self.loadedManaTex[i],1)
            self.loadedMana[i].setPosHpr(0,-.25,0,0,0,0)
            self.loadedMana[i].setScale(0.00005)
        self.loadedMana[0].setZ(.03)
        self.loadedMana[1].setZ(-.0375)
        # Move the grid and rescale it
        self.hexGrid.setScale(.00045)
        self.hexGrid.setPosHpr(0,-1,0,90,90,90)
        
    def endRound(self):
        print "Round over"
        self.ui.detachNode()
        self.hexGrid.detachNode()
        self.dish.detachNode()
        self.robot.detachNode()
        self.loadedMana[0].detachNode()
        self.loadedMana[1].detachNode()
        for i in xrange(len(self.mana)):
            self.mana[i].detachNode()
        self.startScreen.reparentTo(render)
        self.startScreenTex = loader.loadTexture("Textures/endRound.jpg")
        self.startScreen.setTexture(self.startScreenTex,1)
        
        
    def endGame(self):
        print "Game over"
        self.ui.detachNode()
        self.startScreen.reparentTo(render)
        self.startScreenTex = loader.loadTexture("Textures/endGame.jpg")
        self.startScreen.setTexture(self.startScreenTex,1)
        
        
        
###################### HANDLERS ##############################################
    
    def touchRec(self,which):
        # a touch sensor has been received, string which from config T_FUNC array
        ## print "Touch received:", which
        self.touch[which] = True
    
    def motionRec(self,state):
        # a motion sensor has been received, state provided either "got" or "lost"
        ## print "Motion received:", state
        None
        
    def irRec(self,which):
        # a IR sensor has been received, string which from config IR_FUNC array
        ## print "IR received:", which
        self.ir[which] = True
    
    def pressureRec(self,state):
        # a pressure sensor has been received, state provided either "got" or "lost"
        print "Pressure received:", state
        
    def rfidTagRec(self, tag, state):
        # a RFID tag sensor has been received, tag is the string identifier 
        print "RFID tag received:", tag, "state:", state
        
    def checkSensors(self,task):
        #earth ir sensor pressed
        if self.ir[0]:
            self.red = True
            print "Red pressed"
        #wind ir sensor pressed
        if self.ir[1]:
            self.yellow = True
            print "Yellow pressed"
        #fire ir sensor pressed
        if self.ir[2]:
            self.blue = True
            print "Blue pressed"
        #water ir sensor pressed
        if self.ir[3]:
            self.green = True
            print "Green pressed"
            
        #next button pressed
        if self.touch[0]:
            self.exit = True
            print "Exit pressed"
        #practice button pressed
        if self.touch[1]:
            self.help = True
            print "Help pressed"
        #help button pressed
        if self.touch[2]:
            self.tutorial = True
            print "Tutorial pressed"
        #exit button pressed
        if self.touch[3]:
            self.next = True
            print "Next pressed"
        s = Sequence(Wait(0.5),Func(self.resetVals)).start()
        return Task.cont
        
    def resetVals(self):
        #Reset values so as to make sensor reads instantaneous
        self.ir = [False, False, False, False]
        self.touch = [False, False, False, False]
        self.red = False
        self.yellow = False
        self.blue = False
        self.green = False
        self.next = False
        self.practice = False
        self.help = False
        self.exit = False
        
###################### SYSTEM ################################################

    def powerOff(self):
        if not TEST_MODE:
            self.phidget.allLEDsOff()
        sys.exit()

w = World()

run()