import Controller
import ArduinoSerial
import sys, signal

exit_signal = False
sensitivity = 0.7

def endclient_handler(signo, frame):
  print "Caught exit signal, exiting"
  global exit_signal
  exit_signal = True

def main():

  signal.signal(signal.SIGINT, endclient_handler)

  if "--debug" in sys.argv:
    ArduinoSerial.debug = True

  OFF = 0
  FORWARD = 1
  BACKWARD = 2

  print "Connecting to /dev/ttyUSB0"
  Robot = ArduinoSerial.Connection(port = "/dev/ttyUSB0", baudrate = 38400)
  while not Robot.connected():
    print "Connecting to /dev/ttyACM0"
    Robot = ArduinoSerial.Connection(port = "/dev/ttyACM0", baudrate = 38400)
    if Robot.connected():
      break
    print "Connecting to /dev/ttyUSB0"
    Robot = ArduinoSerial.Connection(port = "/dev/ttyUSB0", baudrate = 38400)

  while not Controller.CONNECTED:
    Controller.init()

  # speed: 
  rightside = OFF
  leftside = OFF
  arm = OFF
  claw = OFF

  Robot.write("[000000]")

  global sensitivity

  while not exit_signal:
    Controller.read()
    joysticks = Controller.JOYSTICKS
    triggers = Controller.TRIGGERS
    buttons = Controller.BUTTONS

    leftside = 0
    rightside = 0

    if joysticks["LeftY"] > sensitivity:
      leftside -= 1
      rightside -= 1
    elif joysticks["LeftY"] < -sensitivity:
      leftside += 1
      rightside += 1

    if joysticks["RightX"] > sensitivity:
      leftside -= 1
      rightside += 1
    elif joysticks["RightX"] < -sensitivity:
      leftside += 1
      rightside -= 1

    if leftside < 0:
      leftside = 2
    elif leftside > 0:
      leftside = 1
    if rightside < 0:
      rightside = 2
    elif leftside > 0:
      rightside = 1

    if triggers["Left"] > 0.0 and triggers["Right"] > 0.0:
      arm = OFF
    elif triggers["Left"] > 0.0:
      arm = FORWARD
    elif triggers["Right"] > 0.0:
      arm = BACKWARD
    else:
      arm = OFF

    if buttons["LB"] and buttons["RB"]:
      claw = OFF
    elif buttons["LB"]:
      claw = FORWARD
    elif buttons["RB"]:
      claw = BACKWARD
    else:
      claw = OFF

    Robot.write("[{0}{1}{2}{3}{4}{5}]".format(abs(rightside), abs(leftside), abs(arm), abs(arm), abs(claw), abs(claw)))
    data = Robot.read()
    if data != None:
      print "Reading: {0}".format(data)

  Robot.disconnect()

if __name__ == "__main__":
  main()

