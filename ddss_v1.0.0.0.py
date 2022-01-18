# ==========================================================================================================================================
#   Name                           		:| Ver      :| Author			    :| Last Mod. Date 		:| Changes Made:
#   DDSS			                    :| V1.0.0.0 :| Robert Jiang			:| 01/18/2022		    :| Implemented baseline features
# ==========================================================================================================================================
#   Description
#	DDSS is a display setting utility aimed to help save laptop battery life on Windows by automatically changing the display settings
#	of the primary display when plugging and unplugging the charger.
# ==========================================================================================================================================

# Uses pywin32, psutil, time, and sys
import pywintypes
import win32api
import win32con
import psutil
import time
import sys

i = 0
max_rr = 0  # max refresh rate
min_rr = sys.maxsize # min refresh rate
res_supported = set() # supported resolutions

# find max refresh rate, min refresh rate, and supported resolutions
try:
  while (True):
    ds = win32api.EnumDisplaySettings(None, i) # iterate through primary monitor display settings

    max_rr = ds.DisplayFrequency if (ds.DisplayFrequency > max_rr) else max_rr # find max refresh rate
    min_rr = ds.DisplayFrequency if (ds.DisplayFrequency < min_rr) else min_rr # find min refresh rate

    res_supported.add(tuple([ds.PelsWidth, ds.PelsHeight])) # get supported resolutions

    i+=1
except: pass

# priority list of resolutions when on AC
res_ac = [
           tuple([2560, 1440]),
           tuple([1920, 1080]),
           tuple([1600, 900]),
           tuple([1366, 768]),

           tuple([2560, 1600]),
           tuple([1920, 1200]),
           tuple([1680, 1050]),
           tuple([1440, 900]),

           tuple([2048, 1536]),
           tuple([1920, 1440]),
           tuple([1600, 1200]),
           tuple([1440, 1080])]

# priority list of resolutions when on battery
res_bat = [tuple([1280, 720]),
           tuple([1152, 648]),
           tuple([1024, 576]),

           tuple([1280, 800]),

           tuple([1280, 960]),
           tuple([1024, 768])]

# choose highest supported resolution in priority list when on AC
for res in res_ac:
    if (res in res_supported):
        ac_res = res
        break

# choose highest supported resolution in priority list when on battery
for res in res_bat:
    if (res in res_supported):
        bat_res = res
        break


PYDEVMODE = pywintypes.DEVMODEType() # Instantiate PyDEVMODE object to change display settings
PYDEVMODE.Fields = win32con.DM_DISPLAYFREQUENCY | win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT # Indicate which fields were modified

curr_power_mode = psutil.sensors_battery().power_plugged # Get current power mode (AC or battery)

# Set display settings according to current power mode
if (curr_power_mode):
    PYDEVMODE.DisplayFrequency = max_rr
    PYDEVMODE.PelsWidth = ac_res[0]
    PYDEVMODE.PelsHeight = ac_res[1]
else:
    PYDEVMODE.DisplayFrequency = min_rr
    PYDEVMODE.PelsWidth = bat_res[0]
    PYDEVMODE.PelsHeight = bat_res[1]

win32api.ChangeDisplaySettings(PYDEVMODE, 0) # Change display settings on primary monitor
prev_power_mode = curr_power_mode # Set the previous power mode to the current power mode
time.sleep(0.001) # Delay execution by 0.001 seconds

# Repeat in background
while (True):
    curr_power_mode = psutil.sensors_battery().power_plugged

    # Only change display settings on primary monitor when the power mode changes
    if (curr_power_mode != prev_power_mode):
        if (curr_power_mode):
            PYDEVMODE.DisplayFrequency = max_rr
            PYDEVMODE.PelsWidth = ac_res[0]
            PYDEVMODE.PelsHeight = ac_res[1]
        else:
            PYDEVMODE.DisplayFrequency = min_rr
            PYDEVMODE.PelsWidth = bat_res[0]
            PYDEVMODE.PelsHeight = bat_res[1]

        win32api.ChangeDisplaySettings(PYDEVMODE, 0)

    prev_power_mode = curr_power_mode
    time.sleep(0.001)