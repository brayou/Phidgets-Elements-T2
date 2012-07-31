#Basic imports
from threading import *
from ctypes import *
import sys
import math
import time 
import subprocess

#Phidget specific imports
from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import *
from Phidgets.Devices.LED import *
from Phidgets.Devices.TextLCD import TextLCD
from Phidgets.Devices.RFID import *

#Panda specific imports
import direct.directbase.DirectStart 
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task 
from direct.actor import Actor 
from direct.interval.IntervalGlobal import * 

#Program specific imports
from interface_config import *




class Phidget(DirectObject): 
    def __init__(self):
        
        self.afterSetup = False
            
        # start the LED Controller
        self.startLED()
        
        # start the interface
        self.startInterface()
        
        # start the RFID
        ## self.startRFID()
        
        # accepts 
        self.accept( "o", self.allLEDsOff)
        
        time.sleep(5)
        self.afterSetup = True
        
        
        

###################### INTERFACING ###########################################
###################### DO NOT TOUCH THIS #####################################

    def inferfaceKitAttached(self,e):
        attached = e.device
        print "PM - InterfaceKit %i Attached!" % (attached.getSerialNum())
        return 0

    def interfaceKitDetached(self,e):
        detached = e.device
        print "PM - InterfaceKit %i Detached!" % (detached.getSerialNum())
        return 0

    def interfaceKitError(self,e):
        print "PM - Phidget Error %i: %s" % (e.eCode, e.description)
        return 0

    def interfaceKitInputChanged(self,e):
        print "PM - Device %i Input %i: %s" % (e.device, e.index, e.state)
        # which starterKit is this
        kit = DEVICE_SERIALS.index(e.device)
        # find the device 
        if INPUTS[kit][e.index] == "button":
            self.handleButton(e.index, e.state, kit)
        return 0

    def interfaceKitSensorChanged(self,e):
        ## print "PM - Device %i Sensor %i: %i" % (e.device, e.index, e.value)
        # which starterKit is this
        kit = DEVICE_SERIALS.index(e.device)
        # find the device 
        if SENSORS[kit][e.index] == "touch":
            self.handleTouch(e.index, e.value, kit)
        elif SENSORS[kit][e.index] == "motion":
            self.handleMotion(e.index, e.value, kit)
        elif SENSORS[kit][e.index] == "IRref":
            self.handleIRref(e.index, e.value, kit)
        return 0

    def interfaceKitOutputChanged(self,e):
        ## print "PM - Output %i: %s" % (e.index, e.state)
        return 0
    
    def startInterface(self):
        self.interfaceKit = [None] * NUM_INTERFACES
        for i in range(NUM_INTERFACES):
            #Create an interfacekit object
            self.interfaceKit[i] = InterfaceKit()
            
            # setup handlers
            self.interfaceKit[i].setOnAttachHandler(self.inferfaceKitAttached)
            self.interfaceKit[i].setOnDetachHandler(self.interfaceKitDetached)
            self.interfaceKit[i].setOnErrorhandler(self.interfaceKitError)
            self.interfaceKit[i].setOnInputChangeHandler(self.interfaceKitInputChanged)
            self.interfaceKit[i].setOnOutputChangeHandler(self.interfaceKitOutputChanged)
            ## self.interfaceKit[i].setOnSensorChangeHandler(self.interfaceKitSensorChanged)
            
            # look for the interface
            self.interfaceKit[i].openPhidget(DEVICE_SERIALS[i])
            self.interfaceKit[i].waitForAttach(10000)
            
###################### RFID CONTROLLER #######################################
###################### DO NOT TOUCH THIS #####################################
            
    #Event Handler Callback Functions
    def rfidAttached(self,e):
        attached = e.device
        print "PM - RFID %i Attached!" % (attached.getSerialNum())
        print e
        return 0

    def rfidDetached(self,e):
        detached = e.device
        print "PM - RFID %i Detached!" % (detached.getSerialNum())
        return 0

    def rfidError(self,e):
        ## source = e.device
        print "PM - RFID: Phidget Error %i: %s" % (e.eCode, e.description)
        return 0
    
    def rfidOutputChanged(self,e):
        print "PM - RFID: Output %i State: %s" % (e.index, e.state)

    def rfidTagGained(self,e):
        ## rfid.setLEDOn(1)
        print("PM - RFID: Tag Read: %s" % (e.tag))
        self.handleRFIDtag(e.tag, "got")

    def rfidTagLost(self,e):
        ## rfid.setLEDOn(0)
        print("PM - RFID: Tag Lost: %s" % (e.tag))
        self.handleRFIDtag(e.tag, "lost")
    
    def startRFID(self):
        #Create an rfid object
        self.rfid = RFID()
        
        # setup handlers
        self.rfid.setOnAttachHandler(self.rfidAttached)
        self.rfid.setOnDetachHandler(self.rfidDetached)
        self.rfid.setOnErrorhandler(self.rfidError)
        self.rfid.setOnOutputChangeHandler(self.rfidOutputChanged)
        self.rfid.setOnTagHandler(self.rfidTagGained)
        self.rfid.setOnTagLostHandler(self.rfidTagLost)
        
        # look for the interface
        self.rfid.openPhidget() #(RFID_SERIAL)
        self.rfid.waitForAttach(10000)
        
###################### LED CONTROLLER ########################################
###################### DO NOT TOUCH THIS #####################################
            
    #Event Handler Callback Functions
    def ledAttached(self,e):
        attached = e.device
        print "PM - LED %i Attached!" % (attached.getSerialNum())
        return 0

    def ledDetached(self,e):
        detached = e.device
        print "PM - LED %i Detached!" % (detached.getSerialNum())
        return 0

    def ledError(self,e):
        print "PM - Phidget Error %i: %s" % (e.eCode, e.description)
        return 0
    
    def startLED(self):
        #Create an led object
        self.led = LED()
        
        # setup handlers
        self.led.setOnAttachHandler(self.ledAttached)
        self.led.setOnDetachHandler(self.ledDetached)
        self.led.setOnErrorhandler(self.ledError)
        
        # look for the interface
        self.led.openPhidget(LED_SERIAL)
        self.led.waitForAttach(10000)

###################### HANDLERS ##############################################

    def handleTouch(self,index,value,kit):
        for i in range(4):
            if kit == TOUCH[i][0] and index == TOUCH[i][1]:
                func = i
        # if value < 500 then the sensor has been touched
        if value < 500:
            ## print "PM - Got touch sensor:", kit, index
            # send a message to let the main program know
            messenger.send("touchRec", [T_FUNC[func]])
            # give feedback
            self.handleLED(BUT_LEDS[func][BUT_COL],BUT_LEDS_ON[BUT_COL])
        else:
            # give feedback
            self.handleLED(BUT_LEDS[func][BUT_COL],LED_OFF)
            
    def handleMotion(self,index,value,kit):
        if value < 400 or value > 600:          # something moved
            ## print "PM - Got motion sensor"
            # send a message to let the main program know
            messenger.send("motionRec", ["got"])
        else:                                   # no movement
            ## print "PM - Lost motion sensor"
            messenger.send("motionRec", ["lost"])
            
    def handleIRref(self,index,value,kit):
        for i in range(4):
            if kit == IRREF[i][0] and index == IRREF[i][1]:
                if value < 940:
                    v = IR_LEDS_ON          # turn the LEDs on
                    # send a message to let the main program know
                    messenger.send("irRec", [IR_FUNC[i]])
                else:
                    v = LED_OFF             # turn the LEDs off
                for j in range(4):
                    self.handleLED(IR_LEDS[i][j],v)
                    ## print "PM - Light LED:", i,j,v
        
    def handleButton(self,index,state,kit):
        if kit == 0:  
            if index   == 0:  # pressure plate button  
                if state:       # on
                    ## print "PM - Got Pressure Plate"
                    for i in range(5):
                        self.handleLED(BUT_LEDS[i][1],BUT_LEDS_ON[1])
                    # send a message to let the main program know
                    messenger.send("pressureRec", ["got"])
                else:           # off
                    ## print "PM - Lost Pressure Plate"
                    for i in range(5):
                        self.handleLED(BUT_LEDS[i][1],LED_OFF)
                    # send a message to let the main program know
                    messenger.send("pressureRec", ["lost"])
                    
    def handleRFIDtag(self, tag, state):
        # pass the tag along
        messenger.send("RFIDtagRec", [tag, state]) 
        # give feedback
        if state == "got":
            v = RFID_LEDS_ON        # turn the LEDs on
        else:
            v = LED_OFF             # turn the LEDs off
        for i in range(4):
            self.handleLED(RFID_LEDS[i],v)
     
     
###################### Interfacing Functions #################################

    def startPolling(self):
        # start the polling task
        taskMgr.doMethodLater(.1, self.poll, 'Poll Task')
        
    def stopPolling(self):
        # stop the polling task
        taskMgr.remove('Poll Task')
    
    def poll(self,task):
        # check all the sensor values on the interface kits
        for kit in range(NUM_INTERFACES):
            for index in range(8):
                if not SENSORS[kit][index] == None:
                    val = self.getSensor(index,kit)
                    # find the device 
                    if SENSORS[kit][index] == "touch":
                        self.handleTouch(index, val, kit)
                    elif SENSORS[kit][index] == "motion":
                        self.handleMotion(index, val, kit)
                    elif SENSORS[kit][index] == "IRref":
                        self.handleIRref(index, val, kit)
        return task.again
    
    def handleLED(self,index,value):
        # turn on/off a single led (or set with the top leds)
        self.led.setDiscreteLED(index, value)
        
    def allLEDsOff(self):
        # turn off every led on the console
        # it is important to run this at the start and end of the game
        for i in range(4):
            for j in range(2):
                self.handleLED(BUT_LEDS[i][j],LED_OFF)
        for i in range(4):
            for j in range(4):
                self.handleLED(IR_LEDS[i][j],LED_OFF)
        
    def getLED(self,index):
        # returns the current value of an led at index in a range from 0-100
        v = self.led.getDiscreteLED(index)
        if TEST: print "get channel", index, "=", v
        return v
        
    def getInput(self,index,kit):
        # returns the current value of an input on an interface
        s = self.interfaceKit[kit].getInputState(index)
        if TEST: print "get input for kit", kit, "index", index, "value:", s
        return s
        
    def getOutput(self,index,kit):
        # returns the current value of an output on an interface
        s = self.interfaceKit[kit].getOutputState(index)
        if TEST: print "get output for kit", kit, "index", index, "value:", s
        return s
        
    def setOutput(self,index,state,kit):
        # sets the value of an output on an interface
        if not self.interfaceKit[kit] == None: 
            self.interfaceKit[kit].setOutputState(index,state)   # timing issue
        if TEST: print "set output for kit", kit, "index", index, "state", state
        
    def getSensor(self,index,kit):
        # for device kit, return the value of sensor index
        val = -1
        if not self.interfaceKit[kit] == None: 
            val = self.interfaceKit[kit].getSensorValue(index) 
        ## print "PM - sensor value obtained:", kit, index, val
        return val

