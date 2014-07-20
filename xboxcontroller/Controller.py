import pygame

JOYSTICKS = None
TRIGGERS = None
BUTTONS = None
CONNECTED = None

def init():
    pygame.init()
    pygame.joystick.init()
    ControllerInitialized = pygame.joystick.get_init()
    if ControllerInitialized == True:
        NumberofControllers = pygame.joystick.get_count()
        #print NumberofControllers
        #assigns ID 0 as Controller 1
        Controller1 = pygame.joystick.Joystick(0)
        #print Controller1
        #returns name of controller
        #print Controller1.get_name()
        #initialize Controller1
        Controller1.init()
        #outputs
        #print "Number of Axes : " + str(Controller1.get_numaxes())
        #print "Number of Balls : " + str(Controller1.get_numballs())
        #print "Number of Buttons : " + str(Controller1.get_numbuttons())

        global JOYSTICKS
        global TRIGGERS
        global BUTTONS
        global CONNECTED

        JOYSTICKS = {"LeftX":0, "LeftY":0, "RightX":0, "RightY":0}
        TRIGGERS = {"Left":0, "Right": 0}
        BUTTONS = {"X": False, "A": False, "B": False, "Y": False, "LB": False, "RB": False, "Back": False, "Start": False}
        #DPAD = {"UP": , "DOWN": , "LEFT": , "RIGHT":}
        
        CONNECTED = True
        
def read():        
            global JOYSTICKS
            global TRIGGERS
            global BUTTONS
            AllEvents = pygame.event.get()
            for Event in AllEvents:

                
                #JOYSTICKS & TRIGGERS (registered as joystick events)
                if Event.type == pygame.JOYAXISMOTION:
                    # Checks for axis location of joystick event
                    # Assigns the value (position) of the event to a dictionary according to location
                    # Prints to the console the location of joystick event and the value (position) of the joystick
                      # Negative value on the X-axis represents left while positive value represents right
                      # Negative value on the Y-axis represents up while positive value represents down
                      # Triggers are by default -1.0, when pressed the position is between -1.0 and 1.0 where 1.0 is completely pressed
                    if Event.axis == 0: #LeftX
                        JOYSTICKS["LeftX"] = Event.value
                        #print "Left Joystick X-Axis : " + str(Event.value)
                    elif Event.axis == 1: #LeftY
                        JOYSTICKS["LeftY"] = Event.value
                        #print "Left Joystick Y-Axis : " + str(Event.value)
                    elif Event.axis == 2: #Left Trigger
                        TRIGGERS["Left"] = Event.value
                        #print "Left Trigger : " + str(Event.value)
                    elif Event.axis == 3: #RightX
                        JOYSTICKS["RightX"] = Event.value
                        #print "Right Joystick X-Axis : " + str(Event.value)
                    elif Event.axis == 4: #RightY
                        JOYSTICKS["RightY"] = Event.value
                        #print "Right Joystick Y-Axis : " + str(Event.value)
                    elif Event.axis == 5: #Right Trigger
                        TRIGGERS["Right"] = Event.value
                        #print "Right Trigger : " + str(Event.value)

                        
                #BUTTONS (registered as button events)
                if Event.type == pygame.JOYBUTTONDOWN:
                    if Event.button == 0:
                        BUTTONS["A"] = True
                        #print "A : DOWN"
                    elif Event.button == 1:
                        BUTTONS["B"] = True
                        #print "B : DOWN"
                    elif Event.button == 2:
                        BUTTONS["X"] = True
                        #print "X : DOWN"
                    elif Event.button == 3:
                        BUTTONS["Y"] = True
                        #print "Y : DOWN"
                    elif Event.button == 4:
                        BUTTONS["LB"] = True
                        #print "LB : DOWN"
                    elif Event.button == 5:
                        BUTTONS["RB"] = True
                        #print "RB : DOWN"
                    elif Event.button == 6:
                        BUTTONS["Back"] = True
                        #print "Back : DOWN"
                    elif Event.button == 7:
                        BUTTONS["Start"] = True
                        #print "Start : DOWN"
                    elif Event.button == 8:
                        pass
                        #This is the left joystick button
                    elif Event.button == 9:
                        pass
                        #This is the right joystick button
                if Event.type == pygame.JOYBUTTONUP:
                    if Event.button == 0:
                        BUTTONS["A"] = False
                        #print "A : UP"
                    elif Event.button == 1:
                        BUTTONS["B"] = False
                        #print "B : UP"
                    elif Event.button == 2:
                        BUTTONS["X"] = False
                        #print "X : UP"
                    elif Event.button == 3:
                        BUTTONS["Y"] = False
                        #print "Y : UP"
                    elif Event.button == 4:
                        BUTTONS["LB"] = False
                        #print "LB : UP"
                    elif Event.button == 5:
                        BUTTONS["RB"] = False
                        #print "RB : UP"
                    elif Event.button == 6:
                        BUTTONS["Back"] = False
                        #print "Back : UP"
                    elif Event.button == 7:
                        BUTTONS["Start"] = False
                        #print "Start : UP"
                    elif Event.button == 8:
                        pass
                        #This is the left joystick button
                    elif Event.button == 9:
                        pass
                        #This is the right joystick button
                #DPAD
#main()
