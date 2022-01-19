import psutil
import time
import os
import ddss_config
import ddss_constants
import ddss_display
import pystray
from PIL import Image
from pystray import Icon as icon
from pystray import Menu as menu
from pystray import MenuItem as item
from threading import Thread
import pythoncom
import urllib.request

# ====================================================================================================================
# Author: Robert Jiang
# Name: DDSS v1.5.0.0
# File Name: ddss.py
# Description: Runs DDSS in the background and the SDSS system tray app simulatenously in the background
# Version: 1.5.0.0
# ====================================================================================================================

# Global variables
icon_name = "DDSS v1.5.0.0" # Name of icon when hovering mouse over it
icon_url = "https://i.imgur.com/ACbR587.png" # imgur url to SDSS icon png
stop = False # Used to stop DDSS when SDSS is stopped

# Runs DDSS in the background
def ddss():
    if stop:
        return

    pythoncom.CoInitialize()

    ac_rs, ac_rr, ac_br, by_rs, by_rr, by_br = ddss_display.set_settings()
    curr_power_mode = psutil.sensors_battery().power_plugged # Get current power mode (AC or battery)

    # Set display settings according to current power mode
    if (curr_power_mode):
        ddss_display.change_settings(ac_rs[0], ac_rs[1], ac_rr, ac_br)
    else:
        ddss_display.change_settings(by_rs[0], by_rs[1], by_rr, by_br)

    prev_power_mode = curr_power_mode # Set the previous power mode to the current power mode
    time.sleep(0.001) # Delay execution by 0.001 seconds

    # Repeat in background
    while (True):
        if stop:
            break

        curr_power_mode = psutil.sensors_battery().power_plugged

        # Only change display settings on primary monitor when the power mode changes
        if (curr_power_mode != prev_power_mode):
            if (curr_power_mode):
                ddss_display.change_settings(ac_rs[0], ac_rs[1], ac_rr, ac_br)
            else:
                ddss_display.change_settings(by_rs[0], by_rs[1], by_rr, by_br)

        prev_power_mode = curr_power_mode
        time.sleep(0.001)

# Stops DDSS and the SDSS tray when the user clicks on the 'Quit' menu item
def quit():
    # Set `stop` to True to stop DDSS
    global stop
    stop = True

    # Stop the icon from running
    icon.visible = False
    icon.stop()

# Creates the Static Display Settings Switcher (SDSS) icon allowing for manual resolution and refresh rate switching
def create_icon():
    # Get supported and current display settings
    rs_supported, rr_supported, br_supported, rr_min, rr_max = ddss_display.get_supported_settings()
    rs_curr, rr_curr, br_curr = ddss_display.get_current_settings()

    # Check if the system tray icon png exists, if not download it from imgur
    if (not (os.path.exists(os.getcwd() + "\ddss_icon.png"))):
        urllib.request.urlretrieve(icon_url, get_icon_path())

    image = Image.open("ddss_icon.png")

    # add all supported resolutions and refresh rates as items in the menu
    menu_items = []
    for rs in sorted(rs_supported):
        menu_items.append(item(str(rs[0]) + 'x' + str(rs[1]), (lambda w, h: lambda: ddss_display.change_resolution(w, h))(rs[0], rs[1])))
    for rr in sorted(rr_supported):
        menu_items.append(item(str(rr) + 'Hz', (lambda r: lambda: ddss_display.change_refresh_rate(r))(rr)))
    menu_items.append(item('Quit', lambda: quit()))

    return icon("Dynamic Display Settings Switcher", image, icon_name, tuple(menu_items))


if __name__ == "__main__":
    # Create the SDSS tray icon
    icon = create_icon()

    # Run DDSS and SDSS in separate threads
    Thread(target=ddss).start()
    Thread(target=icon.run).start()
