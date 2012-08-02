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
from phidgets_manager import *

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

        # start the phidget manager
        self.phidget = Phidget()
        self.phidget.allLEDsOff()

        # accept sensor input
        self.accept( "touchRec", self.touchRec )        # received a touch sensor from the phidgets manager
        self.accept( "motionRec", self.motionRec )      # received a motion sensor from the phidgets manager
        self.accept( "irRec", self.irRec )              # received a ir sensor from the phidgets manager
        self.accept( "pressureRec", self.pressureRec )  # received a pressure plate sensor from the phidgets manager
        self.accept( "RFIDtagRec", self.rfidTagRec )    # received a rfid tag sensor from the phidgets manager
        
        if TEST_MODE:
            self.accept( "w-repeat", self.move, [ 1 ] )
            self.accept( "s-repeat", self.move, [ -1 ] )
            self.accept( "a-repeat", self.turn, [ -10 ] )
            self.accept( "d-repeat", self.turn, [ 10 ] )
            self.accept( "escape", self.exit)               # exit the program
        
        # start screen
        self.startScreen = loader.loadModel("Models/plane.egg")
        self.startScreen.reparentTo(render)
        self.startScreenTex = loader.loadTexture("Textures/startScreen.jpg")
        self.startScren.setTexture(self.startScreenTex,1)
        self.screen = 0
        if 
        # start polling
        self.phidget.startPolling()
        

###################### ENVIRONMENT ###########################################
    
    def nextScreen(self):
        if self.screen == 0:
            self.startScreenTex = loader.loadTexture("Textures/instructions.jpg")
            self.startScreen.setTexture(self.startScreenTex,1)
            self.phaseOne()
        else:
            self.startScreenTex = loader.loadTexture("Textures/startScreen.jpg")
            self.startScreen.setTexture(self.startScreenTex,1)
             
            
    def phaseOne(self):
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
        
###################### HANDLERS ##############################################
    
    def touchRec(self,which):
        # a touch sensor has been received, string which from config T_FUNC array
        print "Touch received:", which
        self.touch = which
    def motionRec(self,state):
        # a motion sensor has been received, state provided either "got" or "lost"
        ## print "Motion received:", state
        None
        
    def irRec(self,which):
        # a IR sensor has been received, string which from config IR_FUNC array
        print "IR received:", which
        
    def pressureRec(self,state):
        # a pressure sensor has been received, state provided either "got" or "lost"
        print "Pressure received:", state
        
    def rfidTagRec(self, tag, state):
        # a RFID tag sensor has been received, tag is the string identifier 
        print "RFID tag received:", tag, "state:", state
        
###################### SYSTEM ################################################

    def exit(self):
        self.phidget.allLEDsOff()
        sys.exit()

w = World()

run()