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
    print("Synchronising with NTP...")
    try:
        ntptime.settime()  # sets UTC
        print("Time synced successfully.")
    except Exception as e:
        print("NTP sync failed:", e)

def localTime():
    # Check if British Summer Time (Clocks move forward) should be applied (last Sunday in March to last Sunday in October)
    t = time.localtime()  # UTC
    year = t[0]
    month = t[1]
    day = t[2]

    # Calculate last Sunday in March
    lastSundayinMarch = max(d for d in range(31, 24, -1)
                            if time.localtime(time.mktime((year, 3, d, 0, 0, 0, 0, 0)))[6] == 6)
    # Calculate last Sunday in October
    lastSundayinnOctober = max(d for d in range(31, 24, -1)
                              if time.localtime(time.mktime((year, 10, d, 0, 0, 0, 0, 0)))[6] == 6)

    # Determine if within BST
    if (month > 3 and month < 10) or (month == 3 and day >= lastSundayinMarch) or (month == 10 and day < lastSundayinnOctober):
        offset = 3600  # +1 hour for BST
    else:
        offset = 0  # GMT

    t_local = time.localtime(time.time() + offset)
    return t_local