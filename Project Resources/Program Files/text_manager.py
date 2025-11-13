## IMPORTS ##

from machine import Pin, I2C
from machine_i2c_lcd import I2cLcd

import networking

from time import sleep
import uasyncio as asyncio

## VARIABLES ##

# Hardware

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000) # Declare I2C screen module

lcdAddr = 0x27
lcdRows = 2
lcdColumns = 16
lcd = I2cLcd(i2c, lcdAddr, lcdRows, lcdColumns)

# Display

currentBottomScreenMessage = "No Outstanding Issues, Have a Nice Day               " # 15 spaces added to ensure message fully scrolls off

alarmIcon = bytearray([0x00, 0x04, 0x0E, 0x0E, 0x0E, 0x1F, 0x00, 0x04]) # Also create a connection icon at some point
lcd.custom_char(1, alarmIcon)

## FUNCTIONS ##

def clearDisplay():
    lcd.clear()

def displayIcons(notified, connected):
    lcd.move_to(0,0)
    if connected == True:
        lcd.putchar(chr(0))
    else:
        lcd.putstr(" ")
    if notified == True:
        lcd.putchar(chr(1))
    else:
        lcd.putstr(" ")


def displayTime():
    lcd.move_to(11,0)
    localTime = networking.localTime()
    currentTime = "{:02d}:{:02d}".format(t[3], t[4])
    lcd.putstr(currentTime)


async def scrollMessage(message, delay, row, repeat=False):
    message = " " * lcdColumns + message + " "
    if repeat:
        while True:
            for i in range(len(message) - lcdColumns + 1):
                lcd.move_to(0, row)
                lcd.putstr(message[i:i + lcdColumns])
                await asyncio.sleep(delay)
    else:
        for i in range(len(message) - lcdColumns + 1):
            lcd.move_to(0, row)
            lcd.putstr(message[i:i + lcdColumns])
            await asyncio.sleep(delay)

async def dynamicScrollMessage(row, delay=0.2):
    global currentBottomScreenMessage
    last_message = ""

    while True:
        message = currentBottomScreenMessage
        if message != last_message:
            scroll_text = " " * lcdColumns + message + " "
            last_message = message
        else:
            scroll_text = " " * lcdColumns + message + " "

        for i in range(len(scroll_text) - lcdColumns + 1):
            if currentBottomScreenMessage != last_message:
                break
            lcd.move_to(0, row)
            lcd.putstr(scroll_text[i:i + lcdColumns])
            await asyncio.sleep(delay)