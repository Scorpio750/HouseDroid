#!/bin/bash
if [ -d main\ program ]; then
  rm -rf main\ program
fi
mkdir main\ program

# get the platform in there
cp platform/ArduinoSerial.py main\ program/
cp platform/RobotClient.py main\ program/

# get the controller in there as well for now
cp xboxcontroller/Controller.py main\ program/
