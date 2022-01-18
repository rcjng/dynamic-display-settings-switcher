import pywintypes
import win32api
import win32con
import psutil
import sched
import time
import sys

i = 0
max_rf = 0
min_rf = sys.maxsize
res_supported = set()

try:
  while (True):
    ds = win32api.EnumDisplaySettings(None, i)

    max_rf = ds.DisplayFrequency if (ds.DisplayFrequency > max_rf) else max_rf
    min_rf = ds.DisplayFrequency if (ds.DisplayFrequency < min_rf) else min_rf

    res_supported.add(tuple([ds.PelsWidth, ds.PelsHeight]))

    i+=1
except: pass

res_max = [
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

res_min = [tuple([1280, 720]),
           tuple([1152, 648]),
           tuple([1024, 576]),

           tuple([1280, 800]),

           tuple([1280, 960]),
           tuple([1024, 768])]

for res in res_max:
    if (res in res_supported):
        max_res = res
        break

for res in res_min:
    if (res in res_supported):
        min_res = res
        break

PYDEVMODE = pywintypes.DEVMODEType()
PYDEVMODE.Fields = win32con.DM_DISPLAYFREQUENCY | win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

curr_power_mode = psutil.sensors_battery().power_plugged
if (curr_power_mode):
    PYDEVMODE.DisplayFrequency = max_rf
    PYDEVMODE.PelsWidth = max_res[0]
    PYDEVMODE.PelsHeight = max_res[1]
else:
    PYDEVMODE.DisplayFrequency = min_rf
    PYDEVMODE.PelsWidth = min_res[0]
    PYDEVMODE.PelsHeight = min_res[1]

win32api.ChangeDisplaySettings(PYDEVMODE, 0)
prev_power_mode = curr_power_mode
time.sleep(0.001)

while (True):
    curr_power_mode = psutil.sensors_battery().power_plugged

    if (curr_power_mode != prev_power_mode):
        if (curr_power_mode):
            PYDEVMODE.DisplayFrequency = max_rf
            PYDEVMODE.PelsWidth = max_res[0]
            PYDEVMODE.PelsHeight = max_res[1]
        else:
            PYDEVMODE.DisplayFrequency = min_rf
            PYDEVMODE.PelsWidth = min_res[0]
            PYDEVMODE.PelsHeight = min_res[1]

        win32api.ChangeDisplaySettings(PYDEVMODE, 0)

    prev_power_mode = curr_power_mode
    time.sleep(0.001)