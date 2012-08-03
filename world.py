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
            self.accept( "escape", self.exit)               # exit the program
            
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
        self.startScreenTex = loader.loadTexture("Textures/startScreen.jpg")
        self.startScreen.setTexture(self.startScreenTex,1)
        self.startScreen.setScale(0.4)
        self.screen = 0
        
        #activate nextScreen upon phase button press
        if self.next == True:
           self.nextScreens()

###################### ENVIRONMENT ###########################################
    
    def nextScreen(self):
        if self.screen == 0:
            self.startScreenTex = loader.loadTexture("Textures/instructions.jpg")
            self.startScreen.setTexture(self.startScreenTex,1)
            self.startScreen.reparentTo(render)
            self.screen = 1
        elif self.screen == 1:
            self.startScreenTex = loader.loadTexture("Textures/controls.jpg")
            self.startScreen.setTexture(self.startScreenTex,1)
            self.startScreen.reparentTo(render)
            self.screen == 2
            self.phaseZero()
        else:
            self.startScreenTex = loader.loadTexture("Textures/startScreen.jpg")
            self.startScreen.setTexture(self.startScreenTex,1)
            self.startScreen.reparentTo(render)
             
    def phaseZero(self):
        self.startScreen.hideNode()
        self.ui = loader.loaderModel("Models/plane.egg")
        self.ui.reparentTo(render)
        self.uiTex = loader.loadTexture("Textures/ui.jpg")
        self.ui.setTexture(self.uiTex,1)
        
    def phaseOne(self):
        self.ui.reparentTo(render)
        ## def deltaFunc(self,v,r,mult):
        ## #radius of petri dish
        ## R=.6
        ## V = R*mult-((R*mult*v)/r)
        ## ## print V
        ## return V
        
    def yFinder(self,x):
        y = 0.2*sqrt(9-25*x*x)
        ## print y
        
    def phaseTwo(self):
        self.ui.reparentTo(render)
        # Load petridish
        self.dish = loader.loadModel("Models/petridish.egg")
        self.dish.reparentTo(render)
        dishTex = loader.loadTexture("Textures/PetriDish.jpg")
        self.dish.setTexture(dishTex, 1)
        self.dish.setScale(0.001)
        self.dish.setPosHpr(0,0,0,0,0,0)
        # Load the nanobot
        self.robot = loader.loadModel("Models/NanoBot1.egg")
        self.robot.reparentTo(render)
        ## self.robotTex = loader.loadTexture("Textures/Nano1Body.jpg")
        ## self.robot.setTexture(self.robotTex,1)
        self.robot.setPosHpr(0,0,-.25,0,0,0)
        self.robot.setScale(0.0025)
        ## self.robot.place()
        self.phaseTwo()
        self.yFinder(0)
        
        # Load the mana orbs
        self.mana = [None] * 33
        self.manaTex = {"earth" :  loader.loadTexture("Textures/HEX_Green.jpg"),
                           "wind" : loader.loadTexture("Textures/HEX_Yellow.jpg"),
                           "fire" : loader.loadTexture("Textures/HEX_Red.jpg"),
                           "water" : loader.loadTexture("Textures/HEX_Blue.jpg") }
        # Spawn all of the mana orbs
        for i in xrange(85):
            # Load the mana models and scale them
            self.mana[i] = (loader.loadModel("Models/petridish.egg"))
            self.mana[i].reparentTo(render)
            self.mana[i].setHpr(0,0,0)
            self.mana[i].setScale(0.00005)
            randElem = randint(0,3)
            if randElem == 0:
                self.mana[i].setTexture(self.manaTex["earth"],1)
                self.earthCount += 1
            elif randElem == 1:
                self.mana[i].setTexture(self.manaTex["wind"],1)
                self.windCount += 1
            elif randElem == 2:
                self.mana[i].setTexture(self.manaTex["fire"],1)
                self.fireCount += 1
            elif randElem == 3:
                self.mana[i].setTexture(self.manaTex["water"],1)
                self.waterCount += 1
        
        #gem positioning
        self.mana[0].setPos(0,-0.5,0)
        self.mana[1].setPos(0,-0.5,0)
        self.mana[2].setPos(0,-0.5,0)
        self.mana[3].setPos(0,-0.5,0)
        self.mana[4].setPos(0,-0.5,0)
        self.mana[5].setPos(0,-0.5,0)
        self.mana[6].setPos(0,-0.5,0)
        self.mana[7].setPos(0,-0.5,0)
        self.mana[8].setPos(0,-0.5,0)
        self.mana[9].setPos(0,-0.5,0)
        self.mana[10].setPos(0,-0.5,0)
        self.mana[11].setPos(0,-0.5,0)
        self.mana[12].setPos(0,-0.5,0)
        self.mana[13].setPos(0,-0.5,0)
        self.mana[14].setPos(0,-0.5,0)
        self.mana[15].setPos(0,-0.5,0)
        self.mana[16].setPos(0,-0.5,0)
        self.mana[17].setPos(0,-0.5,0)
        self.mana[18].setPos(0,-0.5,0)
        self.mana[19].setPos(0,-0.5,0)
        self.mana[20].setPos(0,-0.5,0)
        self.mana[21].setPos(0,-0.5,0)
        self.mana[22].setPos(0,-0.5,0)
        self.mana[23].setPos(0,-0.5,0)
        self.mana[24].setPos(0,-0.5,0)
        self.mana[25].setPos(0,-0.5,0)
        self.mana[26].setPos(0,-0.5,0)
        self.mana[27].setPos(0,-0.5,0)
        self.mana[28].setPos(0,-0.5,0)
        self.mana[29].setPos(0,-0.5,0)
        self.mana[30].setPos(0,-0.5,0)
        self.mana[31].setPos(0,-0.5,0)
        self.mana[32].setPos(0,-0.5,0)
        
    def endRound(self):
        print "Round over"
        self.ui.hideNode()
        self.startScreen.reparentTo(render)
        self.startScreenTex = loader.loadTexture("Textures/endRound.jpg")
        self.startScreen.setTexture(self.startScreenTex,1)
        
    def exitGame(self):
        print "Game over"
        self.ui.hideNode()
        self.startScreen.reparentTo(render)
        self.startScreenTex = loader.loadTexture("Textures/endGame.jpg")
        self.startScreen.setTexture(self.startScreenTex,1)
        
        
        
###################### HANDLERS ##############################################
    
    def touchRec(self,which):
        # a touch sensor has been received, string which from config T_FUNC array
        print "Touch received:", which
        self.touch[which] = True
    
    def motionRec(self,state):
        # a motion sensor has been received, state provided either "got" or "lost"
        ## print "Motion received:", state
        None
        
    def irRec(self,which):
        # a IR sensor has been received, string which from config IR_FUNC array
        print "IR received:", which
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
            self.earth = True
        #wind ir sensor pressed
        if self.ir[1]:
            self.wind = True
        #fire ir sensor pressed
        if self.ir[2]:
            self.fire = True
        #water ir sensor pressed
        if self.ir[3]:
            self.water = True
        
        #next button pressed
        if self.touch[0]:
            self.next = True
        #practice button pressed
        if self.touch[1]:
            self.practice = True
        #help button pressed
        if self.touch[2]:
            self.help = True
        #exit button pressed
        if self.touch[3]:
            self.exit = True
        
        #Reset values so as to make sensor reads instantaneous
        self.ir = [False, False, False, False]
        self.touch = [False, False, False, False]
        return Task.again
        
###################### SYSTEM ################################################

    def exit(self):
        self.phidget.allLEDsOff()
        sys.exit()

w = World()

run()