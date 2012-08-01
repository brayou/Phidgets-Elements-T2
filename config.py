TEST_MODE = True

# how many interface kits are attached
NUM_INTERFACES = 1

DEVICE_SERIALS = [ 85215 ]


# SENSORS 

# lists of what sensors are attached  - indexed by device number
SENSORS = [["touch", "touch", "touch", "touch", "IRref", "IRref", "IRref", "IRref"],
           [] ]  
    
# lists that controls the function of the sensors 
T_FUNC =  ["Exit", "butt1", "butt2", "butt3"]
TOUCH  =  [ [0,3],  [0,2],  [0,1],   [0,0] ]       # device,port or kit,index

IR_FUNC = ["IR1", "IR2", "IR3", "IR4"]
IRREF  =  [[0,4], [0,5], [0,6],  [0,7] ]       # device,port or kit,index   

    
# INPUTS 

# lists of what inputs are attached - indexed by device number
INPUTS = [[None, None, None, None, None, None, None, None],
          [ None, None, None, None, None, None, None, None]]
           
# OUTPUTS 

# lists of what outputs are attached  - indexed by device number
OUTPUTS = [[None, None, None, None, None, None, None, None],
           [None, None, None, None, None, None, None, None]]


# LED Controller
LED_SERIAL = 41293

LED_OFF = 0     # value to send for all off

IR_LEDS = [ [60,61,62,63],
            [56,57,58,59],
            [52,53,54,55],
            [48,49,50,51] ]
            
IR_LEDS_ON = 100        # value to send for full on
            
BUT_LEDS = [[7,6],
            [5,4],
            [2,3],
            [1,0]]            #blue, green
            
BUT_LEDS_ON = [30,50]         #blue, green

BUT_COL = 0                     # 0 = blue, 1 = green

RFID_LEDS = [16,17,18,19]

RFID_LEDS_ON = 100        # value to send for full on




# RFID Controller
RFID_SERIAL = 61663




            


