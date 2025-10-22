from machine import Pin
import network
import uasyncio as asyncio

wlan = network.WLAN(network.STA_IF)

warningLight = Pin(12, Pin.OUT)
wifiLight = Pin(25, Pin.OUT)
powerLight = Pin(14, Pin.OUT)

warningLight.value(0)
wifiLight.value(0)
powerLight.value(0)

async def ledControl():  
    while True:
        if wlan.isconnected():
            wifiLight.value(1)
            
        else:
            wifiLight.value(0)
            await asyncio.sleep(0.5)
            wifiLight.value(1)
            
        powerLight.value(1)

        # If there is any kind of warning the warning light should flash brightly, otherwise it will be off
            
        await asyncio.sleep(0.5)