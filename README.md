HOUSEDROID
==========

To load code onto the raspberry pi, do the following:<br>
1) Type

	./genMainProg.sh

2) Move the contents of "./main program/" to the sdcard's home folder<br>
3) If you have not done this already, type in the following to make the program start at boot:<br>
  At the raspberry pi, type:

	$ cd ~/.config
	$ if [ ! -d autostart ]; then mkdir autostart; fi
	$ cd autostart
	$ echo -e "[Desktop Entry]\nType=Application\nExec=lxterminal" >HouseDroid.desktop
	$ cd ~/
	$ if [ ! -f .bashrc ]; then echo "" >.bashrc; fi
	$ echo "python RobotClient.py" >HouseDroidcmd.txt
	$ cat .bashrc HouseDroidcmd.txt >.bashrc.tmp
	$ rm HouseDroidcmd.txt
	$ mv .bashrc.tmp .bashrc

Contributors:<br>
<ul>
    <li>Eric Bronner</li>
    <li>Edward Choi</li>
    <li>Alison Wong</li>
    <li>Patrick Wu</li>
    <li>Lawrence Yong</li>
    <li>Timothy Yong</li>
</ul>

