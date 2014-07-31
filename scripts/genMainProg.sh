#!/bin/bash
if [ -d main\ program ]; then
  rm -rf main\ program
fi
cd ..
mkdir main\ program

# get the setup script in there to autostart the program
cp scripts/setupHouseDroid.sh main\ program/

# get the core in there
cp core/ArduinoSerial.py main\ program/
cp core/RobotClient.py main\ program/

# get the controller in there as well for now
cp gamepads/Controller.py main\ program/
