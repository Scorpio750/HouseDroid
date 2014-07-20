#!/bin/bash
if [ ! -d .config ]; then mkdir .config; fi
cd .config
if [ ! -d autostart ]; then mkdir autostart; fi
cd autostart
echo -e "[Desktop Entry]\nType=Application\nExec=lxterminal" >HouseDroid.desktop
cd ../../
if [ ! -f .bashrc ]; then touch .bashrc; fi
echo -e "\n# HouseDroid\npython RobotClient.py" >HouseDroidcmd.txt
cat .bashrc HouseDroidcmd.txt >.bashrc.tmp
rm HouseDroidcmd.txt
mv .bashrc.tmp .bashrc
