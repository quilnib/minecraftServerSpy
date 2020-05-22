# minecraftServerSpy
Check who is currently playing on your Minecraft server and display to an OLED screen

Followed this tutorial to set up the OLED screen and install the necessary AdaFruit libraries.

You'll also want to make sure you have the latest version of gpiozero installed to control your notification LED

Change the reference to your .conf file (line 19 in minecraftServerStatus.py) to whichever
directory you install this repo to. Then add your server's IP address to the .conf file.

You'll get a 121 error if you don't have an I2C device connected to your Pi before trying to run the code. 