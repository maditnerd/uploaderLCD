#!/usr/bin/env python
# UploaderLCD
import time
import os
import Adafruit_CharLCD as LCD

debounceTime = 0.3
scriptsDir = "/user/arduino/"
waitBeforeHalt = 3
messageWait = 2

def loadSketches(lcd, sketch):
    lcd.clear()
    lcd.set_color(1.0, 1.0, 0.0)
    lcd.message("Loading:\n" + str(sketch))
    returnValue = os.system("/do/platformio/runNano " + str(sketch))
    if(returnValue != 0):  # 512
        lcd.clear()
        lcd.set_color(1.0, 0.0, 0.0)
        lcd.message("Upload failed")
        time.sleep(messageWait)
    if(returnValue == 0):
        lcd.clear()
        lcd.set_color(0.0, 1.0, 0.0)
        lcd.message("Upload OK")
        time.sleep(messageWait)
        loadTest(lcd, sketch)


def loadTest(lcd, sketch):
    lcd.clear()
    lcd.set_color(1.0, 1.0, 0.0)
    lcd.message("Testing:\n" + str(sketch))
    testExists = os.path.isfile(scriptsDir + sketch + "/test/test.py")
    if testExists:
        returnValue = os.system("/do/platformio/test " + sketch)
        # print returnValue
        if(returnValue == 512):
            lcd.clear()
            lcd.set_color(1.0, 0.0, 0.0)
            lcd.message("Test failed")
            time.sleep(messageWait)
        if(returnValue == 0):
            lcd.clear()
            lcd.set_color(0.0, 1.0, 0.0)
            lcd.message("Test OK")
            time.sleep(messageWait)
    else:
        lcd.clear()
        lcd.set_color(1.0, 0.0, 0.0)
        lcd.message("No test found")
        time.sleep(3)


def initLCD(lcd):
    lcd.set_color(1.0, 1.0, 0.0)
    lcd.clear()
    lcd.message('Loading sketches')


def displayFirstSketch(lcd, dirs):
    lcd.set_color(1.0, 1.0, 1.0)
    lcd.clear()
    lcd.message(dirs[0])


def displaySketch(lcd, sketch):
    lcd.set_color(1.0, 1.0, 1.0)
    lcd.clear()
    lcd.message(sketch)


def MainMenu(lcd, dirs):
    dirPosition = 0
    nbDir = len(dirs) - 1

    # Main Menu
    mainMenu = True
    while mainMenu:
        if lcd.is_pressed(LCD.UP):
            if dirPosition == nbDir:
                dirPosition = 0
            else:
                dirPosition = dirPosition + 1
            lcd.clear()
            lcd.message(dirs[dirPosition])
            time.sleep(debounceTime)

        if lcd.is_pressed(LCD.DOWN):
            dirPosition = dirPosition - 1
            if dirPosition == -1:
                dirPosition = nbDir
            lcd.clear()
            lcd.message(dirs[dirPosition])
            time.sleep(debounceTime)
        if lcd.is_pressed(LCD.RIGHT):
            loadSketches(lcd, dirs[dirPosition])
            displaySketch(lcd, dirs[dirPosition])
        if lcd.is_pressed(LCD.LEFT):
            loadTest(lcd, dirs[dirPosition])
            displaySketch(lcd, dirs[dirPosition])
        if lcd.is_pressed(LCD.SELECT):
            waiting = waitBeforeHalt
            while lcd.is_pressed(LCD.SELECT):
                lcd.clear()
                lcd.set_color(1.0, 0.0, 0.0)
                lcd.message("Exit : " + str(waiting))
                waiting = waiting - 1
                time.sleep(1)
                if waiting == 0:
                    lcd.clear()
                    lcd.set_color(1.0, 0.0, 1.0)
                    lcd.message("System stopped\nPlease wait")
                    os.system("/sbin/halt")
                    os._exit()
            displaySketch(lcd, dirs[dirPosition])

# Initialize the LCD using the pins
print "Program started"
lcd = LCD.Adafruit_CharLCDPlate()
initLCD(lcd)
print "LCD init"
dirs = os.listdir(scriptsDir)

print "Display first sketch"
displayFirstSketch(lcd, dirs)

print "Main Menu"
try:
    MainMenu(lcd, dirs)
except:
    lcd.clear()
    lcd.set_color(1.0, 0.0, 0.0)
    lcd.message("FATAL ERROR")
