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
cp manctrl/Controller.py main\ program/Controller.py
