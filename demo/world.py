#Basic imports
from threading import *
from ctypes import *
import sys
import math 
from time import sleep

#Panda specific imports
import direct.directbase.DirectStart 
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task 
from direct.actor import Actor 
from direct.interval.IntervalGlobal import * 

#World specific imports
from interface_config import *
from phidgets_manager import *

class World(DirectObject): 
    def __init__(self): 
        
        #Load the first environment model 
        self.panda = Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"}) 
        self.panda.setScale(.005) 
        self.panda.reparentTo(render) 
        ## self.pandaP1.loop("walk") 
        # create the carot object to aid in moving the panda forward
        self.pandaCarot=NodePath("Carot")
        self.pandaCarot.reparentTo(self.panda)
        self.pandaCarot.setPos(0,-400,0)  # large distance to offset the panda scale
        
        # set the camera
        base.disableMouse()
        base.camera.setPosHpr(15,-70,55, 12, -40, 10) 
        
        # start the phidget manager
        self.phidget = Phidget()
        self.phidget.allLEDsOff()

        # accepts 
        self.accept( "w-repeat", self.move, [ 1 ] )             ##### Remove Later
        self.accept( "s-repeat", self.move, [ -1 ] )            ##### Remove Later
        self.accept( "a-repeat", self.turn, [ -10 ] )           ##### Remove Later
        self.accept( "d-repeat", self.turn, [ 10 ] )            ##### Remove Later
        
        self.accept( "escape", self.exit)               # exit the program
        
        self.accept( "touchRec", self.touchRec )        # received a touch sensor from the phidgets manager
        self.accept( "motionRec", self.motionRec )      # received a motion sensor from the phidgets manager
        self.accept( "irRec", self.irRec )              # received a ir sensor from the phidgets manager
        self.accept( "pressureRec", self.pressureRec )  # received a pressure plate sensor from the phidgets manager
        self.accept( "RFIDtagRec", self.rfidTagRec )    # received a rfid tag sensor from the phidgets manager
        
        # start polling
        self.phidget.startPolling()

###################### HANDLERS ##############################################
        
    def touchRec(self,which):
        # a touch sensor has been received, string which from interface_config T_FUNC array
        print "Touch received:", which
        
    def motionRec(self,state):
        # a motion sensor has been received, state provided either "got" or "lost"
        ## print "Motion received:", state
        None
        
    def irRec(self,which):
        # a IR sensor has been received, string which from interface_config IR_FUNC array
        print "IR received:", which
        
    def pressureRec(self,state):
        # a pressure sensor has been received, state provided either "got" or "lost"
        print "Pressure received:", state
        
    def rfidTagRec(self, tag, state):
        # a RFID tag sensor has been received, tag is the string identifier 
        print "RFID tag received:", tag, "state:", state
        

###################### ENVIRONMENT ###########################################

    def move(self, value):
       self.panda.setPos(self.panda.getPos() + (self.pandaCarot.getPos(render) - self.panda.getPos(render)) * value)
       
    def turn(self,value):
       self.panda.setH(self.panda.getH() + value);
       
    def color(self,value):
        self.panda.setColor(value)
        
###################### SYSTEM ################################################

    def exit(self):
        self.phidget.allLEDsOff()
        sys.exit()

w = World()

run()