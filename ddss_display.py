import os
import pywintypes
import win32api
import win32con
import wmi
import sys
import ddss_config

# ====================================================================================================================
# Author: Robert Jiang
# Name: DDSS v1.5.0.0
# File Name: ddss_display.py
# Description: Stores functions used by DDSS regarding the display and its settings
# Version: 1.5.0.0
# ====================================================================================================================

# Returns the settings to be set by reading the config file and determining if the settings are supported by the display
def set_settings():

    # if no config file exists, create the default config
    if (not (os.path.exists(ddss_config.get_config_path()))):
        ddss_config.create_config()

    # read config file
    config_ac_rs, config_ac_rr, config_ac_br, config_by_rs, config_by_rr, config_by_br = ddss_config.read_config()

    # Find supported display settings
    rs_supported, rr_supported, br_supported, rr_min, rr_max = get_supported_settings()


    # Set resolution when on AC
    if (config_ac_rs in rs_supported):
        ac_rs = config_ac_rs
    else:
        for rs in ddss_constants.ac_rs_priority:
            if (rs in rs_supported):
                ac_rs = rs
                break

    # Set refresh rate when on AC
    if (config_ac_rr in rr_supported):
        ac_rr = config_ac_rr
    else:
        ac_rr = rr_max

    # Set brightness when on AC
    if (config_ac_br in br_supported):
        ac_br = config_ac_br
    else:
        ac_br = 100

    # Set resolution when on Battery
    if (config_by_rs in rs_supported):
        by_rs = config_by_rs
    else:
        for rs in ddss_constants.by_rs_priority:
            if (rs in rs_supported):
                by_rs = rs
                break

    # Set refresh rate when on Battery
    if (config_by_rr in rr_supported):
        by_rr = config_by_rr
    else:
        by_rr = rr_min

    # Set brightness when on Battery
    if (config_by_br in br_supported):
        by_br = config_by_br
    else:
        by_br = 0

    return ac_rs, ac_rr, ac_br, by_rs, by_rr, by_br

# Reeturns the supported display settings and the lowest and highest supported refresh rates
def get_supported_settings():
    i = 0
    rr_max = 0
    rr_min = sys.maxsize
    rr_supported = set()
    rs_supported = set()
    br_supported = wmi.WMI(namespace='wmi').WmiMonitorBrightness()[0].Level

    try:
        while (True):
            ds = win32api.EnumDisplaySettings(None, i)
            rr_max = ds.DisplayFrequency if (ds.DisplayFrequency > rr_max) else rr_max  # find max refresh rate
            rr_min = ds.DisplayFrequency if (ds.DisplayFrequency < rr_min) else rr_min  # find min refresh rate
            rr_supported.add(ds.DisplayFrequency);
            rs_supported.add(tuple([ds.PelsWidth, ds.PelsHeight]))
            i += 1
    except:
        pass

    return rs_supported, rr_supported, br_supported, rr_min, rr_max

# Returns the current display settings used by the display
def get_current_settings():
    ds = win32api.EnumDisplaySettings(None, -1)
    rs_curr = [ds.PelsWidth, ds.PelsHeight]
    rr_curr = ds.DisplayFrequency
    br_curr = wmi.WMI(namespace='wmi').WmiMonitorBrightness()[0].CurrentBrightness

    return rs_curr, rr_curr, br_curr

# Changes the primary display's display settings to a given resolution, refresh rate, and brightness
def change_settings(w: int, h: int, rr: int, br: int):
    change_resolution(w, h)
    change_refresh_rate(rr)
    change_brightness(br)

# Changes the primary display's resolution to a given resolution
def change_resolution(w: int, h: int):
    PYDEVMODE = pywintypes.DEVMODEType()

    PYDEVMODE.PelsWidth = w
    PYDEVMODE.PelsHeight = h
    PYDEVMODE.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    win32api.ChangeDisplaySettings(PYDEVMODE, 0)

# Changes the primary display's refresh rate to a given refresh rate
def change_refresh_rate(rr: int):
    PYDEVMODE = pywintypes.DEVMODEType()

    PYDEVMODE.DisplayFrequency = rr
    PYDEVMODE.Fields = win32con.DM_DISPLAYFREQUENCY

    win32api.ChangeDisplaySettings(PYDEVMODE, 0)

# Changes the primary display's brightness to a given brightness
def change_brightness(br: int):
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(br, 0)