HOUSEDROID
==========

To load code onto the raspberry pi, do the following:<br>
1) In the HouseDroid folder, type:

	$ ./genMainProg.sh

2) Move the contents of "./main program/" to the sdcard's home folder<br>
3) If you have not done this already, type in the following to make the program start at boot:<br>
  In the raspberry pi home folder, type:

	$ ./scripts/setupHouseDroid.sh

Contributors:<br>
<ul>
    <li>Eric Bronner</li>
    <li>Edward Choi</li>
    <li>Patrick Wu</li>
    <li>Lawrence Yong</li>
    <li>Timothy Yong</li>
</ul>

Dependencies (apt-get or pacman or brew):
<ul>
    <li>sphinx-base</li>
    <li>pocketsphinx-dev</li>
    <li>libopencv-dev</li>
    <li>python-opencv</li>
    <li>libgstreamer1.0-dev</li>
    <li>python-gst-1.0</li>
    <li>libfreenect-dev</li>
    <li>python-freenect</li>
    <li>arduino</li>
</ul>

Python Dependencies (pip):
<ul>
    <li>requests</li>
    <li>numpy</li>
    <li>pygame</li>
    <li>serial</li>
</ul>

