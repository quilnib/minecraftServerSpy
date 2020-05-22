import requests
import math
import time
import json
from gpiozero import PWMLED

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Raspberry Pi pin configuration:
RST = 24
redPin = 22

# Config file
confFile = '/home/pi/Documents/minecraftServerSpy/minecraftServer.conf'

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load font
font = ImageFont.truetype(font="Minecraft.ttf", size=30)

# Create drawing object.
draw = ImageDraw.Draw(image)

def main():
    firstRun = True
    lastRunTimestamp = time.time()
    players = []
    numOnline = 0
    redLed = PWMLED(redPin)
    while True:
        if (lastRunTimestamp + 300) < time.time() or firstRun == True:
            firstRun = False
            lastRunTimestamp = time.time()
            try:
                f = open(confFile, 'r')
                serverInfo = json.loads(f.read())
                f.close()
                #print("checking server status. " + str(time.time()))
                r = requests.get("https://api.mcsrvstat.us/2/" + serverInfo['ipAddress'], timeout=10).json()
                numOnline = r['players']['online']
                if numOnline > 0:
                    players = r['players']['list']
                    redLed.pulse()
                    #print(players)
                else:
                    players = []
                    redLed.off()
                    #print("didn't find any players")
            except Exception as e:
                redLed.blink(1,1,0,0,15,True)
                scrollText(e)
        if numOnline > 0:
            scrollText(listToString(players))
        else:
            scrollText("no one online")     
    

def scrollText(scrollText):

    # Define text and get total width.
    text = scrollText
    maxwidth, unused = draw.textsize(text, font=font)

    # Set animation parameters.
    velocity = -4
    startpos = width

    # Animate text
    pos = startpos
    while pos > -maxwidth:#scroll the text once
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Enumerate characters
        x = pos
        for i, c in enumerate(text):
            # Stop drawing if off the right side of screen.
            if x > width:
                break
            # Calculate width but skip drawing if off the left side of screen.
            if x < -10:
                char_width, char_height = draw.textsize(c, font=font)
                x += char_width
                continue
            y = 20
            # Draw text.
            draw.text((x, y), c, font=font, fill=255)
            # Increment x position based on chacacter width.
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
        # Draw the image buffer.
        disp.image(image)
        disp.display()
        # Move position for next frame.
        pos += velocity
        # Pause briefly before drawing next frame.
        time.sleep(0.01)

def listToString(s):
    str1 = ""
    if len(s) > 1:
        str1 = ", "
    return(str1.join(s))

if __name__ == '__main__':
        main()

