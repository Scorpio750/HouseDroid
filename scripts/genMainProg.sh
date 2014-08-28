#!/bin/bash
cd ..
if [ -d main\ program ]; then
  rm -rf main\ program
fi
mkdir main\ program

# get the setup script in there to autostart the program
cp scripts/setupHouseDroid.sh main\ program/

# get the core in there
cp core/RobotClient.py main\ program/RobotClient.py
cp arduino/ArduinoSerial.py main\ program/ArduinoSerial.py

# get the controller in there as well for now
cd manual_control/controller
make
cd ../..
cp manual_control/controller/controller.py main\ program/Controller.py
cp manual_control/controller/libcontroller.so.1 main\ program/libcontroller.so.1
