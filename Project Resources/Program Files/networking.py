## IMPORTS ##

import network
import urequests
import ntptime
import time

## VARIABLES

WIFI_SSID = "REPLACE WITH WIFI SSID"
WIFI_PASSWORD = "REPLACE WITH WIFI PASSWORD"


voiceMonkeyTokens = [] # Fill in with tokens
# 0 = Too Hot. 1 = Too Cold. 2 = Connection Test Message. 3 = Feeding Time (May remove in future)


## FUNCTIONS ##

def connectWifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

def alexaAlert(messageType):
    base_url = "https://api-v2.voicemonkey.io/announcement?"
    
    params = voiceMonkeyTokens[messageType]
        
    url = base_url + params

    print("Sending request to:", url)
    try:
        response = urequests.get(url)
        print("Response:", response.text)
        response.close()
    except Exception as e:
        print("Error:", e)
        
def syncTime():
    try:
        ntptime.settime()
        return True
    except Exception as e:
        return False

def localTime():
    # Get current UTC time from RTC
    t = time.localtime()
    year, month, day = t[0], t[1], t[2]

    def lastSunday(year, month):
        # Start from last day of the month and move backwards to Sunday
        for d in range(31, 24, -1):
            try:
                if time.localtime(time.mktime((year, month, d, 0, 0, 0, 0, 0)))[6] == 6:
                    return d
            except:
                continue
        return 31

    lastSundayMarch = lastSunday(year, 3)
    lastSundayOctober = lastSunday(year, 10)

    # Determine if within BST
    if (month > 3 and month < 10) or \
       (month == 3 and day >= lastSundayMarch) or \
       (month == 10 and day < lastSundayOctober):
        offset = 3600  # +1 hour
    else:
        offset = 0     # GMT

    t_local = time.localtime(time.time() + offset)
    return t_local