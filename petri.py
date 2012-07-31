##############################################################################
## Program Name (File Name): Caps.py
## Programmer: Branden Youssef
## Purpose: PB Week 1 Project
## Date: 7/9/12
## Additional Notes:
##   -This is a basic template for you to use in starting your programming
##    homework assignment.
##      -There are some useful functions that might be helpful, though I
##       haven't given you everything you'll need.
##
##   -You do not have to use everything in here if you don't want to
##    this is just to give you an extra bump along 'correct' path.
##
##   -Feel free to rename anything you want, or to even start from scratch.
##
##   -To help some of the functions have been named and a very brief comment
##    is there to sort of give you an idea of what it might be used for.
##############################################################################
# Python specific Imports
import sys
import random
import math

# Panda specific imports
import direct.directbase.DirectStart                                     
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.gui.DirectGui import OnscreenText

# Program specific imports
import random

# Constants

####### Start: World Class Definition ########################################
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
        self.robot.setPosHpr(0,0,-.025,0,0,0)
        self.robot.setScale(0.0025)
        ## self.robot.place()
        # Load the mana orbs
        ## self.mana = []
        ## for i in range(NUM_RINGS):
            ## for j in range(NUM_ORBS):
        self.mana = (loader.loadModel("Models/petridish.egg"))
        self.mana.reparentTo(render)
        self.manaTex = loader.loadTexture("Textures/HEX_Blue.jpg")
        self.mana.setTexture(self.manaTex,1)
        self.mana.setPos(-self.deltaFunc(0.7019,3.0,0.875),-.05,self.deltaFunc(1.072,3.0,0.875))
        self.mana.setHpr(0,0,0)
        self.mana.setScale(0.00005)
        
        self.mana2 = (loader.loadModel("Models/petridish.egg"))
        self.mana2.reparentTo(render)
        self.manaTex = loader.loadTexture("Textures/HEX_Green.jpg")
        self.mana2.setTexture(self.manaTex,1)
        self.mana2.setPos(-self.deltaFunc(2.066,2.5,0.75),-.05,self.deltaFunc(0.03798,2.5,0.75))
        self.mana2.setHpr(0,0,0)
        self.mana2.setScale(0.00005)
        
        self.mana3 = (loader.loadModel("Models/petridish.egg"))
        self.mana3.reparentTo(render)
        self.manaTex = loader.loadTexture("Textures/HEX_Red.jpg")
        self.mana3.setTexture(self.manaTex,1)
        self.mana3.setPos(-self.deltaFunc(3.0,2.0,0.625),-.05,self.deltaFunc(0.2679,2.0,0.625))
        self.mana3.setHpr(0,0,0)
        self.mana3.setScale(0.00005)
        
        self.mana4 = (loader.loadModel("Models/petridish.egg"))
        self.mana4.reparentTo(render)
        self.manaTex = loader.loadTexture("Textures/HEX_Yellow.jpg")
        self.mana4.setTexture(self.manaTex,1)
        self.mana4.setPos(-self.deltaFunc(2.91,1.5,0.5),-.05,self.deltaFunc(0.987,1.5,0.5))
        self.mana4.setHpr(0,0,0)
        self.mana4.setScale(0.00005)
                            
        self.mana5 = (loader.loadModel("Models/petridish.egg"))
        self.mana5.reparentTo(render)
        self.manaTex = loader.loadTexture("Textures/HEX_Red.jpg")
        self.mana5.setTexture(self.manaTex,1)
        self.mana5.setPos(-self.deltaFunc(1.94,1.0,0.375),-.05,-self.deltaFunc(0.658,1.0,0.375))
        self.mana5.setHpr(0,0,0)
        self.mana5.setScale(0.00005)
        
        self.mana6 = (loader.loadModel("Models/petridish.egg"))
        self.mana6.reparentTo(render)
        self.manaTex = loader.loadTexture("Textures/HEX_Green.jpg")
        self.mana6.setTexture(self.manaTex,1)
        self.mana6.setPos(-self.deltaFunc(0.75,.5,0.25),-.05,-self.deltaFunc(0.067,.5,0.25))
        self.mana6.setHpr(0,0,0)
        self.mana6.setScale(0.00005)
        
        
    def deltaFunc(self,v,r,mult):
        #radius of petri dish
        R=.6
        V = R*mult-((R*mult*v)/r)
        print V
        return V
        
        # Quit Game Function
    def quit(self):
        # Print Goodbye Message 
        print "Bye! Thank you for playing."
        # Exit out of the game
        sys.exit()
######## End: World Class Definition #########################################

# Create an instance of class World
w = World() # Stored as "w"
# Run the program
run()