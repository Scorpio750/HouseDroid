import serial, sys

debug = False

class Connection():
  def __init__(self, port = "/dev/ttyUSB0", baudrate = 9600):
    self.port = port
    self.baudrate = baudrate
    self.databuffer = ""
    self.connection = None
    self.previouswrite = ""
    if not self.connect(port, baudrate):
      print "Unable to connect to {0}, exiting.".format(port)
      #self.disconnect()
      #sys.exit(0)
    else:
      print "Connection successful"
 
  def connect(self, port, baudrate):
    self.disconnect()
    try:
      if not debug:
        self.connection = serial.Serial(port, baudrate)
        print "Connected"
      if debug:
        self.connection = "Connected"
        print "Debug connected"
      return True
    except serial.serialutil.SerialException:
      self.connection = None
      return False

  def connected(self):
    return self.connection != None

  def disconnect(self):
    if self.connection != None:
      if not debug:
        self.connection.close()
        print "Disconnected"
      if debug:
        print "Debug disconnected"
      self.connection = None

  def parseData(self, string):
    backstring = string[::-1]
    endpos = backstring.find("]")
    if endpos == -1:
      return None
    startpos = backstring[endpos:].find("[") + endpos
    if startpos == -1:
      return None
    startpos += 1
    return [len(backstring) - startpos, len(backstring) - endpos]

  def read(self):
    if debug:
      return
    byteWait = self.connection.inWaiting()
    if byteWait:
      self.databuffer += self.connection.read(byteWait)
      # shorten buffer
      if len(self.databuffer) > 512:
        self.databuffer = self.databuffer[-512:]

    pos = self.parseData(self.databuffer)
    if pos == None:
      return None
    else:
      rawString = self.databuffer[pos[0]:pos[1]]
      # shorten buffer
      self.databuffer = self.databuffer[pos[1]:]
      try:
        string = eval (rawString)
        return string
      except:
        return ""

  def write(self, message):
    if message != self.previouswrite:
      self.previouswrite = message
      if not debug:
        self.connection.write(message)
      #if debug:
      print "Writing: " + str(message)

