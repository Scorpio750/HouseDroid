import ArduinoSerial
import sys, signal, os
import Controller

exit_signal = False
sensitivity = 0.2

connected_ports = []

def endclient_handler(signo, frame):
  print "Caught exit signal, exiting"
  global exit_signal
  exit_signal = True

def convinput(value):
  global sensitivity
  if value >= -sensitivity and value <= sensitivity:
    return 0
  else:
    return int(float(value) * 100.0)

def limitoutput(value):
  value = convinput(value)
  if value > 100:
    return 100
  elif value < -100:
    return -100
  else:
    return value

def connect():
  global connected_ports
  ls = os.listdir("/dev")
  usb = filter(lambda s: s.find("USB") != -1, ls)
  acm = filter(lambda s: s.find("ACM") != -1, ls)
  print "ports:"
  print usb
  print acm
  connection = None
  for port in usb:
    if port in connected_ports:
      continue
    connection = ArduinoSerial.Connection(port = "/dev/" + port, baudrate = 57600)
    if connection.connected():
      connected_ports.append(port)
      break
  if not connection or not connection.connected():
    for port in acm:
      if port in connected_ports:
        continue
      connection = ArduinoSerial.Connection(port = "/dev/" + port, baudrate = 57600)
      if connection.connected():
        connected_ports.append(port)
        break
  if not connection or not connection.connected():
    connection = None
  else:
    print "connected to: " + port
    connected_ports.append(port)
  return connection

def disconnectAll(connections):
  for c in connections:
    if c and c.connected():
      c.disconnect()

def main():

  signal.signal(signal.SIGINT, endclient_handler)
  if "--debug" in sys.argv:
    ArduinoSerial.debug = True

  # try to connect to the robot
  connections = [connect(), connect()]
  for c in connections:
    if c == None:
      print "Cannot connect to robot"
      disconnectAll(connections)
      sys.exit(1)
  claw = None
  chassis = None
  i = 0
  for c in connections:
    data = c.read()
    while data == None:
      print "waiting on connection {0}".format(i)
      data = c.read()
    i += 1
    if len(data) == 0:
      continue
    if data[0] == "chassis":
      chassis = c
      print "Connected to chassis"
    elif data[0] == "claw":
      claw = c
      print "Connected to claw"
    else:
      print "Conntected to <unidentified>"
  if not claw or not chassis:
    print "Cannot find claw [OR] chassis"
    disconnectAll(connections)
    sys.exit(1)
  
  # reset
  chassis.write("[000000000]")
  claw.write("[000]")

  # try to connect to te controller
  controller = Controller.controller()
  controller.connect()

  # control the robot
  while not exit_signal:

    X = controller.data.RJOY.x
    Y = controller.data.LJOY.y
    leftside = limitoutput(X - Y)
    rightside = limitoutput(-X - Y)

    arm = 0
    if buttons["LB"] and buttons["RB"]:
      arm = 0
    elif buttons["LB"]:
      arm = 100
    elif buttons["RB"]:
      arm = -100
    else:
      arm = 0

    hand = 0
    if triggers["Left"] > 0 and triggers["Right"] > 0:
      hand = 0
    elif triggers["Left"] > 0:
      hand = 100
    elif triggers["Right"] > 0:
      hand = -100
    else:
      hand = 0

    def getmotor(value):
      mv = 0
      if value < 0:
        mv = -value + 100
      else:
        mv = value
      return ("000" + str(mv))[-3:]

    chassis.write("[{0}{1}{2}]".format(getmotor(rightside), getmotor(leftside), getmotor(arm)))
    claw.write("[{0}]".format(getmotor(hand)))
    data = chassis.read()
    if data != None:
      print "Reading [chassis]: {0}".format(data)
    data = claw.read()
    if data != None:
      print "Reading [claw]: {0}".format(data)

  chassis.write("[000000000]")
  claw.write("[000]")
  controller.disconnect()
  disconnectAll(connections)

if __name__ == "__main__":
  main()

