## IMPORTS ##

from machine import Pin
import network
from light_manager import ledControl
import text_manager
import networking


from time import sleep
import uasyncio as asyncio



## VARIABLES ##

# Hardware

wlan = network.WLAN(network.STA_IF)

#temperature1 = 0    - Implement these when modules arrive
#temperature2 = 0
#meanTemperature = 0

#humidity1 = 0
#humidity2 = 0
#meanHumidity = 0

# Settings

username = "USERNAME"

backlightOn = True
notifsOn = True





## FUNCTIONS ##

async def main():
    text_manager.clearDisplay()
    asyncio.create_task(ledControl())

    await text_manager.scrollMessage(f"Welcome Back {username}               ", 0.2, 0, repeat=False)

    await asyncio.sleep(0.1)

    networking.connectWifi()
    networking.syncTime()

    while not wlan.isconnected():
        await text_manager.scrollMessage("Connecting to WiFi...               ", 0.2, 0, repeat=False)
        
    await text_manager.scrollMessage("Successfully connected to WiFi network!               ", 0.2, 0, repeat=False)
    
    #networking.alexaAlert(2)
    
    
    asyncio.create_task(text_manager.dynamicScrollMessage(row=1, delay=0.2))
    
    while True:
        text_manager.displayIcons(notifsOn, wlan.isconnected())
        text_manager.displayTime()
        await asyncio.sleep(1)

        if not wlan.isconnected():
            networking.connectWifi()
            while not wlan.isconnected():
                await text_manager.scrollMessage("Connecting to WiFi...               ", 0.2, 0, repeat=False)
            await text_manager.scrollMessage("Successfully connected to WiFi network!               ", 0.2, 0, repeat=False)
    
        
        
asyncio.run(main())