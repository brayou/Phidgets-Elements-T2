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
        # Load the mana orbs
        self.mana = [None] * 33
        self.manaTex = {"earth" :  loader.loadTexture("Textures/HEX_Green.jpg"),
                           "wind" : loader.loadTexture("Textures/HEX_Yellow.jpg"),
                           "fire" : loader.loadTexture("Textures/HEX_Red.jpg"),
                           "water" : loader.loadTexture("Textures/HEX_Blue.jpg") }
        # Spawn all of the mana orbs
        for i in xrange(33):
            # 0 of each element is currently in place
            self.earthCount = 0
            self.windCount = 0
            self.fireCount = 0
            self.waterCount = 0
            # Load the mana models and scale them
            self.mana[i] = (loader.loadModel("Models/petridish.egg"))
            self.mana[i].reparentTo(render)
            self.mana[i].setHpr(0,0,0)
            self.mana[i].setScale(0.00005)
            randElem = randint(0,3)
            # If [element] and less than 2 [element] mana in the current circle
                # texture the mana orb
            if randElem == 0 and self.earthCount < 2:
                self.mana[i].setTexture(self.manaTex["earth"],1)
                self.earthCount += 1
            elif randElem == 1 and self.windCount < 2:
                self.mana[i].setTexture(self.manaTex["wind"],1)
                self.windCount += 1
            elif randElem == 2 and self.fireCount < 2:
                self.mana[i].setTexture(self.manaTex["fire"],1)
                self.fireCount += 1
            elif randElem == 3 and self.waterCount < 2:
                self.mana[i].setTexture(self.manaTex["water"],1)
                self.waterCount += 1
            # Reset the element counts when moving onto the next circle so as to allow 2 per
            if i == 8 or i == 15 or i == 21 or i == 26 or i == 30:
                self.earthCount = 0
                self.windCount = 0
                self.fireCount = 0
                self.airCount = 0
                
        # 6th circle positioning
        self.mana[0].setPos(-self.deltaFunc(0.7019,3.0,0.875),-.05,self.deltaFunc(1.072,3.0,0.875))
        self.mana[1].setPos(0,-0.5,0)
        self.mana[2].setPos(0,-0.5,0)
        self.mana[3].setPos(0,-0.5,0)
        self.mana[4].setPos(0,-0.5,0)
        self.mana[5].setPos(0,-0.5,0)
        self.mana[6].setPos(0,-0.5,0)
        self.mana[7].setPos(0,-0.5,0)
        # 5th circle positioning
        self.mana[8].setPos(-self.deltaFunc(2.066,2.5,0.75),-.05,self.deltaFunc(0.03798,2.5,0.75))
        self.mana[9].setPos(0,-0.5,0)
        self.mana[10].setPos(0,-0.5,0)
        self.mana[11].setPos(0,-0.5,0)
        self.mana[12].setPos(0,-0.5,0)
        self.mana[13].setPos(0,-0.5,0)
        self.mana[14].setPos(0,-0.5,0)
        # 4th circle positioning
        self.mana[15].setPos(-self.deltaFunc(3.0,2.0,0.625),-.05,self.deltaFunc(0.2679,2.0,0.625))
        self.mana[16].setPos(0,-0.5,0)
        self.mana[17].setPos(0,-0.5,0)
        self.mana[18].setPos(0,-0.5,0)
        self.mana[19].setPos(0,-0.5,0)
        self.mana[20].setPos(0,-0.5,0)
        # 3th circle positioning
        self.mana[21].setPos(-self.deltaFunc(2.91,1.5,0.5),-.05,self.deltaFunc(0.987,1.5,0.5))
        self.mana[22].setPos(0,-0.5,0)
        self.mana[23].setPos(0,-0.5,0)
        self.mana[24].setPos(0,-0.5,0)
        self.mana[25].setPos(0,-0.5,0)
        # 2nd circle positioning
        self.mana[26].setPos(-self.deltaFunc(1.94,1.0,0.375),-.05,-self.deltaFunc(0.658,1.0,0.375))
        self.mana[27].setPos(0,-0.5,0)
        self.mana[28].setPos(0,-0.5,0)
        self.mana[29].setPos(0,-0.5,0)
        # 1st circle positioning
        self.mana[30].setPos(-self.deltaFunc(0.75,.5,0.25),-.05,-self.deltaFunc(0.067,.5,0.25))
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