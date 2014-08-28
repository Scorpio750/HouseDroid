import sys, os
dllname = "libcontroller.so.1"
if not dllname in os.listdir("."):
  print "Error: cannot find libcontroller.so in the current directory"
  sys.exit(1)
from ctypes import *
libcontroller = CDLL("./" + dllname)

class _joystick_(Structure):
  _fields_ = [("pressed", c_int8),
              ("x",       c_float),
              ("y",       c_float)]

class _controller_(Structure):
  _fields_ = [("name",      POINTER(c_char)),
              ("fd",        c_int32),
              ("connected", c_int8),
              ("buttons",   c_int32),
              ("axes",      c_int32),
              ("thread",    c_uint64),  # hack
              ("alive",     c_int8),
              ("A",         c_int8),
              ("B",         c_int8),
              ("X",         c_int8),
              ("Y",         c_int8),
              ("UP",        c_int8),
              ("DOWN",      c_int8),
              ("LEFT",      c_int8),
              ("RIGHT",     c_int8),
              ("LB",        c_int8),
              ("RB",        c_int8),
              ("LT",        c_float),
              ("RT",        c_float),
              ("LJOY",      _joystick_),
              ("RJOY",      _joystick_),
              ("START",     c_int8),
              ("SELECT",    c_int8),
              ("HOME",      c_int8)]

class controller(object):
  def __init__(self):
    self.data = _controller_()

  def connect(self):
    libcontroller.controller_connect(byref(self.data))
    if self.data.connected == 0:
      sys.exit(1)

  def connected(self):
    return self.data.connected

  def disconnect(self):
    libcontroller.controller_disconnect(byref(self.data))

  def buttons(self):
    return self.data.buttons

  def axes(self):
    return self.data.axes
