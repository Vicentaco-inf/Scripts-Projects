############################################################

		   PARAMETRIC MODELER 
			  V_1.0


Project made by Vicente Gras Mas

############################################################
############################################################

This project make models with a few parameters.
To work with it is necessary to have ParameticModeler.py 
(The app), DESK.png, oneLeg.png, Table.png and Launcher.sh 
optionally.

This app was made in a Linux Ubuntu_64bit image with python2.0
installed on it and executed in virtual box.

For run it, you need to execute on a linux terminal the script
Launcher.sh, it will install all the necessary  packages and 
libraries for make the interface and the tools to our app for 
work, in case that the script seems to not work, try to install
manually the next orders on a terminal:

sudo apt install python-pip
pip install openpyscad
sudo apt-get install python-tk
sudo add-apt-repository ppa:openscad/releases
sudo apt-get install openscad

And then run ./ParametricModeler

############################################################
############################################################

The folder Example models contains a few example models 
generated on .scad and .stl.

it contains the next models:

-A desk without drawers and with drawers on the left side.
-A oneLeg Table Round with a round leg and square with square
legs.
-A Table round with round legs and square with square legs.

############################################################
############################################################

The archive UseExample.mkv is a record of how to use the app
and what produces the app, generating a few examples in stl 
and scad.