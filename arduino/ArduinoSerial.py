## @package ArduinoSerial
import serial, sys

debug = False
query = 0
virtual_connection = ["chassis", "claw"]

# This is a connection class
class Connection():
  ## constructor for the Connection object
  #  @param self
  #     the object pointer
  #  @param port
  #     (optional) the port at which the device is located
  #  @param baudrate
  #     (optional) the baudrate of the serial connection
  def __init__(self, port = "/dev/ttyUSB0", baudrate = 9600):
    self.port = port
    self.baudrate = baudrate
    self.databuffer = ""
    self.connection = None
    self.previouswrite = ""
    if not self.connect(port, baudrate):
      print "Unable to connect to {0}".format(port)
      #self.disconnect()
      #sys.exit(0)
    else:
      print "Connection successful"
 
  ## connect to a device
  #  @param self
  #     the object pointer
  #  @param port
  #     the port at which the device is located
  #  @param baudrate
  #     the baudrate of the serial connection
  #  @return
  #     boolean representing if connection successful
  def connect(self, port, baudrate):
    self.disconnect()
    self.baudrate = baudrate
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

  ## tries to identify if the device is connected
  #  @param self
  #     the object pointer
  #  @return
  #     boolean representing if connection successful
  def connected(self):
    return self.connection != None

  ## disconnect the current device
  #  @param self
  #     the object pointer
  #  @return
  #     None
  def disconnect(self):
    if self.connected():
      if not debug:
        self.connection.close()
        print "Disconnected"
      if debug:
        print "Debug disconnected"
      self.connection = None

  ## try to parse arduino specific data
  #  @param self
  #     the object pointer
  #  @param string
  #     the string of data to be evaluated
  #  @return
  #     positions of start and end on success, or None on error
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

  ## try to read in data
  #  @param self
  #     the object pointer
  #  @return
  #     an evaluated datastring
  def read(self):
    if debug:
      global virtual_connection
      global query
      if query >= len(virtual_connection):
        return None
      else:
        ID = virtual_connection[query]
        query += 1
        return [ID]
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
        string = eval(rawString)
        return string
      except:
        return ""

  ## tries to write to serial
  #  @param self
  #     the object pointer
  #  @param message
  #     the message to send over serial to device
  #  @return
  #     None
  def write(self, message):
    if message != self.previouswrite:
      self.previouswrite = message
      if not debug:
        self.connection.write(message)
      #if debug:
      print "Writing: " + str(message)

